from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class CertificateManager(models.Model):
	email = models.EmailField(unique=True)


class Event(models.Model):
	event_id = models.IntegerField(unique=True)
	event_name = models.CharField(max_length=250)
	event_date = models.DateTimeField(auto_now_add=True)
	parentfolderid = models.CharField(max_length=250)


class EventCertificate(models.Model):
	user = models.EmailField(null=True, blank=True)
	event_id = models.IntegerField()
	event_name = models.CharField(max_length=250)
	date = models.DateField(auto_now_add=True)
	data_file = models.FileField(upload_to="certificates/data_files/")
	template = models.FileField(upload_to="certificates/templates/")
	email_column = models.CharField(max_length=250, null=True, blank=True)
	subject = models.CharField(max_length=250, null=True)
	message = models.TextField(null=True, blank=True)
	slug = models.SlugField(null=True, blank=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.event_name)
		super(EventCertificate, self).save(*args, **kwargs)



class ParticipantCertificate(models.Model):
	event = models.CharField(max_length=250)
	eventid = models.CharField(max_length=250)
	email = models.EmailField(max_length=250)
	full_name = models.CharField(max_length=200,null=True, blank=True)
	reg_no = models.CharField(max_length=100,null=True, blank=True)
	certificatelink = models.URLField(max_length=200)
	certificatehash = models.CharField(max_length=150)
	certificateid = models.CharField(max_length=150)
	status = models.BooleanField(default=False)