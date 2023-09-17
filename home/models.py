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


def generate_profile_image_filename(instance, filename):
    # Get the current timestamp
    timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
    # Get the original file extension
    extension = os.path.splitext(filename)[1]
    # Generate the custom filename using the username and timestamp
    custom_filename = f"{instance.username}_{timestamp}{extension}"
    # Return the complete path where the file should be saved
    return os.path.join('users_profile/', custom_filename)

class events(models.Model):
    event_id = models.IntegerField(primary_key=True)
    title = models.TextField(max_length=1024)
    description = models.TextField(max_length=2048 , blank=True)
    venue = models.TextField(max_length=1024)
    mode = models.TextField(max_length=1024)
    start_dateandtime = models.DateTimeField(null=True, blank=True)
    end_dateandtime = models.DateTimeField(null=True, blank=True)
    imageurl = models.ImageField(upload_to=generate_filename)
    zoom_link = models.URLField(null=True, blank=True)
    whatsapp_group_link = models.URLField(null=True, blank=True)

   
 
class EventRegistration(models.Model):
    event_id = models.IntegerField()
    email = models.EmailField(max_length=1024)
    registered_datetime = models.DateTimeField(default=timezone.now)
    fullname = models.CharField(max_length=200)
    registration_no = models.CharField(max_length=20)
    study_year = models.CharField(max_length=3)
    campus = models.CharField(max_length=100)
    user_event_id = models.CharField(max_length=200, blank=True , null=True)
    


class UserDetails(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    STUDY_YEAR_CHOICES = (
        ('1', 'First Year'),
        ('2', 'Second Year'),
        ('3', 'Third Year'),
        ('4', 'Fourth Year'),
        ('5', 'Fifth Year'),
        ('6', 'sixth Year'),
    )
    
    CAMPUS_CHOICES = (
        ('VZG', 'VIZAG'),
        ('HYD' , 'HYDERABAD'),
        ('BLR' , 'BANGALORE'),
    )
    
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    registration_no = models.CharField(max_length=50)
    institute = models.CharField(max_length=100)
    branch = models.CharField(max_length=100)
    campus = models.CharField(max_length=30 , choices=CAMPUS_CHOICES)
    mobile = models.CharField(max_length=15) 
    study_year = models.CharField(max_length=1, choices=STUDY_YEAR_CHOICES)
    profile_image = models.ImageField(upload_to=generate_profile_image_filename, blank=True, null=True , default="https://img.freepik.com/premium-vector/anonymous-user-circle-icon-vector-illustration-flat-style-with-long-shadow_520826-1931.jpg?size=626&ext=jpg")
    bio = models.TextField(max_length=300, blank=True)
    instagram_link = models.URLField(max_length=200, blank=True)
    linkedin_link = models.URLField(max_length=200, blank=True)
    github_link = models.URLField(max_length=200, blank=True)
    tryhackme_link = models.URLField(max_length=200, blank=True)
    hackthebox_link = models.URLField(max_length=200, blank=True)
    discord_link = models.URLField(max_length=200 , blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
