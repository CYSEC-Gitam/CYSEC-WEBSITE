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
    
    
class ParticipantCertificateAdmin(admin.ModelAdmin):
    list_display = ('event', 'email', 'full_name', 'status')
    list_filter = ('event', 'status')
    search_fields = ('email', 'full_name', 'eventid', 'reg_no')
    list_per_page = 20  # Number of items displayed per page in the admin list view

admin.site.register(ParticipantCertificate, ParticipantCertificateAdmin)