from django.shortcuts import render , HttpResponse

# Create your views here.


def home(request):
    if request.user.is_authenticated:
        return HttpResponse(f"Logged in as {request.user.first_name} {request.user.last_name}")
    else:
        return render(request,"home.html")