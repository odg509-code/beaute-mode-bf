from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [path('admin/', admin.site.urls), path('', include('catalog.urls')), path('compte/', include('accounts.urls')), path('panier/', include('commerce.urls')), path('instituts/', include('beauty.urls'))]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
