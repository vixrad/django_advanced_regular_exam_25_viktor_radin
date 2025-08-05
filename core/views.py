from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm

def home(request):
    return render(request, 'core/home.html')

class AboutView(TemplateView):
    template_name = "core/about.html"

class ContactView(FormView):
    template_name = "core/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy('contact')

    def form_valid(self, form):
        name = form.cleaned_data["name"]
        email = form.cleaned_data["email"]
        message = form.cleaned_data["message"]

        send_mail(
            subject=f"Contact Form Message from {name}",
            message=f"From: {email}\n\nMessage:\n{message}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=False,
        )

        messages.success(
            self.request,
            f"""
            <strong>Your message has been sent successfully!</strong><br><br>
            <strong>Summary:</strong><br>
            <ul class="mb-0">
                <li><strong>Name:</strong> {name}</li>
                <li><strong>Email:</strong> {email}</li>
                <li><strong>Message:</strong> {message}</li>
            </ul>
            """
        )
        return super().form_valid(form)