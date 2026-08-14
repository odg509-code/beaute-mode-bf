from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from .forms import ProfileSettingsForm, SignUpForm
from .models import User
from catalog.models import Product
from commerce.models import Order
from beauty.models import Appointment, Institute

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        allowed_roles = {role for role, _label in User.Role.choices if role != User.Role.ADMIN}
        requested_role = request.GET.get('role')
        form = SignUpForm(initial={'role': requested_role} if requested_role in allowed_roles else None)
    return render(request, 'registration/signup.html', {'form': form})

@login_required(login_url='login')
def dashboard(request):
    """Redirection vers le dashboard approprié selon le rôle"""
    user = request.user
    
    if user.role == 'customer':
        return redirect('customer_dashboard')
    elif user.role == 'seller':
        return redirect('seller_dashboard')
    elif user.role == 'institute':
        return redirect('institute_dashboard')
    elif user.role == 'stylist':
        return redirect('stylist_dashboard')
    else:
        return redirect('home')

@login_required(login_url='login')
def customer_dashboard(request):
    """Dashboard client - voir ses commandes"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    total_spent = orders.aggregate(Sum('total'))['total__sum'] or 0
    
    context = {
        'orders': orders,
        'total_spent': total_spent,
        'order_count': orders.count(),
    }
    return render(request, 'accounts/customer_dashboard.html', context)

@login_required(login_url='login')
def seller_dashboard(request):
    """Dashboard vendeur - gestion des produits"""
    products = Product.objects.filter(seller=request.user)
    sales = Order.objects.filter(items__product__seller=request.user).distinct()
    total_revenue = 0
    for order in sales:
        for item in order.items.filter(product__seller=request.user):
            total_revenue += item.unit_price * item.quantity
    
    context = {
        'products': products,
        'product_count': products.count(),
        'sales_count': sales.count(),
        'total_revenue': total_revenue,
    }
    return render(request, 'accounts/seller_dashboard.html', context)

@login_required(login_url='login')
def institute_dashboard(request):
    """Dashboard institut - gestion des rendez-vous"""
    try:
        institute = Institute.objects.get(owner=request.user)
        appointments = Appointment.objects.filter(service__institute=institute).select_related('client', 'service').order_by('starts_at')
        context = {
            'institute': institute,
            'appointments': appointments[:5],
            'appointment_count': appointments.count(),
            'today_appointment_count': appointments.filter(starts_at__date=timezone.localdate()).count(),
            'service_count': institute.services.count(),
        }
    except Institute.DoesNotExist:
        context = {
            'institute': None,
        }
    
    return render(request, 'accounts/institute_dashboard.html', context)

@login_required(login_url='login')
def stylist_dashboard(request):
    """Dashboard styliste - portfolio et réservations"""
    context = {
        'user': request.user,
        'profile': getattr(request.user, 'professional_profile', None),
    }
    return render(request, 'accounts/stylist_dashboard.html', context)


@login_required(login_url='login')
def dashboard_option(request, section):
    """Pages fonctionnelles des menus de tableau de bord."""
    labels = {
        'products': ('Mes produits', 'Gérez les produits publiés dans votre boutique.'),
        'sales': ('Mes ventes', 'Suivez les commandes contenant vos produits.'),
        'statistics': ('Statistiques', 'Les indicateurs de votre activité apparaîtront ici.'),
        'appointments': ('Rendez-vous', 'Consultez et organisez les demandes de rendez-vous.'),
        'services': ('Services', 'Gérez les prestations proposées par votre institut.'),
        'clients': ('Clients', 'Retrouvez vos clients et leur historique.'),
        'portfolio': ('Portfolio', 'Présentez vos créations et réalisations.'),
        'bookings': ('Réservations', 'Suivez vos réservations et vos demandes.'),
        'reviews': ('Avis', 'Consultez les retours de vos clients.'),
        'addresses': ('Adresses', 'Gérez vos adresses de livraison.'),
        'settings': ('Paramètres du compte', 'Mettez à jour vos informations personnelles.'),
    }
    if section not in labels:
        return redirect('dashboard')
    title, description = labels[section]
    form = ProfileSettingsForm(request.POST or None, instance=request.user)
    if section == 'settings' and request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('dashboard_option', section='settings')
    return render(request, 'accounts/dashboard_option.html', {'section': section, 'title': title, 'description': description, 'form': form})
