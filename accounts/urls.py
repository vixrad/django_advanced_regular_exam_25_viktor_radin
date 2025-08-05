from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import register, CustomLoginView, profile, edit_profile
from .api_views import company_lookup

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),

    # API endpoint (Django REST)
    path('api/companies/<str:company_number>/', company_lookup, name='company_lookup_api'),
]