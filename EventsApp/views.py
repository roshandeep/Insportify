from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from .forms import MultiStepForm, UserForm
from .models import IsSportsMaster, IsVenueMaster, master_table
from django.views.generic import View, FormView
from .models import IsEventTypeMaster


@login_required
def multistep(request):
    submitted = False
    if request.method == "POST":
        form = MultiStepForm(request.POST)
        print('form is going to be validated')
        if form.is_valid():
            print('form validated')
            form.save()
            return HttpResponseRedirect('/?submitted=True')
    else:
        form = MultiStepForm
        if 'submitted' in request.GET:
            submitted = True
    # print('not validated', messages.error)
    return render(request, 'EventsApp/multi_step.html', {'form': form, 'submitted': submitted})


@login_required
def all_events(request):
    event_list = master_table.objects.all()
    return render(request, 'EventsApp/event_list.html', {'event_list': event_list})


@login_required
def user_profile(request):
    context = {
        'user': request.user
    }
    return render(request, 'registration/individual_view.html', context)


def organization_profile(request):
    context = {
        'user': request.user
    }
    return render(request, 'registration/organization_view.html', context)


class UserProfileView(FormView):
    form_class = UserForm
    template_name = 'EventsApp/user_profile.html'
    success_url = reverse_lazy('multistep')


def home(request):
    results = IsEventTypeMaster.objects.values('etm_id', 'etm_category')
    sports = IsSportsMaster.objects.values('sm_id', 'sm_sports_name')
    venues = IsVenueMaster.objects.values('vm_id', 'vm_name')
    events = master_table.objects.all()
    events = [events[i:i + 3] for i in range(0, len(events), 3)]
    context = {
        'event_types': results,
        'sports_list': sports,
        'venues_list': venues,
        'events': events
    }
    html_template = loader.get_template('EventsApp/home.html')
    return HttpResponse(html_template.render(context, request))

# def register_request(request):
# 	if request.method == "POST":
# 		form = NewUserForm(request.POST)
# 		if form.is_valid():
# 			user = form.save()
# 			login(request, user)
# 			messages.success(request, "Registration successful." )
# 			return redirect("main:homepage")
# 		messages.error(request, "Unsuccessful registration. Invalid information.")
# 	form = NewUserForm()
# 	return render (request=request, template_name="EventsApp/register.html", context={"register_form":form})

# def person_create_view(request):
#     form = PersonCreationForm()
#     if request.method == 'POST':
#         form = PersonCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('person_add')
#     return render(request, 'EventsApp/index.html', {'form': form})

# def person_update_view(request, pk):
#     person = get_object_or_404(Person, pk=pk)
#     form = PersonCreationForm(instance=person)
#     if request.method == 'POST':
#         form = PersonCreationForm(request.POST, instance=person)
#         if form.is_valid():
#             form.save()
#             return redirect('person_change', pk=pk)
#     return render(request, 'EventsApp/index.html', {'form': form})

# # AJAX
# def load_cities(request):
#     country_id = request.GET.get('country_id')
#     cities = City.objects.filter(country_id=country_id).all()
#     return render(request, 'EventsApp/city_dropdown_list_options.html', {'cities': cities})
#     #return render(request, 'EventsApp/multi_step.html', {'result': cities})


# def multiformvalidation(request):
# 	submitted = False
# 	if request.method == "POST":
# 		if request.user.is_superuser:
# 			form = MultiFormValidation(request.POST)
# 			if form.is_valid():
# 				form.save()
# 				return HttpResponseRedirect('/event_detail?submitted=True')
# 		else:
# 			form = MultiFormValidation(request.POST)
# 			if form.is_valid():
# 				#form.save()
# 				event = form.save(commit=False)
# 				event.manager = request.user
# 				event.save()
# 				return HttpResponseRedirect('/event_detail?submitted=True')

# 	else:
# 		if request.user.is_superuser:
# 			form = MultiFormValidation
# 		else:
# 			form = MultiFormValidation
# 		if 'submitted' in request.GET:
# 			submitted = True
# 	form = MultiFormValidation
# 	return render(request, 'EventsApp/multi_form.html',{'form' : form, 'submitted':submitted})

# def event_detail(request):
# 	event_list = MultiStep.objects.all()
# 	return render(request, 'EventsApp/event_detail.html',{
# 		'event_detail':event_detail,
# 		})

# def update_event(request,event_id):
# 	event = Event.objects.get(pk=event_id)
# 	if request.user.is_superuser:
# 		form = EventFormAdmin(request.POST or None)
# 	else:
# 		form = EventForm(request.POST or None, instance=event)

# 	if form.is_valid():
# 		form.save()
# 		return redirect('list-events')

# 	return render(request, 'EventsApp/update_event.html', {'event' : event,'form' : form})


# def add_event(request):
# 	submitted = False
# 	if request.method == "POST":
# 		if request.user.is_superuser:
# 			form = EventFormAdmin(request.POST)
# 			if form.is_valid():
# 				form.save()
# 				return HttpResponseRedirect('/add_event?submitted=True')
# 		else:
# 			form = EventForm(request.POST)
# 			if form.is_valid():
# 				#form.save()
# 				event = form.save(commit=False)
# 				event.manager = request.user
# 				event.save()
# 				return HttpResponseRedirect('/add_event?submitted=True')
# 	else:
# 		if request.user.is_superuser:
# 			form = EventFormAdmin
# 		else:
# 			form = EventForm
# 		if 'submitted' in request.GET:
# 			submitted = True
# 	form = EventForm
# 	return render(request, 'EventsApp/add_event.html',{'form' : form, 'submitted':submitted})


# def show_venue(request,venue_id):
# 	venue = Venue.objects.get(pk=venue_id)
# 	return render(request, 'EventsApp/show_venue.html',{
# 		'venue':venue,
# 		})


# def list_venues(request):
# 	venue_list = Venue.objects.all()
# 	return render(request, 'EventsApp/venue.html',{
# 		'venue_list':venue_list,
# 		})
# def add_venue(request):
# 	submitted = False
# 	if request.method == "POST":
# 		form = VenueForm(request.POST)
# 		if form.is_valid():
# 			form.save()
# 			return HttpResponseRedirect('/add_venue?submitted=True')
# 	else:
# 		form = VenueForm
# 		if 'submitted' in request.GET:
# 			submitted = True
# 	form = VenueForm
# 	return render(request, 'EventsApp/add_venue.html',{'form' : form, 'submitted':submitted})

# def all_events(request):
# 	event_list = Event.objects.all()
# 	return render(request, 'EventsApp/event_list.html',{
# 		'event_list':event_list,
# 		})

# Added by Pooja for homepage design and Integration with rest of the flow - 04 FEB 2022
