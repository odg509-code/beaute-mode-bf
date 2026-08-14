from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('connexion/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('inscription/', views.signup, name='signup'),
    path('deconnexion/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    # Dashboards
    path('tableau-de-bord/', views.dashboard, name='dashboard'),
    path('tableau-de-bord/client/', views.customer_dashboard, name='customer_dashboard'),
    path('tableau-de-bord/vendeur/', views.seller_dashboard, name='seller_dashboard'),
    path('tableau-de-bord/institut/', views.institute_dashboard, name='institute_dashboard'),
    path('tableau-de-bord/styliste/', views.stylist_dashboard, name='stylist_dashboard'),
    path('tableau-de-bord/options/<slug:section>/', views.dashboard_option, name='dashboard_option'),
]
