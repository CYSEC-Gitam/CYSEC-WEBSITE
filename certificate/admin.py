from django.contrib import admin
from .models import *


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_id', 'event_name', 'event_date', 'parentfolderid')
    list_filter = ('event_name', 'event_date')
    search_fields = ('event_name', 'parentfolderid')
    ordering = ('event_date',)


@admin.register(CertificateManager)
class CertificateManagerAdmin(admin.ModelAdmin):
    list_display = ('email',)