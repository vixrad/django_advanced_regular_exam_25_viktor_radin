from django.contrib import admin
from .models import DeliveryAddress, Order, OrderItem

@admin.register(DeliveryAddress)
class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address_line1', 'city', 'postcode', 'created_at')
    search_fields = ('address_line1', 'city', 'postcode', 'user__username')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'restaurant', 'user', 'status', 'delivery_time', 'created_at')
    list_filter = ('status', 'restaurant', 'created_at')
    search_fields = ('user__username', 'restaurant__name')
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'menu_item', 'quantity')
    search_fields = ('order__id', 'menu_item__name')