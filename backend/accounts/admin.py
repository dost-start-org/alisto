from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'authority_level', 'contact_number', 'status', 'email_verified')
    list_filter = ('authority_level', 'status', 'email_verified')
    search_fields = ('full_name', 'user__email', 'contact_number')

admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)