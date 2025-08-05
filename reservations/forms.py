from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.core.exceptions import ValidationError
from datetime import datetime, date, timedelta
from django.utils import timezone
from .models import Reservation, Review
from restaurants.models import OpeningHour
from core.utils import generate_available_time_slots

class ReservationForm(forms.ModelForm):
    reservation_date = forms.DateField(
        label="Reservation Date",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    reservation_time = forms.TimeField(
        label="Reservation Time",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Reservation
        fields = ['restaurant', 'reservation_date', 'reservation_time', 'number_of_people']
        widgets = {
            'number_of_people': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

    def __init__(self, *args, **kwargs):
        self.restaurant = kwargs.pop('restaurant', None)
        hide_restaurant = kwargs.pop('hide_restaurant', False)
        super().__init__(*args, **kwargs)

        if hide_restaurant:
            self.fields['restaurant'].widget = forms.HiddenInput()

        tomorrow = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
        self.fields['reservation_date'].widget.attrs['min'] = tomorrow
        self.fields['reservation_time'].widget.choices = []

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Reserve', css_class='btn btn-success w-100 mt-3'))

    def clean_reservation_date(self):
        reservation_date = self.cleaned_data.get("reservation_date")
        if reservation_date <= date.today():
            raise ValidationError("Reservations must be made for a future date (not today).")
        if reservation_date.year != date.today().year:
            raise ValidationError("Reservations can only be made within the current year.")
        return reservation_date

    def clean(self):
        cleaned_data = super().clean()
        reservation_date = cleaned_data.get("reservation_date")
        reservation_time = cleaned_data.get("reservation_time")
        restaurant = cleaned_data.get("restaurant") or self.restaurant

        if not reservation_date or not reservation_time or not restaurant:
            return cleaned_data

        reservation_datetime = datetime.combine(reservation_date, reservation_time)

        # Ensure timezone awareness
        if timezone.is_naive(reservation_datetime):
            reservation_datetime = timezone.make_aware(reservation_datetime)
        else:
            reservation_datetime = reservation_datetime.astimezone(timezone.get_current_timezone())

        weekday = reservation_datetime.weekday()
        opening = OpeningHour.objects.filter(restaurant=restaurant, day_of_week=weekday).first()
        if not opening or opening.is_closed:
            raise ValidationError("This restaurant is closed on the selected day.")

        valid_slots = generate_available_time_slots(opening.open_time, opening.close_time)
        if reservation_time not in valid_slots:
            raise ValidationError("Selected time is outside the restaurant's booking hours.")

        cleaned_data["reservation_time"] = reservation_datetime
        return cleaned_data


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit Review', css_class='btn btn-primary w-100 mt-3'))