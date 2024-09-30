from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('home.urls')),
    path('products/', include('products.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('bag/', include('bag.urls')),
    path('checkout/',include('checkout.urls')),
    path('profile/', include('profiles.urls')),
    path('management_dashboard/', include('management_dashboard.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
