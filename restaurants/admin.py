from django.contrib import admin
from .models import Restaurant, OpeningHour

class OpeningHourInline(admin.TabularInline):
    model = OpeningHour
    extra = 1

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'phone', 'city', 'postal_code', 'street_name', 'street_number')
    search_fields = ('name', 'city', 'postal_code', 'street_name', 'street_number', 'phone')
    inlines = [OpeningHourInline]
    fieldsets = (
        (None, {
            'fields': (
                'owner', 'name', 'description', 'phone', 'image',
                'city', 'postal_code', 'street_name', 'street_number'
            )
        }),
    )