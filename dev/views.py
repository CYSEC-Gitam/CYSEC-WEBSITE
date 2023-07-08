from django.shortcuts import render

# Create your views here.


def dev(request):
    return render(request,"dev.html")

