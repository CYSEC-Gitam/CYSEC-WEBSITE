from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *

class FaqAdmin(ImportExportModelAdmin):
    list_display = ('questionno','question', 'answer', 'hyperlinktext', 'hyperlink')
    search_fields = ('questionno','question', 'answer')
    list_sort = ('questionno',)  # Add more fields for filtering if needed
    list_per_page = 20  # Change the number of items displayed per page

    fieldsets = (
        (None, {
            'fields': ('questionno','question', 'answer')
        }),
        ('Hyperlink', {
            'fields': ('hyperlinktext', 'hyperlink'),
            'classes': ('collapse',),
        }),
    )

    # Optionally, you can add prepopulated fields for URLField using the following:
    # prepopulated_fields = {'hyperlinktext': ('hyperlink',)}

admin.site.register(faq, FaqAdmin)




class EventsAdmin(ImportExportModelAdmin):
    list_display = ('event_id', 'title', 'description', 'venue', 'mode', 'start_dateandtime', 'zoom_link', 'is_submission','submission_driveid')
    search_fields = ('title', 'venue', 'mode' , 'start_dateandtime')
    list_filter = ('start_dateandtime',)  # Add more fields for filtering if needed
    list_per_page = 20  # Change the number of items displayed per page

    fieldsets = (
        ('Event Details', {
            'fields': ('event_id', 'title', 'description', 'venue', 'mode', 'start_dateandtime', 'end_dateandtime', 'imageurl')
        }),
        ('Event links', {
            'fields': ('zoom_link' , 'whatsapp_group_link')
        }),
        ('Event Submission (if event need any submission)', {
            'fields': ('is_submission','submission_driveid')
        }),
    )

admin.site.register(events, EventsAdmin)



class UserDetailsAdmin(ImportExportModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'gender', 'study_year')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'registration_no', 'institute')
    list_filter = ('gender', 'study_year')
    list_per_page = 20

    fieldsets = (
        ('Personal Information', {
            'fields': ('username', 'first_name', 'last_name', 'email', 'date_of_birth', 'gender', 'profile_image', 'bio')
        }),
        ('Academic Information', {
            'fields': ('registration_no', 'institute', 'branch', 'campus', 'study_year')
        }),
        ('Social Media Links', {
            'fields': ('instagram_link', 'linkedin_link', 'github_link', 'tryhackme_link', 'hackthebox_link' , 'discord_link')
        }),
    )

admin.site.register(UserDetails, UserDetailsAdmin)




@admin.register(EventRegistration)
class EventRegistrationAdmin(ImportExportModelAdmin):
    list_display = ('event_id', 'email', 'registered_datetime', 'fullname', 'registration_no', 'study_year', 'campus', 'user_event_id')
    list_filter = ('event_id', 'registered_datetime','study_year', 'campus')
    search_fields = ('event_id','email', 'fullname', 'registration_no')
    date_hierarchy = 'registered_datetime'
    list_per_page = 50


@admin.register(event_submission)
class event_submissionAdmin(ImportExportModelAdmin):
    list_display = ('event_id', 'email', 'registered_datetime', 'fullname', 'registration_no', 'study_year', 'campus', 'user_submission_id')
    list_filter = ('event_id', 'registered_datetime','study_year', 'campus')
    search_fields = ('event_id','email', 'fullname', 'registration_no')
    date_hierarchy = 'registered_datetime'
    list_per_page = 50
