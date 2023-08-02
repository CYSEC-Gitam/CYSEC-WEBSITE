from django.db import models
import os
# Create your models here.
from django.utils import timezone


class faq(models.Model):
    questionno = models.IntegerField(unique=True)
    question = models.TextField(max_length=1024)
    answer = models.TextField(max_length=1024)
    hyperlinktext = models.TextField(max_length=1024,null=True, blank=True)
    hyperlink = models.URLField(max_length=1024,null=True, blank=True)


   


def generate_filename(instance, filename):
    # Get the current timestamp
    timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
    # Get the original file extension
    extension = os.path.splitext(filename)[1]
    # Generate the custom filename using event_id and title
    custom_filename = f"{instance.event_id}_{instance.title.replace(' ', '_')}_{timestamp}{extension}"
    # Return the complete path where the file should be saved
    return os.path.join('events/', custom_filename)

class events(models.Model):
    event_id = models.IntegerField(primary_key=True)
    title = models.TextField(max_length=1024)
    description = models.TextField(max_length=2048)
    venue = models.TextField(max_length=1024)
    mode = models.TextField(max_length=1024)
    dateandtime = models.DateTimeField()
    imageurl = models.ImageField(upload_to=generate_filename)
    link = models.URLField(null=True, blank=True)
    
 