from django.db import models
from django.contrib.auth.models import User
#from django.utils import timezone
from datetime import datetime 


class Venue(models.Model):
	name =models.CharField('Venue Name', max_length=120)
	address = models.CharField(max_length=300)
	zip_code = models.CharField('Zip Code',max_length=20)
	phone = models.CharField('Contact Number', max_length=20,blank=True)
	web = models.URLField('Website Address', blank=True)
	email_address = models.EmailField('Email', blank=True)

	def __str__(self):
		return self.name

class MultiStep(models.Model):
	event_title = models.CharField('Event Title', max_length=30, null=True)
	category = models.CharField('Category', max_length=30,default='SOME STRING', null=True)
	description = models.CharField('Description', max_length=200, null=True)
	event_type = models.CharField('Free/Fee', max_length=20,null=True)
	#min_age = models.IntegerField('Minimum Age',null=True)
	ath_min_age = models.CharField(null=True,max_length=20)
	ath_max_age = models.CharField(null=True, max_length=20)
	sup_min_age = models.CharField(null=True, max_length=20)
	sup_max_age = models.CharField(null=True,max_length=20)
	event_time = models.CharField('Event Time', max_length=20,null=True)
	event_date = models.CharField(blank=True, max_length=20,null=True)	#venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
	venue = models.CharField('Venue', blank=True, null=True, max_length=30)
	street = models.CharField('Street', max_length=30,blank=True,null=True)
	city = models.CharField('City', max_length=30,blank=True,null=True)
	province = models.CharField('Province', max_length=30,blank=True,null=True)
	country = models.CharField('Country', max_length=30,blank=True,null=True)
	zip_code = models.CharField('Zip Code', max_length=30,blank=True,null=True)
	staff_level = models.CharField('Staff Level', max_length=30, blank=True,null=True)
	athelete_level = models.CharField('Athelete Level', max_length=30, blank=True,null=True)



	def __str__(self):
		return self.event_title

class MyEventUser(models.Model):
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	email = models.EmailField('User Email')

	def __str__(self):
		return self.first_name #+ ' ' + self.last_name

class Event(models.Model):
	name = models.CharField('Event Name', max_length=120)
	venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
	event_date = models.DateTimeField('Event Date')
	category = models.CharField('Category',max_length=20,blank=True)
	#venue = models.CharField(max_length=120)
	#manager = models.CharField(max_length=60)
	manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
	description = models.TextField(blank=True)
	attendees = models.ManyToManyField(MyEventUser, blank=True)

	def __str__(self):
		return self.name

class MultiStepFormModel(models.Model):
	event_name = models.CharField('Event Name', max_length=120)
	event_date = models.DateTimeField('Event Date', max_length=120)
	description = models.CharField('description', max_length=120)
	category = models.CharField('category', max_length=120)
	manager = models.CharField('manager', max_length=120)
	phone = models.CharField('phone', max_length=120)
	email = models.EmailField('email', blank=True)
	website = models.URLField('Website', blank=True)

	def __str__(self):
		return self.name


