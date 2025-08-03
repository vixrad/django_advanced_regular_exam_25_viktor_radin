from django.urls import path
from .views import register, CustomLoginView, company_lookup

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('api/companies/<str:company_number>/', company_lookup, name='company_lookup'),
]