from django import forms
from django.forms import ModelForm
from .models import Venue, Event

#Admin superUser event form
class EventFormAdmin(ModelForm):
	class Meta:
		model = Event
		fields = ('name','event_date', 'category','venue', 'manager','attendees','description')
		labels = {
			'name': 'Event',
			'event_date': 'Event Date',
			'category' : 'Category', 
			'venue': 'Venue',
			'manager': 'Manager',
			'attendees': 'Attendees',
			'description':'',
		}

		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control','placeholder' :'Event Name'}),
			'event_date': forms.DateTimeInput(attrs={'class':'form-control','placeholder' :'YYYY-MM-DD HH:MM:SS'}),
			'category': forms.TextInput(attrs={'class':'form-control','placeholder' :'Category'}),
			'venue': forms.Select(attrs={'class':'form-select','placeholder' :'Venue'}),
			'manager': forms.Select(attrs={'class':'form-select','placeholder' :'Manager'}),
			'attendees': forms.SelectMultiple(attrs={'class':'form-control','placeholder' : 'Attendees'}),
			'description':forms.Textarea(attrs={'class':'form-control','placeholder' :'Description'}),
		}
#user event form
class EventForm(ModelForm):
	class Meta:
		model = Event
		fields = ('name','event_date', 'category','venue','attendees','description')
		labels = {
			'name': 'Event',
			'event_date': 'Event Date',
			'category' : 'Category', 
			'venue': 'Venue',
			'attendees': 'Attendees',
			'description':'',
		}

		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control','placeholder' :'Event Name'}),
			'event_date': forms.DateTimeInput(attrs={'class':'form-control','placeholder' :'YYYY-MM-DD HH:MM:SS'}),
			'category': forms.TextInput(attrs={'class':'form-control','placeholder' :'Category'}),
			'venue': forms.Select(attrs={'class':'form-select','placeholder' :'Venue'}),
			'attendees': forms.SelectMultiple(attrs={'class':'form-control','placeholder' : 'Attendees'}),
			'description':forms.Textarea(attrs={'class':'form-control','placeholder' :'Description'}),
		}

#create a venue form
class VenueForm(ModelForm):
	class Meta:
		model = Venue
		fields = ('name','address', 'zip_code', 'phone','web', 'email_address')
		labels = {
			'name': '',
			'address': '',
			'zip_code': '',
			'phone': '',
			'web':'',
			'email_address': '',
		}

		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control','placeholder' :'Venue Name'}),
			'address': forms.TextInput(attrs={'class':'form-control','placeholder' :'Address'}),
			'zip_code': forms.TextInput(attrs={'class':'form-control','placeholder' :'Zip Code'}),
			'phone': forms.TextInput(attrs={'class':'form-control','placeholder' :'Phone'}),
			'web':forms.TextInput(attrs={'class':'form-control','placeholder' :'Web Address'}),
			'email_address': forms.EmailInput(attrs={'class':'form-control','placeholder' : 'Email'}),
		}

