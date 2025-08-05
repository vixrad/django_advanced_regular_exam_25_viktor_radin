from django import forms
from .models import Restaurant, OpeningHour
from .validators import validate_1920x1080_image

class RestaurantForm(forms.ModelForm):
    image = forms.ImageField(
        required=False,
        validators=[validate_1920x1080_image],
        help_text="Upload a JPG or PNG image with a 16:9 aspect ratio."
    )

    class Meta:
        model = Restaurant
        fields = [
            'name', 'description', 'city', 'postal_code',
            'street_name', 'street_number', 'phone', 'image'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'street_name': forms.TextInput(attrs={'class': 'form-control'}),
            'street_number': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

class OpeningHourForm(forms.ModelForm):
    class Meta:
        model = OpeningHour
        fields = ['day_of_week', 'open_time', 'close_time', 'is_closed']
        widgets = {
            'open_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'close_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'is_closed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        is_closed = cleaned_data.get("is_closed")
        open_time = cleaned_data.get("open_time")
        close_time = cleaned_data.get("close_time")

        if not is_closed and (not open_time or not close_time):
            raise forms.ValidationError("Specify both opening and closing times or mark as closed.")
        return cleaned_data