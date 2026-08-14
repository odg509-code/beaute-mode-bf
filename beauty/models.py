from django.conf import settings
from django.db import models
class Institute(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='institutes')
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    city = models.CharField(max_length=80, default='Ouagadougou')
    neighborhood = models.CharField(max_length=80)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=30)
    whatsapp = models.CharField(max_length=30, blank=True)
    image_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    def __str__(self): return self.name
class Service(models.Model):
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=100)
    duration_minutes = models.PositiveIntegerField(default=60)
    price = models.PositiveIntegerField()
class Appointment(models.Model):
    class Status(models.TextChoices): PENDING='pending','En attente'; CONFIRMED='confirmed','Confirmé'; COMPLETED='completed','Terminé'; CANCELLED='cancelled','Annulé'
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='appointments')
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='appointments')
    starts_at = models.DateTimeField()
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING)
    note = models.TextField(blank=True)
