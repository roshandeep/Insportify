from django.shortcuts import render,redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect
from .models import Event,Venue
from .forms import VenueForm, EventForm, EventFormAdmin


def multistepform(request):
	return render(request,'EventsApp/multi_step.html',{})

def multistepform_save(request):
	if request.method!="POST":
		return HttpResponseRedirect(reverse('multistepform'))
	else:
		event_name = request.POST.get("event_name")
		event_date = request.POST.get("event_date")
		description = request.POST.get("description")
		category = request.POST.get('category')
		venue = request.POST.get("venue")
		manager = request.POST.get("manager")
		phone = request.POST.get("phone")
		email = request.POST.get('email')
		website = request.POST.get('website')
		multistepform = MultiStepFormModel(event_name=event_name, event_date=event_date,description=description,category=category,venue=venue,manager=manager,phone=phone,email=email,website=website)
		multistepform.save()
		messages.success(request,'Event successful created!!!')
		return HttpResponseRedirect(reverse('multistepform'))



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
