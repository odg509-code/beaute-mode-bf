from django.urls import path
from . import views
urlpatterns = [path('', views.cart_detail, name='cart_detail'), path('ajouter/<int:product_id>/', views.cart_add, name='cart_add'), path('retirer/<int:product_id>/', views.cart_remove, name='cart_remove'), path('commande/', views.checkout, name='checkout')]
