from django.contrib import admin
from .models import Reservation, Review

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'user', 'reservation_time', 'number_of_people', 'status', 'created_at')
    list_filter = ('status', 'reservation_time', 'restaurant')
    search_fields = ('user__email', 'restaurant__name')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('reservation', 'user', 'rating', 'created_at')
    search_fields = ('user__email', 'reservation__restaurant__name')
    list_filter = ('rating',)