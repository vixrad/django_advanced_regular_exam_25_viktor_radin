from django.contrib import admin
from .models import Restaurant, OpeningHour, RestaurantImage

class OpeningHourInline(admin.TabularInline):
    model = OpeningHour
    extra = 1

class RestaurantImageInline(admin.TabularInline):
    model = RestaurantImage
    extra = 1

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'phone', 'offers_delivery', 'free_delivery', 'delivery_fee')
    list_filter = ('offers_delivery', 'free_delivery')
    search_fields = ('name', 'address', 'phone')
    inlines = [OpeningHourInline, RestaurantImageInline]
    fieldsets = (
        (None, {
            'fields': ('owner', 'name', 'description', 'address', 'phone')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude')
        }),
        ('Delivery Options', {
            'fields': ('offers_delivery', 'free_delivery', 'delivery_fee')
        }),
    )