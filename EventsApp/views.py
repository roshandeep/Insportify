from django.shortcuts import render,redirect,reverse
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect
from .models import Event, Venue, MultiStep
from .forms import VenueForm, EventForm, EventFormAdmin,MultiStepForm
#from formtools.wizard.views import SessionWizardView
from django.contrib import messages

def multistep(request):
	submitted = False
	if request.method == "POST":
		form = MultiStepForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/?submitted=True')
	else:
		form = MultiStepForm
		if 'submitted' in request.GET:
			submitted = True
	return render(request, 'EventsApp/multi_step.html',{'form' : form, 'submitted':submitted})

def multiformvalidation(request):
	submitted = False
	if request.method == "POST":
		if request.user.is_superuser:
			form = MultiFormValidation(request.POST)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/event_detail?submitted=True')
		else:
			form = MultiFormValidation(request.POST)
			if form.is_valid():
				#form.save()
				event = form.save(commit=False)
				event.manager = request.user
				event.save()
				return HttpResponseRedirect('/event_detail?submitted=True')

	else:
		if request.user.is_superuser:
			form = MultiFormValidation
		else:
			form = MultiFormValidation
		if 'submitted' in request.GET:
			submitted = True
	form = MultiFormValidation
	return render(request, 'EventsApp/multi_form.html',{'form' : form, 'submitted':submitted})

def event_detail(request):
	event_list = MultiStep.objects.all()
	return render(request, 'EventsApp/event_detail.html',{
		'event_detail':event_detail,
		})

def update_event(request,event_id):
	event = Event.objects.get(pk=event_id)
	if request.user.is_superuser:
		form = EventFormAdmin(request.POST or None)
	else:
		form = EventForm(request.POST or None, instance=event)

	if form.is_valid():
		form.save()
		return redirect('list-events')

	return render(request, 'EventsApp/update_event.html', {'event' : event,'form' : form})



def add_event(request):
	submitted = False
	if request.method == "POST":
		if request.user.is_superuser:
			form = EventFormAdmin(request.POST)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/add_event?submitted=True')
		else:
			form = EventForm(request.POST)
			if form.is_valid():
				#form.save()
				event = form.save(commit=False)
				event.manager = request.user
				event.save()
				return HttpResponseRedirect('/add_event?submitted=True')
	else:
		if request.user.is_superuser:
			form = EventFormAdmin
		else:
			form = EventForm
		if 'submitted' in request.GET:
			submitted = True
	form = EventForm
	return render(request, 'EventsApp/add_event.html',{'form' : form, 'submitted':submitted})


def show_venue(request,venue_id):
	venue = Venue.objects.get(pk=venue_id)
	return render(request, 'EventsApp/show_venue.html',{
		'venue':venue,
		})


def list_venues(request):
	venue_list = Venue.objects.all()
	return render(request, 'EventsApp/venue.html',{
		'venue_list':venue_list,
		})
def add_venue(request):
	submitted = False
	if request.method == "POST":
		form = VenueForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/add_venue?submitted=True')
	else:
		form = VenueForm
		if 'submitted' in request.GET:
			submitted = True
	form = VenueForm
	return render(request, 'EventsApp/add_venue.html',{'form' : form, 'submitted':submitted})

def all_events(request):
	event_list = Event.objects.all()
	return render(request, 'EventsApp/event_list.html',{
		'event_list':event_list,
		})

def home(request,year=datetime.now().year,month=datetime.now().strftime('%B')):
	name = 'Don'
	month = month.capitalize()
	#Convert month from name to number
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	#Create a calendar
	cal = HTMLCalendar().formatmonth(
		year,
		month_number)

	#get current year/time
	now = datetime.now()
	current_year = now.year

	#get current time
	time = now.strftime('%I:%M %p')
	return render(request, 'EventsApp/home.html',{
		"name" : name,
		"year" : year,
		"month": month,
		"month_number" : month_number,
		"cal": cal,
		"current_year": current_year,
		"time": time
		})

# Create your views here.
