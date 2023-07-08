from django.urls import path
from dev.views import *
urlpatterns = [
    path('',dev,name="dev" ),
]