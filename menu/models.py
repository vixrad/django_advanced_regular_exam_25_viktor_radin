from django.db import models
from restaurants.models import Restaurant

class MenuCategory(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='categories'
    )
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('restaurant', 'name')

    def __str__(self):
        return f"{self.name} ({self.restaurant.name})"


class MenuItem(models.Model):
    category = models.ForeignKey(
        MenuCategory,
        on_delete=models.CASCADE,
        related_name='items'
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    allergens = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated list of allergens (e.g., nuts, gluten, dairy)"
    )
    calories = models.PositiveIntegerField(blank=True, null=True, help_text="Calories per portion")
    protein = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Protein (g)")
    carbs = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Carbs (g)")
    fat = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Fat (g)")

    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - £{self.price}"