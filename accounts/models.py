from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None  # remove default username
    email = models.EmailField(unique=True)
    is_owner = models.BooleanField(default=False)
    company_number = models.CharField(max_length=50, blank=True, null=True)
    strike_count = models.PositiveIntegerField(default=0)
    is_restricted = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # only email is required

    objects = UserManager()

    def add_strike(self):
        self.strike_count += 1
        if self.strike_count >= 3:
            self.is_restricted = True
        self.save()

    def reset_strikes(self):
        self.strike_count = 0
        self.is_restricted = False
        self.save()

    def __str__(self):
        return self.email