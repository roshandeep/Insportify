from django import forms
from django.forms import ModelForm
from .models import Venue, Event, MultiStep
#from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput



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




class MultiStepForm(ModelForm):
	#sport_type: forms.ChoiceField(choices=CHOICES)
	#CHOICES = [('R','Recurring day'),('S','Singular day')]
	#CHOICES1 = [('Private','Private Event'),('Public', 'Public Event'),('F','Free'),('fee','Fee')]
	#sport_type =forms.CharField(label='Recurring/Day', widget=forms.RadioSelect(choices=CHOICES))
	#event_type =forms.CharField(label='Event Type', widget=forms.RadioSelect(choices=CHOICES1))
	class Meta:
		model = MultiStep
		fields = ('event_title','category','description', 'event_type','ath_min_age','ath_max_age','sup_min_age','sup_max_age','event_time','event_date','venue','street','city','province','country','zip_code','staff_level','athelete_level')
		labels = {
			'event_title': '',
			'category' : '',
			'description' : '',
			'event_type' : '',
			'ath_min_age': '',
			'ath_max_age' : '',
			'sup_min_age' : '',
			'sup_max_age' : '',
			'event_time':'',
			'event_date' : '',
			'venue' : 'Venue',
			'street' : '',
			'city' : '',
			'province' : '',
			'country' : '',
			'zip_code' : '',
			'staff_level' : '',
			'athelete_level' : '',
		}
		widgets = {
			'event_title': forms.TextInput(attrs={'class':'form-control','placeholder' :'Event Title'}),
			'category' : forms.TextInput(attrs={'class':'form-select','placeholder' :'Select Category'}),
			'description': forms.TextInput(attrs={'class':'form-control','placeholder' :'Description'}),
			'event_type': forms.TextInput(attrs={'class':'form-control','placeholder' :'Event Type'}),
			'ath_min_age': forms.TextInput(attrs={'class': 'form-control'}),
			'ath_max_age': forms.TextInput(attrs={'class': 'form-control'}),
			'sup_min_age': forms.TextInput(attrs={'class': 'form-control'}),
			'sup_max_age': forms.TextInput(attrs={'class': 'form-control'}),
			'event_time': forms.TextInput(attrs={'class':'form-control','placeholder' :'Event Time'}),
			'event_date': forms.TextInput(attrs={'class':'form-control','placeholder' :'Event Date'}),
			'venue': forms.TextInput(attrs={'class':'form-control','placeholder' :'Venue'}),
			'street': forms.TextInput(attrs={'class':'form-control','placeholder' :'Street'}),
			'city': forms.TextInput(attrs={'class':'form-control','placeholder' :'City'}),
			'province': forms.TextInput(attrs={'class':'form-control','placeholder' :'Province'}),
			'country': forms.TextInput(attrs={'class':'form-control','placeholder' :'Country'}),
			'zip_code': forms.TextInput(attrs={'class':'form-control','placeholder' :'Zip Code'}),
			'staff_level': forms.TextInput(attrs={'class':'form-control','placeholder' :'Staff level'}),
			'athelete_level': forms.TextInput(attrs={'class':'form-control','placeholder' :'Athelete level'}),
			}
