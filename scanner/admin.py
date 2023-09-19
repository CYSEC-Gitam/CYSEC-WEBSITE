from django.contrib import admin

# Register your models here.
from .models import *

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_id', 'event_name', 'event_date')
    search_fields = ('event_name', )
    list_filter = ('event_date', )

@admin.register(scanning)
class ScanningAdmin(admin.ModelAdmin):
    list_display = ('email',)
    search_fields = ('email',)