from django.urls import path
from home.views import *


urlpatterns = [
    path('',home,name="home" ),
    path('news',news,name="news"),
    path('test', test , name="test"),
    path('user_details' , user_details , name="user_details"),
    path('ctftime', ctfs_feed, name="ctftime"),
    path('register_event/<int:event_id>/', register_event, name='register_event'),
    path('login', login, name="login"),
]