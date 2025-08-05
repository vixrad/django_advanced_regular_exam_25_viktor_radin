from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db import DatabaseError
from restaurants.models import Restaurant
from .forms import CustomUserCreationForm, CustomLoginForm, ProfileEditForm

FULL_ADMIN_GROUP = "Full Admin"
STAFF_ADMIN_GROUP = "Staff Admin"

# assign user to the correct group based on is_owner flag
def assign_user_to_group(user):
    try:
        full_admin_group = Group.objects.filter(name=FULL_ADMIN_GROUP).first()
        staff_admin_group = Group.objects.filter(name=STAFF_ADMIN_GROUP).first()

        if not full_admin_group or not staff_admin_group:
            return False

        # remove old memberships and assign new
        user.groups.remove(full_admin_group, staff_admin_group)
        if user.is_owner:
            user.groups.add(full_admin_group)
        else:
            user.groups.add(staff_admin_group)
        return True

    except DatabaseError:
        return False

# user registration with group assignment
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.is_owner = form.cleaned_data.get("is_owner")
                user.company_number = (
                    form.cleaned_data.get("company_number") if user.is_owner else None
                )
                user.save()

                # assign to correct group
                if not assign_user_to_group(user):
                    messages.warning(
                        request,
                        "default groups not found. please run migrations and check signals."
                    )

                # auto login
                login(request, user)
                messages.success(request, "your account has been created and you are now logged in.")
                return redirect("profile")

            except DatabaseError:
                messages.error(request, "a database error occurred while creating your account.")
        else:
            messages.error(request, "please correct the errors below and try again.")
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})

# custom login view
class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = CustomLoginForm

# user profile view
@login_required
def profile(request):
    try:
        restaurants = (
            Restaurant.objects.filter(owner=request.user)
            if request.user.is_owner or request.user.is_superuser
            else []
        )
    except DatabaseError:
        messages.error(request, "unable to fetch your restaurants at the moment.")
        restaurants = []

    return render(request, "accounts/profile.html", {"restaurants": restaurants})

# edit user profile and update group membership
@login_required
def edit_profile(request):
    user = request.user
    if request.method == "POST":
        form = ProfileEditForm(request.POST, instance=user)
        if form.is_valid():
            try:
                user = form.save()

                # assign to correct group
                if not assign_user_to_group(user):
                    messages.warning(
                        request,
                        "default groups not found. please run migrations and check signals."
                    )

                messages.success(request, "your profile has been updated.")
                return redirect("profile")

            except DatabaseError:
                messages.error(request, "an error occurred while updating your profile.")
        else:
            messages.error(request, "please correct the errors below and try again.")
    else:
        form = ProfileEditForm(instance=user)
    return render(request, "accounts/edit_profile.html", {"form": form})