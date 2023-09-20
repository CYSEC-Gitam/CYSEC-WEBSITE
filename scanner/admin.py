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
    
    
@admin.register(student_status)
class StudentStatusAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'event_id', 'email', 'status')
    list_filter = ('event_id', 'status')
    search_fields = ('fullname', 'email')

@admin.register(entries)
class EntriesAdmin(admin.ModelAdmin):
    list_display = ('event_id', 'email', 'date', 'time', 'verifiedby', 'status')
    list_filter = ('event_id', 'status', 'verifiedby')
    search_fields = ('email', 'verifiedby')

@admin.register(student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'email', 'event_id', 'college', 'branch', 'year', 'date')
    list_filter = ('event_id', 'college', 'branch', 'year')
    search_fields = ('fullname', 'email', 'college', 'branch', 'year')
    readonly_fields = ('entries',)