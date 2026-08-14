from django.urls import path
from . import views
urlpatterns = [path('', views.home, name='home'), path('boutique/', views.shop, name='shop'), path('produit/<slug:slug>/', views.product_detail, name='product_detail'), path('favoris/', views.favorites, name='favorites'), path('favoris/<int:product_id>/', views.toggle_favorite, name='toggle_favorite')]
