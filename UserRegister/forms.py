from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from django.db import transaction
from EventsApp.models import  User
from django.contrib.auth import get_user_model
from EventsApp.models import Individual, Organization

User = get_user_model()

class IndividualSignUpForm(UserCreationForm):
	first_name = forms.CharField(required=True)
	last_name = forms.CharField(required=True)
	phone = forms.CharField(required=True)

	class Meta(UserCreationForm.Meta):
		model = User

	@transaction.atomic
	def save(self):
		user = super().save(commit=False)
		user.is_individual = True
		user.first_name = self.cleaned_data.get('first_name')
		user.last_name = self.cleaned_data.get('last_name')
		user.save()
		individual = Individual.objects.create(user=user)
		individual.phone = self.cleaned_data.get('phone')
		individual.save()
		return user

class OrganizationSignUpForm(UserCreationForm):
	organization_name = forms.CharField(required=True)
	# last_name = forms.CharField(required=True)
	phone = forms.CharField(required=True)

	class Meta(UserCreationForm.Meta):
		model = User

	@transaction.atomic
	def save(self):
		user = super().save(commit=False)
		user.is_organization = True
		user.is_staff = True
		user.first_name = self.cleaned_data.get('first_name')
		user.last_name = self.cleaned_data.get('last_name')
		user.save()
		organization = Organization.objects.create(user=user)
		organization.phone = self.cleaned_data.get('phone')
		organization.save()
		return user



class DateInput(forms.DateInput):
    input_type = 'date'
class SignUpForm(UserCreationForm):
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
	first_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
	last_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
	#birthdate = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name')


	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class']='form-control'
		self.fields['first_name'].widget.attrs['class']='form-control'
		self.fields['last_name'].widget.attrs['class']='form-control'

class EditProfileForm(UserChangeForm):
	first_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
	last_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
	username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
	dob = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
	phone = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
	i_am_interested_participating_in = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
	have_you_ever_had_concussion = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
	prefer_city = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
	prefer_province = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
	prefer_country = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
	prefer_sport= forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
	prefer_position = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))


	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name','dob', 'password', 'email', 'phone','i_am_interested_participating_in','have_you_ever_had_concussion', 'prefer_city', 'prefer_province', 'prefer_country', 'prefer_sport', 'prefer_position')