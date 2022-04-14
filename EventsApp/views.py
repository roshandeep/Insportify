from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from .forms import MultiStepForm, UserForm
from .models import IsSportsMaster, IsVenueMaster, master_table, Individual, Organization
from django.views.generic import View, FormView
from .models import IsEventTypeMaster


@login_required
def multistep(request):
    if request.method == "POST":
        form = MultiStepForm(request.POST)
        print('form is going to be validated')
        if form.is_valid():
            print('form validated')
            form.save()
            messages.success(request, 'Event Created')
            return render(request, 'EventsApp/multi_step.html', {'form': form})
    else:
        form = MultiStepForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'EventsApp/multi_step.html', {'form': form})


@login_required
def all_events(request):
    event_list = master_table.objects.all()
    return render(request, 'EventsApp/event_list.html', {'event_list': event_list})


def event_by_id(request, event_id):
    event = master_table.objects.get(pk=event_id)
    print(event.description)
    return render(request, 'EventsApp/event_detail.html', {'event': event})


@login_required
def user_profile(request):
    context = {
        'user': request.user
    }
    if request.method == "POST":
        response = request.POST.dict()
        obj = Individual()
        obj.user = request.user
        obj.first_name = response["first_name"]
        obj.last_name = response["last_name"]
        obj.phone = response["mobile"]
        obj.email = response["contact_email"]
        obj.provider = response["provider"]
        obj.dob = response["dob"]
        obj.concussion = response["is_concussion"]
        obj.participation_interest = response["interest_gender"]
        obj.city = response["city"]
        obj.province = response["province"]
        obj.country = response["Country"]
        obj.sports_category = response["sport_category"]
        obj.sports_type = response["sport_type"]
        obj.sports_position = response["position"]
        obj.sports_skill = response["skill"]
        obj.save()
        messages.success(request, 'Individual details updated!')

    return render(request, 'registration/individual_view.html', context)


@login_required
def organization_profile(request):
    context = {
        'user': request.user
    }
    if request.method == "POST":
        response = request.POST.dict()
        obj = Organization()
        obj.user = request.user
        obj.type_of_organization = response["type_of_organization"]
        obj.organization_name = response["company_name"]
        obj.parent_organization_name = response["parent_organization"]
        obj.registration_no = response["registration"]
        obj.street = response["street_name"]
        obj.city = response["city"]
        obj.province = response["province"]
        obj.country = response["country"]
        obj.postal_code = response["postal_code"]
        obj.email = response["email"]
        obj.phone = response["phone"]
        obj.website = response["website"]
        obj.gender_focus = response["gender"]
        obj.age_group = response["age_group"]
        obj.save()
        messages.success(request, 'Organization details updated!')
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
