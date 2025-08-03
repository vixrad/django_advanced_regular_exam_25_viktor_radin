from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    is_owner = forms.BooleanField(required=False, label="Register as Restaurant Owner?")
    company_number = forms.CharField(max_length=50, required=False, label="Company Number")

    class Meta:
        model = User
        fields = ["email", "password1", "password2", "is_owner", "company_number"]

    def clean(self):
        cleaned_data = super().clean()
        is_owner = cleaned_data.get("is_owner")
        company_number = cleaned_data.get("company_number")

        if is_owner and not company_number:
            self.add_error("company_number", "Company number is required for restaurant owners.")

        return cleaned_data

class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your email"
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your password"
        })
    )