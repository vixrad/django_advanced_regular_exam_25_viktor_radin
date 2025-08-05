from django.urls import path
from . import views

urlpatterns = [
    path('my/', views.MyReservationsView.as_view(), name='my_reservations'),
    path('owner/', views.OwnerReservationsView.as_view(), name='owner_reservations'),
    path('new/', views.ReservationCreateView.as_view(), name='reservation_create'),
    path('new/<int:restaurant_id>/', views.ReservationCreateView.as_view(), name='reservation_create_with_restaurant'),
    path('<int:pk>/', views.ReservationDetailView.as_view(), name='reservation_detail'),
    path('<int:pk>/review/', views.leave_review, name='leave_review'),
    path('api/restaurants/<int:restaurant_id>/timeslots/', views.available_timeslots, name='available_timeslots'),
    path('cancel/<int:pk>/', views.cancel_reservation, name='cancel_reservation'),
    path('owner/confirm/<int:pk>/', views.owner_confirm_reservation, name='owner_confirm_reservation'),
    path('owner/cancel/<int:pk>/', views.owner_cancel_reservation, name='owner_cancel_reservation'),
]