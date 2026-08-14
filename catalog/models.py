from django.conf import settings
from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True)
    description = models.CharField(max_length=200, blank=True)
    image_url = models.URLField(blank=True)
    class Meta: verbose_name_plural = 'categories'
    def __str__(self): return self.name

class Product(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    name = models.CharField(max_length=160)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.PositiveIntegerField(help_text='Montant en FCFA')
    old_price = models.PositiveIntegerField(null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    city = models.CharField(max_length=80, default='Ouagadougou')
    image_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ['-created_at']
    def __str__(self): return self.name
    def get_absolute_url(self): return reverse('product_detail', args=[self.slug])
    @property
    def average_rating(self):
        value = self.reviews.aggregate(models.Avg('rating'))['rating__avg']
        return round(value or 0, 1)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=150, blank=True)

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorited_by')
    class Meta: constraints = [models.UniqueConstraint(fields=['user','product'], name='unique_product_favorite')]

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: constraints = [models.CheckConstraint(condition=models.Q(rating__gte=1, rating__lte=5), name='rating_range')]
