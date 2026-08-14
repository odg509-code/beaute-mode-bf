from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from catalog.models import Product
from .forms import CheckoutForm
from .models import Order, OrderItem, Payment


def cart_lines(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys(), is_active=True).select_related('category')
    lines = [
        {'product': product, 'quantity': cart[str(product.id)], 'line_total': product.price * cart[str(product.id)]}
        for product in products
        if str(product.id) in cart
    ]
    return lines


def cart_detail(request):
    lines = cart_lines(request)
    return render(request, 'commerce/cart.html', {'lines':lines, 'total':sum(x['line_total'] for x in lines)})
def cart_add(request, product_id):
    if request.method != 'POST': return redirect('shop')
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = request.session.get('cart', {}); key = str(product.id)
    if product.stock < 1:
        messages.error(request, 'Ce produit est actuellement indisponible.')
        return redirect(request.POST.get('next') or 'shop')
    if cart.get(key, 0) >= product.stock:
        messages.error(request, 'La quantité demandée dépasse le stock disponible.')
        return redirect(request.POST.get('next') or 'cart_detail')
    cart[key] = cart.get(key, 0) + 1
    request.session['cart'] = cart; request.session.modified = True
    messages.success(request, f'{product.name} a été ajouté au panier.')
    return redirect(request.POST.get('next') or 'cart_detail')
def cart_remove(request, product_id):
    if request.method != 'POST':
        return redirect('cart_detail')
    cart = request.session.get('cart', {}); cart.pop(str(product_id), None); request.session['cart'] = cart; request.session.modified = True
    return redirect('cart_detail')


@login_required
def checkout(request):
    lines = cart_lines(request)
    if not lines:
        messages.info(request, 'Votre panier est vide.')
        return redirect('cart_detail')

    total = sum(line['line_total'] for line in lines)
    form = CheckoutForm(request.POST or None, user=request.user)
    if request.method == 'POST' and form.is_valid():
        with transaction.atomic():
            locked_products = {
                product.id: product
                for product in Product.objects.select_for_update().filter(id__in=[line['product'].id for line in lines])
            }
            unavailable = [line['product'].name for line in lines if locked_products.get(line['product'].id, line['product']).stock < line['quantity']]
            if unavailable:
                form.add_error(None, 'Stock insuffisant pour : ' + ', '.join(unavailable) + '.')
            else:
                order = Order.objects.create(
                    user=request.user, total=total,
                    delivery_city=form.cleaned_data['delivery_city'],
                    delivery_address=form.cleaned_data['delivery_address'],
                )
                for line in lines:
                    product = locked_products[line['product'].id]
                    OrderItem.objects.create(order=order, product=product, quantity=line['quantity'], unit_price=product.price)
                    product.stock -= line['quantity']
                    product.save(update_fields=['stock'])
                Payment.objects.create(order=order, method=form.cleaned_data['payment_method'])
                request.session['cart'] = {}
                request.session.modified = True
                messages.success(request, f'Commande #{order.id} enregistrée. Nous vous contacterons pour la confirmation.')
                return redirect('customer_dashboard')

    return render(request, 'commerce/checkout.html', {'lines': lines, 'total': total, 'form': form})
