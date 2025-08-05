from django.db import models
from django.conf import settings
from .validators import validate_1920x1080_image


class Restaurant(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='restaurants'
    )
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=False)
    postal_code = models.CharField(max_length=20, blank=False)
    street_name = models.CharField(max_length=255, blank=False)
    street_number = models.CharField(max_length=10, blank=False)
    phone = models.CharField(max_length=20, blank=False)
    image = models.ImageField(
        upload_to='restaurants/',
        blank=True,
        null=True,
        validators=[validate_1920x1080_image],
        help_text="Main restaurant image (16:9 PNG or JPG)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class OpeningHour(models.Model):
    DAYS_OF_WEEK = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='opening_hours'
    )
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    open_time = models.TimeField(blank=True, null=True)
    close_time = models.TimeField(blank=True, null=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('restaurant', 'day_of_week')
        ordering = ['day_of_week']

    def __str__(self):
        status = "Closed" if self.is_closed else f"{self.open_time} - {self.close_time}"
        return f"{self.restaurant.name} - {self.get_day_of_week_display()}: {status}"