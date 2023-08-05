from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import faq , events

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
    list_display = ('event_id', 'title', 'description', 'venue', 'mode', 'dateandtime', 'link')
    search_fields = ('title', 'venue', 'mode')
    list_filter = ('dateandtime',)  # Add more fields for filtering if needed
    list_per_page = 20  # Change the number of items displayed per page

    fieldsets = (
        (None, {
            'fields': ('event_id', 'title', 'description', 'venue', 'mode', 'dateandtime', 'imageurl', 'link')
        }),
    )

admin.site.register(events, EventsAdmin)



from django.contrib import admin
from .models import UserDetails

class UserDetailsAdmin(admin.ModelAdmin):
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

