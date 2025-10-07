from django.contrib import admin
from .models import EmergencyType, EmergencyReport, EmergencyVerification, UserEvaluation

admin.site.register(EmergencyType)
admin.site.register(EmergencyReport)
admin.site.register(EmergencyVerification)
admin.site.register(UserEvaluation)
