from django.db import models

# Create your models here.

class Event(models.Model):
	event_id = models.IntegerField(unique=True)
	event_name = models.CharField(max_length=250)
	event_date = models.DateTimeField(auto_now_add=True)
 
 
class scanning(models.Model):
    email = models.EmailField()
    
