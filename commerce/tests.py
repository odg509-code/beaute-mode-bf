from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from catalog.models import Category, Product
from .models import Order, Payment


class CartTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        seller = User.objects.create_user(username='vendeur', password='motdepasse123', role=User.Role.SELLER)
        category = Category.objects.create(name='Mode', slug='mode')
        cls.product = Product.objects.create(
            seller=seller, category=category, name='Robe', slug='robe',
            description='Robe élégante', price=10000, stock=3,
        )

    def test_post_adds_product_and_increments_quantity(self):
        url = reverse('cart_add', args=[self.product.id])

        first_response = self.client.post(url)
        second_response = self.client.post(url)

        self.assertRedirects(first_response, reverse('cart_detail'))
        self.assertRedirects(second_response, reverse('cart_detail'))
        self.assertEqual(self.client.session['cart'][str(self.product.id)], 2)

    def test_get_add_does_not_modify_cart(self):
        response = self.client.get(reverse('cart_add', args=[self.product.id]))

        self.assertRedirects(response, reverse('shop'))
        self.assertNotIn('cart', self.client.session)

    def test_remove_deletes_product_from_cart(self):
        session = self.client.session
        session['cart'] = {str(self.product.id): 1}
        session.save()

        response = self.client.post(reverse('cart_remove', args=[self.product.id]))

        self.assertRedirects(response, reverse('cart_detail'))
        self.assertNotIn(str(self.product.id), self.client.session['cart'])

    def test_get_remove_does_not_modify_cart(self):
        session = self.client.session
        session['cart'] = {str(self.product.id): 1}
        session.save()

        response = self.client.get(reverse('cart_remove', args=[self.product.id]))

        self.assertRedirects(response, reverse('cart_detail'))
        self.assertEqual(self.client.session['cart'], {str(self.product.id): 1})

    def test_checkout_requires_authentication(self):
        session = self.client.session
        session['cart'] = {str(self.product.id): 1}
        session.save()

        response = self.client.get(reverse('checkout'))

        self.assertRedirects(response, f"{reverse('login')}?next={reverse('checkout')}")

    def test_checkout_creates_order_payment_and_reduces_stock(self):
        buyer = User.objects.create_user(username='cliente', password='motdepasse123', city='Ouagadougou')
        session = self.client.session
        session['cart'] = {str(self.product.id): 2}
        session.save()
        self.client.force_login(buyer)

        response = self.client.post(reverse('checkout'), {
            'delivery_city': 'Ouagadougou',
            'delivery_address': 'Secteur 15, près du marché',
            'payment_method': Payment.Method.CASH,
        })

        self.assertRedirects(response, reverse('customer_dashboard'))
        order = Order.objects.get()
        self.assertEqual(order.total, 20000)
        self.assertEqual(order.items.get().quantity, 2)
        self.assertEqual(order.payment.method, Payment.Method.CASH)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 1)
        self.assertEqual(self.client.session['cart'], {})

    def test_checkout_rejects_unavailable_stock(self):
        buyer = User.objects.create_user(username='cliente', password='motdepasse123')
        session = self.client.session
        session['cart'] = {str(self.product.id): 4}
        session.save()
        self.client.force_login(buyer)

        response = self.client.post(reverse('checkout'), {
            'delivery_city': 'Ouagadougou', 'delivery_address': 'Secteur 15',
            'payment_method': Payment.Method.CASH,
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Stock insuffisant')
        self.assertFalse(Order.objects.exists())
