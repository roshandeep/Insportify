from django import forms
from django.forms import ModelForm
from .models import Venue, Event, MultiStep
#from EventsApp.models import Person, City, Country
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
		#fields = "__all__"
		fields = ('event_title','description', 'sport_type','position','skill','position_price','min_age','max_age','event_time','event_date','sport_category','venue','street','province','country','zip_code','city', 'event_type')
		labels = {
			'event_title': '',
			'description' : '',
			'event_time':'',
			'event_date' : '',
			'sport_category' : '',
			'venue' : 'Venue',
			'street' : '',
			'province' : '',
			'city' : '',
			'country' : '',
			'zip_code' : '',
			'sport_type' : '',
			'position' : '',
			'skill' : '',
			'position_price' : 'position_price',
			'min_age' : '',
			'max_age' : '',
			'event_type' : '',
		}

		widgets = {
			'event_title': forms.TextInput(attrs={'class':'form-control','placeholder' :'Event Title'}),
			'description': forms.TextInput(attrs={'class':'form-control','placeholder' :'Description'}),
			'event_time': forms.TextInput(attrs={'class':'form-control','placeholder' :'Event Time'}),
			'event_date': forms.DateTimeInput(attrs={'class':'form-control','placeholder' :'YYYY-MM-DD HH:MM:SS'}),
			'sport_category' : forms.TextInput(attrs={'class':'form-control','placeholder' :'Sport Name'}),
			'venue': forms.TextInput(attrs={'class':'form-control','placeholder' :'Venue'}),
			'street': forms.TextInput(attrs={'class':'form-control','placeholder' :'Street'}),
			'province': forms.TextInput(attrs={'class':'form-control','placeholder' :'Province'}),
			'city': forms.TextInput(attrs={'class':'form-control','placeholder' :'city'}),
			'country': forms.TextInput(attrs={'class':'form-control','placeholder' :'Country'}),
			'zip_code': forms.TextInput(attrs={'class':'form-control','placeholder' :'Zip Code'}),
			'event_type': forms.NumberInput(),
			'sport_category': forms.TextInput(attrs={'class':'form-control','placeholder' :'Sport Category'}),
			'sport_type' : forms.TextInput(attrs={'class':'form-control','placeholder' :'Sport Type'}),
			'skill' : forms.TextInput(attrs={'class':'form-control','placeholder' :'Skill Level'}),
			'position_price' : forms.NumberInput(),
			'min_age' : forms.NumberInput(),
			'max_age' : forms.NumberInput(),
			}


# class PersonCreationForm(forms.ModelForm):
#     class Meta:
#         model = Person
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['city'].queryset = City.objects.none()

#         if 'country' in self.data:
#             try:
#                 country_id = int(self.data.get('country'))
#                 self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
#             except (ValueError, TypeError):
#                 pass  # invalid input from the client; ignore and fallback to empty City queryset
#         elif self.instance.pk:
#             self.fields['city'].queryset = self.instance.country.city_set.order_by('name')