from django.contrib import admin

# Register your models here.
# Auth/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('user_id', 'username', 'email', 'is_staff', 'is_active', 'is_artist')
    list_filter = ('is_staff', 'is_active', 'is_artist')
    search_fields = ('user_id', 'username', 'email')
    ordering = ('user_id',)
    
    fieldsets = (
        (None, {'fields': ('user_id', 'password')}),
        ('Personal info', {'fields': ('username', 'email', 'contact_number', 'brand_name', 'company_name', 'position')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_artist', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_id', 'username', 'email', 'contact_number', 'brand_name', 'company_name', 'position', 'password1', 'password2', 'is_staff', 'is_active', 'is_artist', 'groups', 'user_permissions'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
