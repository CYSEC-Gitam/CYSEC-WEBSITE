from django.urls import path
from .views import *


urlpatterns = [
    path('', scan_home, name="scan_home"),
    path('scan_event/<int:event_id>/', scan_event, name='scan_event'),
]