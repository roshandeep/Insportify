from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from django.db import transaction
from EventsApp.models import User
from django.contrib.auth import get_user_model
from EventsApp.models import Individual, Organization, Profile

User = get_user_model()


class IndividualSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    email = forms.CharField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'type': 'password', 'name': 'password1'}),
        label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'type': 'password', 'name': 'password2'}),
        label="Password (again)")

    class Meta:
        model = User
        fields = (
            "email",
            'password1',
            'password2',
            "first_name",
            "last_name",
            "phone",
        )

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_individual = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email').lower()
        user.set_password(self.cleaned_data["password1"])
        user.save()
        profile = Profile.objects.create(active_user=user,user=user, name=user.first_name, is_master=True)
        individual = Individual.objects.create(profile=profile)
        individual.phone = self.cleaned_data.get('phone')
        # individual.email = self.cleaned_data.get('email').lower()
        individual.first_name = self.cleaned_data.get('first_name')
        individual.last_name = self.cleaned_data.get('last_name')
        individual.save()
        return user


class MVPSignUpForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    email = forms.CharField(required=True)
    website = forms.CharField(required=False)
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'type': 'password', 'name': 'password1'}),
        label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'type': 'password', 'name': 'password2'}),
        label="Password (again)")

    class Meta():
        model = User
        fields = (
            "email",
            'password1',
            'password2',
            "first_name",
            "last_name",
            "phone",
            "website",
        )

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_individual = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email').lower()
        user.set_password(self.cleaned_data["password1"])
        user.save()
        profile = Profile.objects.create(active_user=user,user=user, is_master=True)
        individual = Individual.objects.create(profile=profile)
        individual.phone = self.cleaned_data.get('phone')
        # individual.email = self.cleaned_data.get('email').lower()
        individual.first_name = self.cleaned_data.get('first_name')
        individual.last_name = self.cleaned_data.get('last_name')
        individual.website = self.cleaned_data.get('website')
        individual.save()
        return user


class PasswordResetAuthForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ("email",)
        exclude = ("password",)


class OrganizationSignUpForm(forms.ModelForm):
    organization_name = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    email = forms.CharField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'type': 'password', 'name': 'password1'}),
        label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'type': 'password', 'name': 'password2'}),
        label="Password (again)")

    class Meta():
        model = User
        fields = (
            "email",
            'password1',
            'password2',
            "organization_name",
            "phone",
        )

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_organization = True
        user.is_staff = True
        user.first_name = self.cleaned_data.get('organization_name')
        user.email = self.cleaned_data.get('email').lower()
        user.set_password(self.cleaned_data["password1"])
        # print(self.cleaned_data["password1"])
        user.save()
        profile = Profile.objects.create(active_user=user,user=user, is_master=True)
        organization = Organization.objects.create(profile=profile)
        organization.organization_name = self.cleaned_data.get('organization_name')
        organization.phone = self.cleaned_data.get('phone')
        organization.email = self.cleaned_data.get('email').lower()
        organization.save()
        return user


class DateInput(forms.DateInput):
    input_type = 'date'


class SignUpForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
