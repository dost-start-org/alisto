from django.contrib import admin
from .models import EmergencyContact, ContactRedirection

class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_number', 'type')
    list_filter = ('type',)
    search_fields = ('name', 'contact_number', 'description')

class ContactRedirectionAdmin(admin.ModelAdmin):
    list_display = ('contact', 'emergency_type')
    list_filter = ('emergency_type',)
    search_fields = ('contact__name', 'emergency_type__name')

admin.site.register(EmergencyContact, EmergencyContactAdmin)
admin.site.register(ContactRedirection, ContactRedirectionAdmin)
