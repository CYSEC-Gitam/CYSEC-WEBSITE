from django.urls import path
from .views import *


urlpatterns = [
    path('', scan_home,name="scan_home" ),
]