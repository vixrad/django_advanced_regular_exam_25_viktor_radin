from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    is_owner = forms.BooleanField(required=False)
    company_number = forms.CharField(max_length=50, required=False)

    class Meta:
        model = User
        fields = ["email", "password1", "password2"]  # no is_owner/company_number in default Meta

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
            "placeholder": "Enter your email",
            "autofocus": "autofocus"
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your password"
        })
    )


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'is_owner', 'company_number']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'company_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'is_owner': 'Register as Restaurant Owner?',
            'company_number': 'Company Number',
        }

    def clean(self):
        cleaned_data = super().clean()
        is_owner = cleaned_data.get("is_owner")
        company_number = cleaned_data.get("company_number")

        if is_owner and not company_number:
            self.add_error("company_number", "Company number is required for restaurant owners.")
        return cleaned_data