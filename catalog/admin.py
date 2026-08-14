from django.contrib import admin
from .models import Category, Product, ProductImage, Favorite, Review
admin.site.register([Category, Product, ProductImage, Favorite, Review])
