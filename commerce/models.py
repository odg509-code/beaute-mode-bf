from django.conf import settings
from django.db import models
from catalog.models import Product
class Order(models.Model):
    class Status(models.TextChoices): PENDING='pending','En attente'; CONFIRMED='confirmed','Confirmée'; PREPARING='preparing','En préparation'; DELIVERED='delivered','Livrée'; CANCELLED='cancelled','Annulée'
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='orders')
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING)
    total = models.PositiveIntegerField()
    delivery_city = models.CharField(max_length=80)
    delivery_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()
class Payment(models.Model):
    class Method(models.TextChoices): MOBILE='mobile_money','Mobile Money'; ORANGE='orange_money','Orange Money'; MOOV='moov_money','Moov Money'; CASH='cash','Paiement à la livraison'; CARD='card','Carte bancaire'
    order = models.OneToOneField(Order, on_delete=models.PROTECT, related_name='payment')
    method = models.CharField(max_length=20, choices=Method.choices)
    provider_reference = models.CharField(max_length=120, blank=True)
    status = models.CharField(max_length=20, default='pending')
