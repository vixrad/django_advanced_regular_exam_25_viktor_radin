from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from core.utils import generate_available_time_slots
from restaurants.models import Restaurant


class Reservation(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_COMPLETED = 'completed'
    STATUS_NO_SHOW = 'no_show'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_CONFIRMED, 'Confirmed'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_NO_SHOW, 'No Show'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    reservation_time = models.DateTimeField()
    number_of_people = models.PositiveIntegerField(default=1)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-reservation_time']
        indexes = [
            models.Index(fields=['restaurant', 'reservation_time']),
            models.Index(fields=['user', 'status']),
        ]

    def clean(self):
        # Ensure reservation_time is provided
        if not self.reservation_time:
            raise ValidationError({"reservation_time": "Please select a date and time for your reservation."})

        # Reservation must be in the future
        if self.reservation_time < timezone.now():
            raise ValidationError({"reservation_time": "Reservation time must be in the future."})

        # Check if restaurant is open on the selected day
        weekday = self.reservation_time.weekday()
        opening = self.restaurant.opening_hours.filter(day_of_week=weekday).first()
        if not opening or opening.is_closed:
            raise ValidationError({"reservation_time": "The restaurant is closed on this day."})

        # Check if selected time is valid according to opening hours
        slots = generate_available_time_slots(opening.open_time, opening.close_time)
        if self.reservation_time.time() not in slots:
            raise ValidationError({
                "reservation_time": "Invalid time. Please choose one of the available 30-minute slots."
            })

    def __str__(self):
        return f"{self.restaurant.name} | {self.user.email} | {self.reservation_time.strftime('%Y-%m-%d %H:%M')}"


class Review(models.Model):
    reservation = models.OneToOneField(
        Reservation,
        on_delete=models.CASCADE,
        related_name='review'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.PositiveSmallIntegerField(default=5, help_text="Rating from 1 to 5")
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['rating'])]

    def clean(self):
        if self.reservation.status != Reservation.STATUS_COMPLETED:
            raise ValidationError("You can only leave a review for a completed reservation.")

    def __str__(self):
        return f"Review {self.rating}/5 by {self.user.email} for {self.reservation.restaurant.name}"