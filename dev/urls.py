from django.urls import path
from dev.views import *
urlpatterns = [
    path('',home,name="home" ),
]