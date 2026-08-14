from django.test import TestCase
from django.urls import reverse

from beauty.models import Institute
from catalog.models import Category, Product
from commerce.models import Order, OrderItem
from .models import User


class AccountFlowsTests(TestCase):
    def test_signup_creates_customer_and_redirects_to_dashboard(self):
        response = self.client.post(reverse('signup'), {
            'username': 'aminata', 'email': 'aminata@example.com', 'first_name': 'Aminata', 'last_name': 'Traore',
            'phone': '70000000', 'country': User.Country.BURKINA_FASO, 'city': 'Bobo-Dioulasso',
            'role': User.Role.CUSTOMER, 'password1': 'Motdepasse123!', 'password2': 'Motdepasse123!',
        })

        self.assertRedirects(response, reverse('dashboard'), fetch_redirect_response=False)
        self.assertTrue(User.objects.filter(username='aminata').exists())

    def test_signup_cannot_create_an_administrator(self):
        response = self.client.post(reverse('signup'), {
            'username': 'admin-malicious', 'email': 'admin@example.com', 'first_name': 'Admin', 'last_name': 'Test',
            'country': User.Country.BURKINA_FASO, 'role': User.Role.ADMIN,
            'password1': 'Motdepasse123!', 'password2': 'Motdepasse123!',
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='admin-malicious').exists())

    def test_signup_role_can_be_preselected_from_public_home_links(self):
        response = self.client.get(f"{reverse('signup')}?role={User.Role.SELLER}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].initial['role'], User.Role.SELLER)

    def test_dashboard_routes_each_role_to_its_page(self):
        routes = {
            User.Role.CUSTOMER: 'customer_dashboard', User.Role.SELLER: 'seller_dashboard',
            User.Role.INSTITUTE: 'institute_dashboard', User.Role.STYLIST: 'stylist_dashboard',
        }
        for role, destination in routes.items():
            user = User.objects.create_user(username=f'{role}-user', password='motdepasse123', role=role)
            self.client.force_login(user)

            response = self.client.get(reverse('dashboard'))

            self.assertRedirects(response, reverse(destination))

    def test_logout_requires_post_and_ends_the_session(self):
        user = User.objects.create_user(username='connecte', password='motdepasse123')
        self.client.force_login(user)

        self.assertEqual(self.client.get(reverse('logout')).status_code, 405)
        response = self.client.post(reverse('logout'))

        self.assertRedirects(response, reverse('home'))
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_settings_updates_the_authenticated_user(self):
        user = User.objects.create_user(username='profil', password='motdepasse123', first_name='Ancien')
        self.client.force_login(user)

        response = self.client.post(reverse('dashboard_option', args=['settings']), {
            'first_name': 'Nouveau', 'last_name': 'Nom', 'email': 'nouveau@example.com',
            'phone': '70000000', 'country': User.Country.BURKINA_FASO, 'city': 'Ouagadougou',
        })

        self.assertRedirects(response, reverse('dashboard_option', args=['settings']))
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'Nouveau')

    def test_seller_dashboard_calculates_revenue(self):
        seller = User.objects.create_user(username='vendeur', password='motdepasse123', role=User.Role.SELLER)
        buyer = User.objects.create_user(username='cliente', password='motdepasse123')
        category = Category.objects.create(name='Accessoires', slug='accessoires')
        product = Product.objects.create(seller=seller, category=category, name='Sac', slug='sac', description='Sac', price=5000, stock=1)
        order = Order.objects.create(user=buyer, total=15000, delivery_city='Ouaga', delivery_address='Centre')
        OrderItem.objects.create(order=order, product=product, quantity=3, unit_price=5000)
        self.client.force_login(seller)

        response = self.client.get(reverse('seller_dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_revenue'], 15000)

    def test_institute_dashboard_displays_owned_institute(self):
        owner = User.objects.create_user(username='institut', password='motdepasse123', role=User.Role.INSTITUTE)
        institute = Institute.objects.create(owner=owner, name='Belle Peau', slug='belle-peau', description='Soins', neighborhood='Koulouba', address='Rue', phone='70000000')
        self.client.force_login(owner)

        response = self.client.get(reverse('institute_dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['institute'], institute)
