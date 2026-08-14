from django.contrib import admin
from .models import Institute, Service, Appointment
admin.site.register([Institute, Service, Appointment])
