from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from restaurants.models import Restaurant
from .forms import CustomUserCreationForm, CustomLoginForm, ProfileEditForm

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_owner = form.cleaned_data.get("is_owner")
            user.company_number = form.cleaned_data.get("company_number") if user.is_owner else None
            user.save()

            # Auto login
            login(request, user)
            messages.success(request, "Your account has been created and you are now logged in.")
            return redirect("profile")
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})


class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = CustomLoginForm


@login_required
def profile(request):
    restaurants = []
    if request.user.is_owner or request.user.is_superuser:
        restaurants = Restaurant.objects.filter(owner=request.user)
    return render(request, 'accounts/profile.html', {"restaurants": restaurants})


@login_required
def edit_profile(request):
    user = request.user
    if request.method == "POST":
        form = ProfileEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect("profile")
    else:
        form = ProfileEditForm(instance=user)
    return render(request, "accounts/edit_profile.html", {"form": form})