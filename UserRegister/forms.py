from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms

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
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
	first_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
	last_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
	username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
	last_login = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
	date_joined = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))


	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password', 'last_login', 'date_joined')