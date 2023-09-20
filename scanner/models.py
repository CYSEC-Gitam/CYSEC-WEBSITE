from django.db import models
import jsonfield
from django.utils import timezone
# Create your models here.

class Event(models.Model):
	event_id = models.IntegerField(unique=True)
	event_name = models.CharField(max_length=250)
	event_date = models.DateTimeField(auto_now_add=True)
 
 
class scanning(models.Model):
    email = models.EmailField()
    

class student_status(models.Model):
  fullname = models.CharField(max_length=200, null=True, blank=True)
  user_eventid = models.CharField(max_length=200, null=True, blank=True)
  event_id = models.IntegerField()
  email = models.EmailField(max_length=200)
  status = models.CharField(max_length=200)


class entries(models.Model):
    event_id = models.IntegerField()
    email = models.CharField(max_length=100)
    user_eventid = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    verifiedby = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=200 , null=True)
  
  

class student(models.Model):
  fullname = models.CharField(max_length=228)
  email = models.CharField(max_length=228)
  event_id = models.IntegerField()
  user_eventid = models.CharField(max_length=200)
  college = models.CharField(max_length=228)
  branch = models.CharField(max_length=228)
  year = models.CharField(max_length=228)
  date = models.DateTimeField(default=timezone.now)
  entries = jsonfield.JSONField(default={})