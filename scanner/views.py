from datetime import datetime
from django.shortcuts import render , redirect , HttpResponse
from django.contrib import messages
from .models import *
from home.models import *
from .forms import qrcontent
# Create your views here.


def scan_home(request):
    if request.user.is_authenticated and scanning.objects.filter(email=request.user.email).exists():
        if request.method == 'GET':
            events = Event.objects.all().order_by('-event_date').values()
            return render(request, 'scanner_select_event.html' , { 'events' : events})
        elif request.method == 'POST':
            event_id = int(request.POST['event_id']) 
            return redirect('scan_event', event_id=event_id)
    else:
        messages.warning(request, 'You are not authorized')
        return redirect('home')
    
    
def scan_event(request, event_id):
    if request.user.is_authenticated and scanning.objects.filter(email=request.user.email).exists():
        if request.method == 'GET':
            data = {'registrar': request.user.first_name}
            form = qrcontent(data)
            admitted = len(student_status.objects.filter(status="IN"))
            out = len(student_status.objects.filter(status="OUT"))
            return render(request, 'scanner_scan.html', {
                'form': form,
                'admitted': admitted,
                'out': out
            })
        elif request.method == 'POST':
            qrcode = request.POST.get('qrtext')
            if EventRegistration.objects.filter(user_event_id=qrcode , event_id=event_id).exists():
                if student_status.objects.filter(user_eventid=qrcode,  event_id=event_id , status="OUT").exists():
                    student_status.objects.filter(user_eventid=qrcode,  event_id=event_id).update(status='IN')
                    ist = datetime.now()
                    todaydate = datetime.date(ist)
                    timenow = datetime.time(ist)
                    
                    userdata = student.objects.filter(user_eventid=qrcode,  event_id=event_id).values()[0]
                    entries_json = userdata['entries']
                    entries_json[f'IN_{len(entries_json)//2}'] = [str(timenow)[0:5] , todaydate ]
                    student.objects.filter(user_eventid=qrcode,  event_id=event_id).update(entries=entries_json)


                    entry = student_status.objects.filter(user_eventid=qrcode).values()
                    entry_update = entries(
                                        event_id = event_id,
                                        user_eventid=qrcode,
                                        email=entry[0]['email'],
                                        date=todaydate,
                                        time=timenow,
                                        verifiedby=request.user.first_name,
                                        status="IN")
                    entry_update.save()
                    messages.success(request, 'User In')
                    return redirect('scan_event', event_id=event_id)
                elif student_status.objects.filter(user_eventid=qrcode,  event_id=event_id , status="IN").exists():
                    entry = student_status.objects.filter(user_eventid=qrcode,  event_id=event_id ).values()
                    student_status.objects.filter(user_eventid=qrcode).update(status='OUT')
                    ist = datetime.now()
                    todaydate = datetime.date(ist)
                    timenow = datetime.time(ist)

                    userdata = student.objects.filter(user_eventid=qrcode).values()[0]
                    entries_json = userdata['entries']
                    entries_json[f'OUT_{len(entries_json)//2}'] = [str(timenow)[0:5] , todaydate ]
                    student.objects.filter(user_eventid=qrcode).update(entries=entries_json)

                    
                    entry_update = entries(user_eventid=qrcode,
                                        event_id = event_id,
                                        email=entry[0]['email'],
                                        date=todaydate,
                                        time=timenow,
                                        verifiedby=request.user.first_name,
                                        status="OUT")
                    entry_update.save()
                    messages.success(request, 'User OUT')
                    return redirect('scan_event', event_id=event_id)
                else:
                    user_event = EventRegistration.objects.get(user_event_id=qrcode)
                    fullname = user_event.fullname
                    user_eventid = qrcode
                    email = user_event.email
                    verifiedby = request.user.first_name
                    status = "IN"
                    
                    user = UserDetails.objects.get(email=email)

                    ist = datetime.now()
                    todaydate = datetime.date(ist)
                    timenow = datetime.time(ist)

                    useradd = student(
                        fullname = fullname,
                        email = email,
                        event_id = event_id,
                        user_eventid = user_eventid,
                        college = user.institute,
                        branch = user.branch,
                        year = user.study_year
                    )
                    useradd.save()
                    userdata = student.objects.filter(user_eventid=qrcode).values()[0]
                    entries_json = userdata['entries']
                    entries_json[f'IN_{len(entries_json)//2}'] = [str(timenow)[0:5] , todaydate ]
                    student.objects.filter(user_eventid=qrcode).update(entries=entries_json)

                    
                    entry_update = entries(
                                        event_id = event_id,
                                        user_eventid=user_eventid,
                                        email=email,
                                        date=todaydate,
                                        time=timenow,
                                        verifiedby=verifiedby,
                                        status="IN")
                    entry_update.save()
                    
                    status_update = student_status(
                    fullname=fullname,
                    user_eventid=user_eventid,
                    email=email,
                    event_id= event_id,
                    status=status)
                    status_update.save()
                    
                    messages.success(request, 'User In')
                    return redirect('scan_event', event_id=event_id)
                
            else:
                messages.success(request, 'User not valid')
                return redirect('scan_event', event_id=event_id)
    else:
        messages.warning(request, 'You are not authorized')
        return redirect('home')