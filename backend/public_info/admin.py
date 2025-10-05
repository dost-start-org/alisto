from django.contrib import admin
from .models import EmergencyContact, ContactRedirection

admin.site.register(EmergencyContact)
admin.site.register(ContactRedirection)
