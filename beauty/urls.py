from django.urls import path
from . import views
urlpatterns = [path('', views.institutes, name='institutes'), path('<slug:slug>/reserver/', views.book, name='book')]
