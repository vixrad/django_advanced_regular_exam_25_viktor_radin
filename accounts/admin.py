from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('is_owner', 'strike_count', 'is_restricted')}),
    )
    list_display = ('username', 'email', 'is_owner', 'strike_count', 'is_restricted', 'is_staff')
    list_filter = ('is_owner', 'is_restricted', 'is_staff')
    search_fields = ('username', 'email')