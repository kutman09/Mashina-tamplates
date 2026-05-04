from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('cars/', include(('apps.cars.urls', 'cars'), namespace='cars')),
    path('accounts/', include('allauth.urls')),
    path('profile/', include(('apps.accounts.urls', 'accounts'), namespace='accounts')),
    path('favorites/', include(('apps.favorites.urls', 'favorites'), namespace='favorites')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
