from django.contrib import admin
from .models import Agency, AgencyEmergencyType

class AgencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'hotline_number', 'latitude', 'longitude')
    search_fields = ('name', 'hotline_number')

class AgencyEmergencyTypeAdmin(admin.ModelAdmin):
    list_display = ('agency', 'emergency_type')
    list_filter = ('agency', 'emergency_type')

admin.site.register(Agency, AgencyAdmin)
admin.site.register(AgencyEmergencyType, AgencyEmergencyTypeAdmin)
