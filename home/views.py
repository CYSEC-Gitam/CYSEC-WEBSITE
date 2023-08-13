from django.shortcuts import render , redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
import feedparser
from .forms import UserDetailsForm
from .models import *
# Create your views here.
from datetime import datetime
import pytz
from django.contrib.auth.decorators import login_required



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



def get_ctfs_feed():


    upcoming_ctfs_feed = feedparser.parse('https://feeds.feedburner.com/ctftime/upcoming')
    current_ctfs_feed = feedparser.parse('https://feeds.feedburner.com/ctftime/current')
    past_ctfs_feed = feedparser.parse('https://feeds.feedburner.com/ctftime/past')
    upcoming_entries = upcoming_ctfs_feed.entries
    current_entries = current_ctfs_feed.entries
    past_entries = past_ctfs_feed.entries
    upcoming_ctfs = []
    current_ctfs = []
    past_ctfs = []
    for data in upcoming_entries:
        ctf = {}
        ctf['title'] = data['title']
        ctf['event_url'] = data['link']
        ctf['start_date'] =convert_utc_to_ist( data['start_date'] )
        ctf['finish_date'] = convert_utc_to_ist( data['finish_date'])
        ctf['format_text'] = data['format_text']
        ctf['organizers'] = data['organizers']
        ctf['rating_weight'] = float(data['weight'])
        ctf['logo_url'] = data['logo_url']
        upcoming_ctfs.append(ctf)

    
    for data in current_entries:
        ctf = {}
        ctf['title'] = data['title']
        ctf['event_url'] = data['link']
        ctf['start_date'] =convert_utc_to_ist( data['start_date'] )
        ctf['finish_date'] = convert_utc_to_ist( data['finish_date'])
        ctf['format_text'] = data['format_text']
        ctf['organizers'] = data['organizers']
        ctf['rating_weight'] = float(data['weight'])
        ctf['logo_url'] = data['logo_url']
        current_ctfs.append(ctf)
        
    for data in past_entries:
        ctf = {}
        ctf['title'] = data['title']
        ctf['event_url'] = data['link']
        ctf['start_date'] =convert_utc_to_ist( data['start_date'] )
        ctf['finish_date'] = convert_utc_to_ist( data['finish_date'])
        ctf['format_text'] = data['format_text']
        ctf['organizers'] = data['organizers']
        ctf['rating_weight'] = float(data['weight'])
        ctf['logo_url'] =  data['logo_url']
        past_ctfs.append(ctf)
    return current_ctfs , past_ctfs , upcoming_ctfs



def home(request):
    if request.method == 'GET':
        faqs = faq.objects.all().order_by('questionno').values()
        current_ctfs , past_ctfs , upcoming_ctfs = get_ctfs_feed()
        ctfs = current_ctfs + upcoming_ctfs
        if request.user.is_authenticated:
            return render(request,"home.html" , { 'ctfs': ctfs,'faqs':faqs})
        else:
            return render(request,"home.html" ,  { 'ctfs': ctfs,'faqs':faqs})


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
                
            return render(request, 'user_details.html', {'form': form})
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
    current_ctfs , past_ctfs , upcoming_ctfs = get_ctfs_feed()
    return render(request , 'ctfs.html' , {'current_ctfs' : current_ctfs , 'past_ctfs' : past_ctfs , 'upcoming_ctfs' : upcoming_ctfs})









def test(request):
    if request.method == 'GETe':
        events_list = events.objects.all().values()[0]
        print(events_list)
        return render(request, 'test.html', {'event':events_list})
    else:

        return render(request, 'test2.html')
    




        
    
    
    
    
