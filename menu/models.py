from django.db import models
from restaurants.models import Restaurant
from .validators import validate_square_image

class MenuCategory(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='menu_categories'
    )
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('restaurant', 'name')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.restaurant.name})"

class MenuItem(models.Model):
    category = models.ForeignKey(
        MenuCategory,
        on_delete=models.CASCADE,
        related_name='menu_items'
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='menu_items/',
        blank=True,
        null=True,
        validators=[validate_square_image],
        help_text="Upload a square image (1:1) at least 600x600 px"
    )
    price = models.DecimalField(max_digits=6, decimal_places=2)
    allergens = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated allergens (e.g., nuts, gluten, dairy)"
    )
    calories = models.PositiveIntegerField(help_text="Calories per portion")
    protein = models.PositiveIntegerField(help_text="Protein (g)")
    carbs = models.PositiveIntegerField(help_text="Carbs (g)")
    fat = models.PositiveIntegerField(help_text="Fat (g)")
    available = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - £{self.price:.2f}"