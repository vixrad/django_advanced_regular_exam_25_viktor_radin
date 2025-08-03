from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Additional Info', {'fields': ('is_owner', 'company_number', 'strike_count', 'is_restricted')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_owner', 'company_number'),
        }),
    )

    list_display = ('email', 'is_owner', 'company_number', 'strike_count', 'is_restricted', 'is_staff')
    list_filter = ('is_owner', 'is_restricted', 'is_staff')
    search_fields = ('email',)
    ordering = ('email',)