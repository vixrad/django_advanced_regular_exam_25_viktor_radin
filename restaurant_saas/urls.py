"""
URL configuration for restaurant_saas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core import views as core_views
from core.views import ContactView, AboutView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Accounts app (register, login, logout, company lookup API)
    path('accounts/', include('accounts.urls')),

    # Built-in auth URLs (password reset, change, etc.)
    path('accounts/', include('django.contrib.auth.urls')),

    # Core site pages
    path('', core_views.home, name='home'),
    path('restaurants/', include('restaurants.urls')),
    path('contact/', ContactView.as_view(), name='contact'),
    path('about/', AboutView.as_view(), name='about'),
    path('menu/', include('menu.urls')),
    path('orders/', include('orders.urls')),
]