from django.shortcuts import get_object_or_404, render , redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
import feedparser
from .forms import UserDetailsForm
from .models import *
# Create your views here.
from datetime import datetime
import pytz
from django.contrib.auth.decorators import login_required
import hashlib


#### this function is for converting utc time to ctf time of ctfs from ctftime.org 
def convert_utc_to_ist(utc_datetime_str):
    try:
        # Parse the date and time strings as UTC
        utc_datetime = datetime.strptime(utc_datetime_str, "%Y%m%dT%H%M%S").replace(tzinfo=pytz.UTC)
        # Convert to IST timezone
        ist_timezone = pytz.timezone('Asia/Kolkata')
        ist_datetime = utc_datetime.astimezone(ist_timezone)
        # Formatting the datetime into a more readable format
        formatted_datetime = ist_datetime.strftime("%b %d, %Y, %I:%M %p")
        return formatted_datetime
    except Exception as e:
        print("Error:", e)
        return None



def get_ctfs_feed(c , p , u):
    def ctf_feed(rss):
        feed = feedparser.parse(rss)
        entries = feed.entries
        ctfs = []
        for data in entries:
            ctf = {}
            ctf['title'] = data['title']
            ctf['event_url'] = data['link']
            ctf['start_date'] =convert_utc_to_ist( data['start_date'] )
            ctf['finish_date'] = convert_utc_to_ist( data['finish_date'])
            ctf['format_text'] = data['format_text']
            ctf['organizers'] = data['organizers']
            ctf['rating_weight'] = float(data['weight'])
            ctf['logo_url'] = data['logo_url']
            ctfs.append(ctf)
        return ctfs
    
    upcoming_ctfs_feed = 'https://feeds.feedburner.com/ctftime/upcoming'
    current_ctfs_feed = 'https://feeds.feedburner.com/ctftime/current'
    past_ctfs_feed = 'https://feeds.feedburner.com/ctftime/past'
    upcoming_ctfs = []
    current_ctfs = []
    past_ctfs = []

    if c :
        current_ctfs = ctf_feed(current_ctfs_feed)
    if p:
        past_ctfs = ctf_feed(past_ctfs_feed)
    if u:
        upcoming_ctfs = ctf_feed(upcoming_ctfs_feed)
        
    return current_ctfs , past_ctfs , upcoming_ctfs



def home(request):
    if request.method == 'GET':
        current_datetime = datetime.now()
        event = events.objects.filter(end_dateandtime__gte=current_datetime).order_by('end_dateandtime')
        first_event = event.values().first() 
        
        current_ctfs , past_ctfs , upcoming_ctfs = get_ctfs_feed(1, 0 ,1)
        ctfs = current_ctfs + upcoming_ctfs
        faqs = faq.objects.all().order_by('questionno').values()
        if request.user.is_authenticated:
            event_registrations = EventRegistration.objects.filter(email=request.user.email).values()
            registered = [i['event_id'] for i in event_registrations] 
            
            if UserDetails.objects.filter(email=request.user.email).exists():
                return render(request,"home.html" , { 'event':first_event,'ctfs': ctfs,'faqs':faqs, 'registered':registered})
            else:
                return redirect("logout")
        else:
            return render(request,"home.html" ,  {  'event':first_event,'ctfs': ctfs,'faqs':faqs})


@login_required       
def user_details(request):
    if request.user.is_authenticated:
        if UserDetails.objects.filter(email=request.user.email).exists():
            return redirect('home')
        else:
            if request.method == 'POST':
                form = UserDetailsForm(request.POST, request.FILES )
                if form.is_valid():
                    form.save()
                    return redirect('home')
            else:
                initial_data = {'email': request.user.email}
                form = UserDetailsForm(initial=initial_data)
                
            return render(request, 'user_details2.html', {'form': form})
    else:
        return redirect('home')
    
    
    
def login(request):
    messages.success(request, 'Please Login to continue')
    return redirect('home')

def register_event(request, event_id):
    if request.user.is_authenticated:
        if UserDetails.objects.filter(email=request.user.email).exists():
            user = UserDetails.objects.get(email=request.user.email)
            current_datetime = datetime.now()
            fullname = user.first_name + ' ' + user.last_name 
            
            user_event_id =  hashlib.md5(( str(event_id) + str(request.user.email) + str(fullname) + str(current_datetime)).encode())
            user_event_id = user_event_id.hexdigest()
            
            EventRegistration.objects.get_or_create(event_id=event_id, email=user.email, registered_datetime = current_datetime,fullname=fullname, registration_no= user.registration_no , study_year=user.study_year,campus=user.campus , user_event_id =user_event_id)
            messages.success(request, 'Event registration successfully.')
            return redirect('home')
        else:
            return redirect('user_details')
    else:
        return redirect('home')

  
def news(request):
    feed = feedparser.parse("https://feeds.feedburner.com/TheHackersNews")
    entries = feed.entries
    # https://simpleisbetterthancomplex.com/tutorial/2016/08/03/how-to-paginate-with-django.html
    paginator = Paginator(entries, 8)
    page = request.GET.get('page', 1)
    try:
        post_pagin = paginator.page(page)
    except PageNotAnInteger:
        post_pagin = paginator.page(1)
    except EmptyPage:
        post_pagin = paginator.page(paginator.num_pages)
    for entry in post_pagin:
        if entry.links[1]['url']:
            entry['thumbnail'] =  entry.links[1]['url']
        else:
            entry['thumbnail'] = "https://e7.pngegg.com/pngimages/209/93/png-clipart-newspaper-journalism-android-android-news-online-newspaper.png"
    context = {"post_pagin":post_pagin}
    return render(request, 'news.html', context)








def ctfs_feed(request):
    current_ctfs , past_ctfs , upcoming_ctfs = get_ctfs_feed(1,1,1)
    return render(request , 'ctfs.html' , {'current_ctfs' : current_ctfs , 'past_ctfs' : past_ctfs , 'upcoming_ctfs' : upcoming_ctfs})






#below functions are added for testing purposes these functions are not part the website


def test(request):
    if request.method == 'GETe':
        events_list = events.objects.all().values()[0]
        print(events_list)
        return render(request, 'test2.html', {'event':events_list})
    else:
        regno = '122010324054'
        user = UserDetails.objects.filter(registration_no=regno).values()
        ids = []
        for i in user:
            ids.append(i['email'])
        return render(request, 'test2.html' , {'user':ids , 'reg':'jerryshravan@gmail.com'})
    
    
def qrfill():
  for i in EventRegistration.objects.all():
    if (EventRegistration.objects.filter(email=i.email).exists()):
      user = EventRegistration.objects.get(email=i.email)
      user_event_id = hashlib.md5((str(user.email) + str(user.registered_datetime) + str(user.event_id)).encode())
      user.user_event_id = user_event_id.hexdigest()
      user.save()
      print(f"{i.email} : done")
    else:
      print(f"{i.email} : incomplete")
    




        
    
    
    
    
