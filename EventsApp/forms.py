from django import forms
from django.forms import ModelForm
from .models import master_table, Test_Person, Test_City
#from EventsApp.models import Person, City, Country
#from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

# #Admin superUser event form
# class EventFormAdmin(ModelForm):
# 	class Meta:
# 		model = Event
# 		fields = ('name','event_date', 'category','venue', 'manager','attendees','description')
# 		labels = {
# 			'name': 'Event',
# 			'event_date': 'Event Date',
# 			'category' : 'Category', 
# 			'venue': 'Venue',
# 			'manager': 'Manager',
# 			'attendees': 'Attendees',
# 			'description':'',
# 		}

# 		widgets = {
# 			'name': forms.TextInput(attrs={'class':'form-control','placeholder' :'Event Name'}),
# 			'event_date': forms.DateTimeInput(attrs={'class':'form-control','placeholder' :'YYYY-MM-DD HH:MM:SS'}),
# 			'category': forms.TextInput(attrs={'class':'form-control','placeholder' :'Category'}),
# 			'venue': forms.Select(attrs={'class':'form-select','placeholder' :'Venue'}),
# 			'manager': forms.Select(attrs={'class':'form-select','placeholder' :'Manager'}),
# 			'attendees': forms.SelectMultiple(attrs={'class':'form-control','placeholder' : 'Attendees'}),
# 			'description':forms.Textarea(attrs={'class':'form-control','placeholder' :'Description'}),
# 		}
# #user event form
# class EventForm(ModelForm):
# 	class Meta:
# 		model = Event
# 		fields = ('name','event_date', 'category','venue','attendees','description')
# 		labels = {
# 			'name': 'Event',
# 			'event_date': 'Event Date',
# 			'category' : 'Category', 
# 			'venue': 'Venue',
# 			'attendees': 'Attendees',
# 			'description':'',
# 		}

# 		widgets = {
# 			'name': forms.TextInput(attrs={'class':'form-control','placeholder' :'Event Name'}),
# 			'event_date': forms.DateTimeInput(attrs={'class':'form-control','placeholder' :'YYYY-MM-DD HH:MM:SS'}),
# 			'category': forms.TextInput(attrs={'class':'form-control','placeholder' :'Category'}),
# 			'venue': forms.Select(attrs={'class':'form-select','placeholder' :'Venue'}),
# 			'attendees': forms.SelectMultiple(attrs={'class':'form-control','placeholder' : 'Attendees'}),
# 			'description':forms.Textarea(attrs={'class':'form-control','placeholder' :'Description'}),
# 		}

# #create a venue form
# class VenueForm(ModelForm):
# 	class Meta:
# 		model = Venue
# 		fields = ('name','address', 'zip_code', 'phone','web', 'email_address')
# 		labels = {
# 			'name': '',
# 			'address': '',
# 			'zip_code': '',
# 			'phone': '',
# 			'web':'',
# 			'email_address': '',
# 		}

# 		widgets = {
# 			'name': forms.TextInput(attrs={'class':'form-control','placeholder' :'Venue Name'}),
# 			'address': forms.TextInput(attrs={'class':'form-control','placeholder' :'Address'}),
# 			'zip_code': forms.TextInput(attrs={'class':'form-control','placeholder' :'Zip Code'}),
# 			'phone': forms.TextInput(attrs={'class':'form-control','placeholder' :'Phone'}),
# 			'web':forms.TextInput(attrs={'class':'form-control','placeholder' :'Web Address'}),
# 			'email_address': forms.EmailInput(attrs={'class':'form-control','placeholder' : 'Email'}),
# 		}

# class NewUserForm(UserCreationForm):
# 	email = forms.EmailField(required=True)

# 	class Meta:
# 		model = User
# 		fields = ("username", "email", "password1","password2")

# 	def save(self, commit=True):
# 		user = super(NewUserForm, self).save(commit=False)
# 		user.email = self.cleaned_date['email']
# 		if commit:
# 			user.save()
# 		return user


class MultiStepForm(ModelForm):
	#sport_type: forms.ChoiceField(choices=CHOICES)
	#CHOICES = [('R','Recurring day'),('S','Singular day')]
	#CHOICES1 = [('Private','Private Event'),('Public', 'Public Event'),('F','Free'),('fee','Fee')]
	#sport_type =forms.CharField(label='Recurring/Day', widget=forms.RadioSelect(choices=CHOICES))
	#event_type =forms.CharField(label='Event Type', widget=forms.RadioSelect(choices=CHOICES1))
	class Meta:
		model = master_table
		#fields = "__all__"
		fields = ('event_title','description', 'sport_type','position','skill','min_age','max_age','sport_category','venue','province','country','city', 'datetimes','no_of_position', 'position_cost')
		labels = {
			'event_title': '',
			'description' : '',
			'datetimes':'',
			'sport_category' : '',
			'venue' : 'Venue',
			'street' : '',
			'province' : '',
			'city' : '',
			'country' : '',
			'sport_type' : '',
			'position' : '',
			'skill' : '',
			'min_age' : '',
			'max_age' : '',
			'event_type' : '',
			'no_of_position' : '',
			'position_cost' : ''
			#'name' : '',
			}
class RegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email / Username')

class UserForm(forms.Form):
	first_name = forms.CharField(max_length=20)
	last_name = forms.CharField(max_length=20)
	DOB = forms.DateField()
	contact = forms.CharField(max_length=50)
	participate = forms.CharField(max_length=30)
	is_concussion = forms.CharField(max_length=10)
	pref_city = forms.CharField(max_length=30)
	pref_province = forms.CharField(max_length=30)
	pref_country = forms.CharField(max_length=30)
	pref_sport = forms.CharField(max_length=30)
	pref_sport = forms.CharField(max_length=30)
	pref_position = forms.CharField(max_length=30)




		# }

		# widgets = {
		# 	'event_title': forms.TextInput(attrs={'class':'form-control','placeholder' :'Event Title'}),
		# 	'description': forms.TextInput(attrs={'class':'form-control','placeholder' :'Description'}),
		# 	'event_time': forms.NumberInput(),
		# 	'event_date': forms.TextInput(attrs={'class':'form-control','placeholder' :'Event date'}),
		# 	'sport_category' : forms.TextInput(attrs={'class':'form-control','placeholder' :'Sport Name'}),
		# 	'venue': forms.TextInput(attrs={'class':'form-control','placeholder' :'Venue'}),
		# 	'street': forms.TextInput(attrs={'class':'form-control','placeholder' :'Street'}),
		# 	'province': forms.TextInput(attrs={'class':'form-control','placeholder' :'Province'}),
		# 	'city': forms.TextInput(attrs={'class':'form-control','placeholder' :'city'}),
		# 	'country': forms.TextInput(attrs={'class':'form-control','placeholder' :'Country'}),
		# 	'zip_code': forms.TextInput(attrs={'class':'form-control','placeholder' :'Zip Code'}),
		# 	'event_type': forms.TextInput(),
		# 	'sport_category': forms.TextInput(attrs={'class':'form-control','placeholder' :'Sport Category'}),
		# 	'sport_type' : forms.TextInput(attrs={'class':'form-control','placeholder' :'Sport Type'}),
		# 	'skill' : forms.TextInput(attrs={'class':'form-control','placeholder' :'sport_type'}),
		# 	'position_price' : forms.Numbernput(),
		# 	'min_age' : forms.NumberInput(),
		# 	'max_age' : forms.NumberInput(),
		# 	#'name' : forms.TextInput(attrs={'class':'form-control','placeholder' :'Name'})
		# 	}


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