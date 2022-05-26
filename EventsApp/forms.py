from django import forms
from django.forms import ModelForm
from .models import master_table, Availability, Invite
# from EventsApp.models import Person, City, Country
# from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class MultiStepForm(ModelForm):
    class Meta:
        model = master_table
        fields = (
        'event_title', 'description','event_type', 'sport_type', 'position', 'skill', 'min_age', 'max_age', 'sport_category',
        'venue', 'province', 'country', 'city', 'datetimes', 'no_of_position', 'position_cost')
        labels = {
            'event_title': '',
            'description': '',
            'datetimes': '',
            'sport_category': '',
            'venue': 'Venue',
            'street': '',
            'province': '',
            'city': '',
            'country': '',
            'sport_type': '',
            'position': '',
            'skill': '',
            'min_age': '',
            'max_age': '',
            'event_type': '',
            'no_of_position': '',
            'position_cost': ''
        }


class RegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'password1', 'password2')


class ForgotPasswordForm(AuthenticationForm):
    email = forms.CharField(label='Email')


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


class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['day_of_week', 'start_time', 'end_time']

        widgets = {
            'start_time': forms.TimeInput(format='%H:%M', attrs={'placeholder': 'HH:MM 24 hr format'}),
            'end_time': forms.TimeInput(format='%H:%M', attrs={'placeholder': 'HH:MM 24 hr format'})
        }

    field_order = ['day_of_week', 'start_time', 'end_time',]

class InviteForm(forms.ModelForm):
    class Meta:
        model = Invite
        fields = ['email']

    field_order = ['email',]