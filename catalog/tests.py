from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from .models import Category, Favorite, Product


class CatalogViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        seller = User.objects.create_user(username='vendeur', password='motdepasse123', role=User.Role.SELLER)
        cls.category = Category.objects.create(name='Tissus', slug='tissus')
        cls.product = Product.objects.create(
            seller=seller, category=cls.category, name='Faso Dan Fani', slug='faso-dan-fani',
            description='Tissu traditionnel', price=15000, stock=5,
        )
        cls.inactive_product = Product.objects.create(
            seller=seller, category=cls.category, name='Produit caché', slug='produit-cache',
            description='Indisponible', price=5000, stock=0, is_active=False,
        )

    def test_home_displays_active_featured_products(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="hero"')
        self.assertContains(response, self.product.name)
        self.assertNotContains(response, self.inactive_product.name)

    def test_shop_filters_by_query_and_category(self):
        response = self.client.get(reverse('shop'), {'q': 'Faso', 'category': self.category.slug})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)
        self.assertNotContains(response, self.inactive_product.name)

    def test_product_detail_is_available_only_for_active_product(self):
        response = self.client.get(self.product.get_absolute_url())
        hidden_response = self.client.get(self.inactive_product.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(hidden_response.status_code, 404)

    def test_favorites_require_authentication(self):
        response = self.client.get(reverse('favorites'))

        self.assertRedirects(response, f"{reverse('login')}?next={reverse('favorites')}")

    def test_user_can_add_and_remove_a_favorite(self):
        customer = User.objects.create_user(username='cliente', password='motdepasse123')
        self.client.force_login(customer)

        add_response = self.client.post(reverse('toggle_favorite', args=[self.product.id]))
        self.assertRedirects(add_response, self.product.get_absolute_url())
        self.assertTrue(Favorite.objects.filter(user=customer, product=self.product).exists())

        favorites_response = self.client.get(reverse('favorites'))
        self.assertContains(favorites_response, self.product.name)

        remove_response = self.client.post(reverse('toggle_favorite', args=[self.product.id]))
        self.assertRedirects(remove_response, self.product.get_absolute_url())
        self.assertFalse(Favorite.objects.filter(user=customer, product=self.product).exists())
