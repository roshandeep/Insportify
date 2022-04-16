import openpyxl
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from .forms import MultiStepForm, UserForm
from .models import master_table, Individual, Organization, Venues, SportsCategory
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
    if request.method == "GET":
        individual = Individual.objects.get(user=request.user)
        context['individual'] = individual
        return render(request, 'registration/individual_view.html', context)

    elif request.method == "POST":
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
    if request.method == "GET":
        organization = Organization.objects.get(user=request.user)
        context['organization'] = organization
        return render(request, 'registration/organization_view.html', context)

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
    sports = SportsCategory.objects.values('pk', 'sports_catgeory_text')
    venues = Venues.objects.values('pk', 'vm_name')
    load_venues_excel()
    events = master_table.objects.all()
    events = [events[i:i + 3] for i in range(0, len(events), 3)]
    context = {
        'sports_list': sports,
        'venues_list': venues,
        'events': events
    }
    html_template = loader.get_template('EventsApp/home.html')
    return HttpResponse(html_template.render(context, request))


def load_venues_excel():
    path = "./venue.xlsx"
    wb_obj = openpyxl.load_workbook(path)
    sheet_obj = wb_obj.active
    # Venues.objects.all().delete()
    for i in range(1, sheet_obj.max_row+1):
        if sheet_obj.cell(row=i, column=5).value.strip() == "ON":
            vm_name = sheet_obj.cell(row=i, column=1).value.strip()
            vm_venue_description = sheet_obj.cell(row=i, column=2).value.strip()
            vm_venue_street = sheet_obj.cell(row=i, column=3).value.strip()
            vm_venuecity = sheet_obj.cell(row=i, column=4).value.strip()
            vm_venue_province = sheet_obj.cell(row=i, column=5).value.strip()
            vm_venue_country = sheet_obj.cell(row=i, column=6).value.strip()
            vm_venue_zip = sheet_obj.cell(row=i, column=7).value.strip()
            obj = Venues(vm_name=vm_name, vm_venue_description=vm_venue_description, vm_venue_street=vm_venue_street,
                         vm_venuecity=vm_venuecity, vm_venue_province=vm_venue_province,
                         vm_venue_country=vm_venue_country, vm_venue_zip=vm_venue_zip)
            # obj.save()