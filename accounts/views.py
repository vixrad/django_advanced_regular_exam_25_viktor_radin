from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, CustomLoginForm
import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_GET

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_owner = form.cleaned_data.get("is_owner")
            user.company_number = form.cleaned_data.get("company_number") if user.is_owner else None
            user.save()
            messages.success(request, "Your account has been created. You can now log in.")
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})


class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = CustomLoginForm

@require_GET
def company_lookup(request, company_number):
    url = f"https://api.company-information.service.gov.uk/company/{company_number}"
    response = requests.get(url, auth=(settings.COMPANIES_HOUSE_API_KEY, ""))

    if response.status_code == 200:
        data = response.json()
        address = ", ".join(filter(None, [
            data.get("registered_office_address", {}).get("address_line_1"),
            data.get("registered_office_address", {}).get("address_line_2"),
            data.get("registered_office_address", {}).get("locality"),
            data.get("registered_office_address", {}).get("postal_code")
        ]))
        return JsonResponse({
            "company_name": data.get("company_name", ""),
            "registered_office_address": address
        })
    return JsonResponse({"error": "Company not found"}, status=response.status_code)