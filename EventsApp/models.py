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


# class Sport_type(models.Model):
# 	category = models.ForeignKey(MultiStep, on_delete=models.CASCADE)
# 	name = models.CharField(max_length=30)

# 	def __str__(self):
# 		return self.name

# class Position(models.Model):
# 	sport_type = models.ForeignKey(Sport_type , on_delete=models.SET_NULL, null=True)
# 	name = models.CharField(max_length=30)

# 	def __str__(self):
# 		return self.name

# class Skill(models.Model):
# 	name = models.CharField(max_length=30)
# 	price = models.IntegerField()
# 	skill = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)

# 	def __str__(self):
# 		return self.name

# class SportCategory(models.Model):
	

# 	def __str__(self):
# 		return self.name

class MultiStep(models.Model):
	event_title = models.CharField('Event Title', max_length=30, null=True)
	description = models.CharField('Description', max_length=200, null=True)
	event_type = models.IntegerField('Event Type',blank=True,null=True)
	#min_age = models.IntegerField('Minimum Age',null=True)
	#sport_name = models.CharField('Sport Category', max_length=30, blank=True)
	event_time = models.CharField('Event Time', max_length=20,null=True)
	event_date = models.DateField('Event Date', blank=True, null=True)	#venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
	venue = models.CharField('Venue', blank=True, null=True, max_length=30)
	street = models.CharField('Street', max_length=30,blank=True,null=True)
	city = models.CharField('City', max_length=30,blank=True,null=True)
	province = models.CharField('Province', max_length=30,blank=True,null=True)
	country = models.CharField('Country', max_length=30,blank=True,null=True)
	zip_code = models.CharField('Zip Code', max_length=30,blank=True,null=True)
	sport_category = models.CharField('Sport Category', max_length=30,null=True)
	sport_type = models.CharField('Sport Type', max_length=30,null=True)
	position = models.CharField('Position', max_length=30, null=True)
	skill = models.CharField('Skill Level', max_length=30, null=True)
	position_price = models.IntegerField('Position Price', blank=True,null= True)
	min_age = models.IntegerField('Minimum Age',blank=True,null=True)
	max_age = models.IntegerField('Maximum Age', blank=True,null=True)
	#name = models.CharField(max_length=30)
	# category = models.ForeignKey(MultiStep, on_delete=models.SET_NULL, null=True)
	# sport_type = models.ForeignKey(Sport_type, on_delete=models.SET_NULL, null=True)
	# skill = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)
	# age_range = models.IntegerField()
	
	def __str__(self):
		return self.event_title



# class Country(models.Model):
#     name = models.CharField(max_length=40)

#     def __str__(self):
#         return self.name

# class City(models.Model):
#     country = models.ForeignKey(MultiStep, on_delete=models.CASCADE)
#     name = models.CharField(max_length=40)

#     def __str__(self):
#         return self.name


# # class Person(models.Model):
# #     name = models.CharField(max_length=124)
# #     country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True)
# #     city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True)

#     def __str__(self):
#         return self.name





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






