from django.contrib import admin
from .models import EmergencyType, EmergencyReport, EmergencyVerification, UserEvaluation

class EmergencyTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_type')
    search_fields = ('name',)

class EmergencyReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'emergency_type', 'user', 'verification_status', 'status', 'date_created')
    list_filter = ('emergency_type', 'verification_status', 'status')
    search_fields = ('id', 'user__email', 'details')
    date_hierarchy = 'date_created'

class EmergencyVerificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'report', 'user', 'vote', 'date_created')
    list_filter = ('vote',)
    search_fields = ('report__id', 'user__email', 'details')
    date_hierarchy = 'date_created'

class UserEvaluationAdmin(admin.ModelAdmin):
    list_display = ('id', 'report', 'user', 'stars', 'did_app_guide_clearly', 'completion_speed')
    list_filter = ('stars', 'did_app_guide_clearly', 'completion_speed', 'confidence_level')
    search_fields = ('report__id', 'user__email', 'improvement_suggestion')
    date_hierarchy = 'date_created'

admin.site.register(EmergencyType, EmergencyTypeAdmin)
admin.site.register(EmergencyReport, EmergencyReportAdmin)
admin.site.register(EmergencyVerification, EmergencyVerificationAdmin)
admin.site.register(UserEvaluation, UserEvaluationAdmin)
