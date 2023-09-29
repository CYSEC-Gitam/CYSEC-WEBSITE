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
from .upload import event_upload


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
        first_event = event.values()
        
        current_ctfs , past_ctfs , upcoming_ctfs = get_ctfs_feed(1, 0 ,1)
        ctfs = current_ctfs + upcoming_ctfs
        faqs = faq.objects.all().order_by('questionno').values()
        if request.user.is_authenticated:
            event_registrations = EventRegistration.objects.filter(email=request.user.email).values()
            registered = [i['event_id'] for i in event_registrations] 
            eventsubmissions = event_submission.objects.filter(email=request.user.email).values()
            submissions = [i['event_id'] for i in eventsubmissions] 
            if UserDetails.objects.filter(email=request.user.email).exists():
                return render(request,"home.html" , { 'events':first_event,'ctfs': ctfs,'faqs':faqs, 'registered':registered , 'submissions':submissions})
            else:
                return redirect("logout")
        else:
            return render(request,"home.html" ,  {  'events':first_event,'ctfs': ctfs,'faqs':faqs})


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


@login_required(login_url="/auth/login/google-oauth2/")
def register_event(request, event_id):
    if request.user.is_authenticated:
        if events.objects.filter(event_id=event_id).exists():
            if UserDetails.objects.filter(email=request.user.email).exists():
                user = UserDetails.objects.get(email=request.user.email)
                current_datetime = datetime.now()
                fullname = user.first_name + ' ' + user.last_name 
                
                user_event_id =  hashlib.md5(( str(event_id) + str(request.user.email) + str(fullname) + str(current_datetime)).encode())
                user_event_id = user_event_id.hexdigest()
                if not EventRegistration.objects.filter(email=request.user.email , event_id=event_id).exists():
                    if str(event_id) == "230920":
                        send_pass_mail(fullname, request.user.email, user_event_id)

                    EventRegistration.objects.get_or_create(event_id=event_id, email=user.email, registered_datetime = current_datetime,fullname=fullname, registration_no= user.registration_no , study_year=user.study_year,campus=user.campus, user_event_id=user_event_id)
                messages.success(request, 'Event registration successfully.')
                return redirect('home')
            else:
                return redirect('user_details')
        else:
            return redirect('home')
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


@login_required(login_url="/auth/login/google-oauth2/")
def eventsubmission(request, event_id):
    if request.user.is_authenticated:
        if events.objects.filter(event_id=event_id).exists():
            if request.method == 'GET':
                user_email = request.user.email
                eventid = event_id
                if events.objects.get(event_id=eventid).is_submission:
                    if EventRegistration.objects.filter(email=user_email, event_id=eventid).exists():
                        if not event_submission.objects.filter(email=user_email, event_id=eventid).exists():
                            event = events.objects.get(event_id=eventid)
                            return render(request,'event_submission.html', {'event': event})
                        else:
                            messages.success(request, 'You Already uploded the File')
                            return redirect('home')
                    else:
                        messages.success(request, 'Please Register for the event')
                        return redirect('home')
                else:
                    return redirect('home')
            elif request.method == 'POST':
                user_email = request.user.email
                eventid = event_id
                if events.objects.get(event_id=eventid).is_submission:
                    if EventRegistration.objects.filter(email=user_email, event_id=eventid).exists():
                        if not event_submission.objects.filter(email=user_email, event_id=eventid).exists():
                            upload = request.FILES.get('eventupload')
                            event  = events.objects.get(event_id=eventid)
                            user  =  UserDetails.objects.get(email=user_email)
                            timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
                            filename = f"{str(event.title).replace(' ','_')}_{str(user.first_name).replace(' ','_')}_{str(user.last_name).replace(' ','_')}__{timestamp}"
                            open(filename+'.pdf', 'wb').write(upload.file.read())
                            parentid = events.objects.get(event_id=eventid).submission_driveid
                            fileid = event_upload(filename, parentid)
                            eventsubmission = event_submission(
                                event_id = event_id,
                                email = user_email,
                                fullname = user.first_name + ' ' + user.last_name,
                                registration_no = user.registration_no,
                                study_year = user.study_year,
                                campus = user.campus,
                                user_submission_id = fileid,
                            )
                            eventsubmission.save()
                            os.remove(filename+'.pdf')
                            messages.success(request, 'File uploded succesfully')
                            return redirect('home')
                        else:
                            messages.success(request, 'You Already uploded the File')
                            return redirect('home')
                    else:
                        messages.success(request, 'Please Register for the event')
                        return redirect('home')
                else:
                    return redirect('home')
        else:
            return redirect('home')
    else:
        return redirect('login')


#below functions are added for testing purposes these functions are not part the website


def test(request):
    if request.method == 'GET':
        return render(request, 'event_submission.html')
    else:
        return render(request, 'event_submission.html')
    
    
    
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
    
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings


def send_pass_mail(name, email, qrhash):
  subject, from_email, to = f'{name},Your Ticket For CYSEC Moive Night', settings.EMAIL_HOST_USER, email
  html_content1 = get_template('event_confirmation_mail.html').render({'qrhash': qrhash})
  msg = EmailMultiAlternatives(subject, html_content1, from_email, [to])
  msg.content_subtype = "html"
  msg.send() 


def sendmails(eventid):
  for i in EventRegistration.objects.all():
    if (EventRegistration.objects.filter(email=i.email,event_id=eventid).exists()):
        user = EventRegistration.objects.get(email=i.email ,event_id=eventid)
        userd = UserDetails.objects.get(email=user.email)
        name = userd.first_name + ' ' + userd.last_name 
        qrhash = user.user_event_id
        mailid = user.email
        send_pass_mail(name,mailid,qrhash)
        print(f"{user.email} sent mail")
    else:
        print(f"{i.email} is not a member")


        
    
    
    
    
