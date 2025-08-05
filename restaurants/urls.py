from django.urls import path
from . import views

urlpatterns = [
    path('', views.RestaurantListView.as_view(), name='restaurant_list'),
    path('add/', views.add_restaurant, name='add_restaurant'),
    path('<int:pk>/edit/', views.edit_restaurant, name='edit_restaurant'),
    path('<int:pk>/delete/', views.delete_restaurant, name='delete_restaurant'),
    # NEW endpoint for AJAX timeslots
    path('<int:restaurant_id>/timeslots/', views.get_timeslots, name='get_timeslots'),
]