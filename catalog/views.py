from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Category, Favorite, Product


def _get_favorite_ids(request):
    """Retourne l'ensemble des IDs de produits favoris de l'utilisateur connecté."""
    if not request.user.is_authenticated:
        return set()
    return set(Favorite.objects.filter(user=request.user).values_list('product_id', flat=True))


def home(request):
    return render(request, 'catalog/home.html', {
        'featured': Product.objects.filter(is_active=True)[:4],
        'categories': Category.objects.all()[:4],
        'favorite_ids': _get_favorite_ids(request),
    })


def shop(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '')
    products = Product.objects.filter(is_active=True).select_related('category', 'seller')
    if query:
        products = products.filter(Q(name__icontains=query) | Q(category__name__icontains=query) | Q(city__icontains=query))
    if category:
        products = products.filter(category__slug=category)
    return render(request, 'catalog/shop.html', {
        'products': products,
        'categories': Category.objects.all(),
        'query': query,
        'current_category': category,
        'favorite_ids': _get_favorite_ids(request),
    })


def product_detail(request, slug):
    product = get_object_or_404(Product.objects.select_related('seller', 'category'), slug=slug, is_active=True)
    is_favorited = request.user.is_authenticated and Favorite.objects.filter(user=request.user, product=product).exists()
    return render(request, 'catalog/product_detail.html', {'product': product, 'is_favorited': is_favorited})


@login_required
def toggle_favorite(request, product_id):
    if request.method != 'POST':
        return redirect('shop')
    product = get_object_or_404(Product, id=product_id, is_active=True)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
    if created:
        messages.success(request, f'{product.name} a été ajouté à vos favoris.')
    else:
        favorite.delete()
        messages.info(request, f'{product.name} a été retiré de vos favoris.')
    return redirect(request.POST.get('next') or product.get_absolute_url())


@login_required
def favorites(request):
    products = Product.objects.filter(favorited_by__user=request.user, is_active=True).select_related('category', 'seller')
    return render(request, 'catalog/favorites.html', {
        'products': products,
        'favorite_ids': _get_favorite_ids(request),
    })