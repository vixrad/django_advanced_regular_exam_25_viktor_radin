from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_owner = models.BooleanField(default=False)
    strike_count = models.PositiveIntegerField(default=0)
    is_restricted = models.BooleanField(default=False)

    def add_strike(self):
        """Increase strike count and check restriction."""
        self.strike_count += 1
        if self.strike_count >= 3:
            self.is_restricted = True
        self.save()

    def reset_strikes(self):
        """Reset strikes (optional admin action)."""
        self.strike_count = 0
        self.is_restricted = False
        self.save()

    def __str__(self):
        return self.username