from django import forms
from .models import MenuCategory, MenuItem
from .validators import validate_square_image

class MenuCategoryForm(forms.ModelForm):
    class Meta:
        model = MenuCategory
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category name'})
        }

class MenuItemForm(forms.ModelForm):
    image = forms.ImageField(
        required=False,
        validators=[validate_square_image],
        help_text="Upload a square image (1:1, at least 600x600 px)"
    )

    class Meta:
        model = MenuItem
        fields = [
            'name', 'description', 'image',
            'price', 'allergens', 'calories', 'protein', 'carbs', 'fat', 'available'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'allergens': forms.TextInput(attrs={'class': 'form-control'}),
            'calories': forms.NumberInput(attrs={'class': 'form-control'}),
            'protein': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'carbs': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'fat': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }