from django.shortcuts import render
from .models import *
# Create your views here.


def scan_home(request):
    if request.user.is_authenticated and scanning.objects.filter(email=request.user.email).exists():
        events = Event.objects.all().order_by('-event_date').values()
        return render(request, 'scanner_select_event.html' , { 'events' : events})
