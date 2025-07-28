from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from core.utils import generate_available_time_slots
from restaurants.models import Restaurant

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('no_show', 'No Show'),
        ('cancelled', 'Cancelled'),
    ]

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reservation_time = models.DateTimeField()
    number_of_people = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        weekday = self.reservation_time.weekday()
        opening = self.restaurant.opening_hours.filter(day_of_week=weekday).first()
        if not opening:
            raise ValidationError("Restaurant is closed on this day.")

        slots = generate_available_time_slots(opening.open_time, opening.close_time)
        if self.reservation_time.time() not in slots:
            raise ValidationError(
                "Invalid reservation time (must be on a 30-minute slot within opening hours)."
            )

    def __str__(self):
        return f"Reservation at {self.restaurant.name} by {self.user} on {self.reservation_time}"


class Review(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name='review')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(default=5, help_text="Rating from 1 to 5")
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.reservation.status != 'completed':
            raise ValidationError("You can only leave a review for a completed reservation.")

    def __str__(self):
        return f"Review by {self.user} for {self.reservation.restaurant.name}"