from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = 'customer', 'Client'
        SELLER = 'seller', 'Vendeur'
        INSTITUTE = 'institute', 'Institut'
        STYLIST = 'stylist', 'Styliste'
        ADMIN = 'admin', 'Administrateur'
    
    class Country(models.TextChoices):
        BURKINA_FASO = 'bf', 'Burkina Faso'
        IVORY_COAST = 'ci', "Côte d'Ivoire"
        MALI = 'ml', 'Mali'
        GUINEA = 'gn', 'Guinée'
        SENEGAL = 'sn', 'Sénégal'
        NIGER = 'ne', 'Niger'
        BENIN = 'bj', 'Bénin'
        CAMEROON = 'cm', 'Cameroun'
        GABON = 'ga', 'Gabon'
        DRC = 'cd', 'République Démocratique du Congo'
        OTHER = 'other', 'Autre pays'
    
    role = models.CharField(max_length=16, choices=Role.choices, default=Role.CUSTOMER)
    phone = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=20, choices=Country.choices, default=Country.BURKINA_FASO)
    city = models.CharField(max_length=80, blank=True)

class ProfessionalProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='professional_profile')
    business_name = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    city = models.CharField(max_length=80, default='Ouagadougou')
    neighborhood = models.CharField(max_length=80, blank=True)
    whatsapp = models.CharField(max_length=30, blank=True)
    verified = models.BooleanField(default=False)
