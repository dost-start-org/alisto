from django.contrib import admin
from .models import Responder

class ResponderAdmin(admin.ModelAdmin):
    list_display = ('user', 'agency')
    list_filter = ('agency',)
    search_fields = ('user__email', 'agency__name')

admin.site.register(Responder, ResponderAdmin)
