from django.shortcuts import render
from django.views.generic import TemplateView

def home(request):
    return render(request, 'core/home.html')

class ContactView(TemplateView):
    template_name = "core/contact.html"

class AboutView(TemplateView):
    template_name = "core/about.html"