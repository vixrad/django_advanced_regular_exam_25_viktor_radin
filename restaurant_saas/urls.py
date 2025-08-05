from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views as core_views
from core.views import ContactView, AboutView

urlpatterns = [
    path('admin/', admin.site.urls),

    # accounts app (register, login, logout, company lookup api)
    path('accounts/', include('accounts.urls')),

    # built-in auth urls (password reset, change, etc.)
    path('accounts/', include('django.contrib.auth.urls')),

    # core site pages
    path('', core_views.home, name='home'),
    path('restaurants/', include('restaurants.urls')),
    path('contact/', ContactView.as_view(), name='contact'),
    path('about/', AboutView.as_view(), name='about'),
    path('menu/', include('menu.urls')),
    # orders url disabled for now
    # path('orders/', include('orders.urls')),
    path('reservations/', include('reservations.urls'))
]

# serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)