from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_id', 'event_name', 'event_date', 'parentfolderid')
    list_filter = ('event_name', 'event_date')
    search_fields = ('event_name', 'parentfolderid')
    ordering = ('event_date',)


@admin.register(CertificateManager)
class CertificateManagerAdmin(admin.ModelAdmin):
    list_display = ('email',)
    

@admin.register(ParticipantCertificate)   
class ParticipantCertificateAdmin(ImportExportModelAdmin):
    list_display = ('id','event','eventid', 'email', 'full_name', 'status')
    list_filter = ('event', 'status')
    search_fields = ('email', 'full_name', 'eventid', 'reg_no')
    list_per_page = 100  # Number of items displayed per page in the admin list view



@admin.register(EventCertificate)
class EventCertificateAdmin(ImportExportModelAdmin):
    list_display = ('id','event_name', 'date', 'user', 'event_id', 'slug')
    search_fields = ('event_name', 'user')
    # prepopulated_fields = {'slug': ('event_name',)}
    # readonly_fields = ('slug', 'date')

    fieldsets = (
        ('Event Information', {
            'fields': ('event_name', 'event_id','slug')
        }),
        ('User Information', {
            'fields': ('user', 'email_column')
        }),
        ('Email Configuration', {
            'fields': ('subject', 'message')
        }),
        ('Files', {
            'fields': ('data_file', 'template')
        }),
    )

