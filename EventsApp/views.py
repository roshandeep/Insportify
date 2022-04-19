import openpyxl
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from .forms import MultiStepForm, UserForm
from .models import master_table, Individual, Organization, Venues, SportsCategory, SportsType
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
    sports_category = SportsCategory.objects.all()
    sports_type = SportsType.objects.all()
    context['sports_category'] = sports_category
    context['sports_type'] = sports_type

    if request.method == "GET":
        individual = Individual.objects.get(user=request.user)
        # print(individual.__dict__)
        context['individual'] = individual
        return render(request, 'registration/individual_view.html', context)

    elif request.method == "POST":
        individual = Individual.objects.filter(user=request.user)
        response = request.POST.dict()
        if individual.exists():
            individual = Individual.objects.get(user=request.user)
            individual.user = request.user
            individual.first_name = response["first_name"].strip()
            individual.last_name = response["last_name"].strip()
            individual.phone = response["mobile"].strip()
            individual.email = response["contact_email"].strip()
            individual.provider = response["provider"].strip()
            individual.dob = response["dob"].strip()
            individual.concussion = response["is_concussion"].strip()
            individual.participation_interest = response["interest_gender"].strip()
            individual.city = response["city"].strip()
            individual.province = response["province"].strip()
            individual.country = response["Country"].strip()
            individual.sports_category = response["sport_category"].strip()
            individual.sports_type = response["sport_type"].strip()
            individual.sports_position = response["position"].strip()
            individual.sports_skill = response["skill"].strip()
            individual.save()
            context['individual'] = individual
        else:
            obj = Individual()
            obj.user = request.user
            obj.first_name = response["first_name"].strip()
            obj.last_name = response["last_name"].strip()
            obj.phone = response["mobile"].strip()
            obj.email = response["contact_email"].strip()
            obj.provider = response["provider"].strip()
            obj.dob = response["dob"].strip()
            obj.concussion = response["is_concussion"].strip()
            obj.participation_interest = response["interest_gender"].strip()
            obj.city = response["city"].strip()
            obj.province = response["province"].strip()
            obj.country = response["Country"].strip()
            obj.sports_category = response["sport_category"].strip()
            obj.sports_type = response["sport_type"].strip()
            obj.sports_position = response["position"].strip()
            obj.sports_skill = response["skill"].strip()
            obj.save()
            context['individual'] = obj
        messages.success(request, 'Individual details updated!')

    return render(request, 'registration/individual_view.html', context)


def get_selected_sports_type(request):
    data = {}
    if request.method == "POST":
        selected_category = request.POST['selected_category_text']
        try:
            print(selected_category)
            selected_type = SportsType.objects.filter(sports_category__sports_catgeory_text=selected_category)
            print(selected_type)
        except Exception:
            data['error_message'] = 'error'
            return JsonResponse(data)
        return JsonResponse(list(selected_type.values('pk', 'sports_type_text')), safe=False)

@login_required
def organization_profile(request):
    context = {
        'user': request.user
    }
    if request.method == "GET":
        organization = Organization.objects.get(user=request.user)
        print(organization.__dict__)
        context['organization'] = organization
        return render(request, 'registration/organization_view.html', context)

    if request.method == "POST":
        organization = Organization.objects.filter(user=request.user)
        response = request.POST.dict()
        if organization.exists():
            organization = Organization.objects.get(user=request.user)
            organization.user = request.user
            organization.type_of_organization = response["type_of_organization"].strip()
            organization.organization_name = response["company_name"].strip()
            organization.parent_organization_name = response["parent_organization"].strip()
            organization.registration_no = response["registration"].strip()
            organization.street = response["street_name"].strip()
            organization.city = response["city"].strip()
            organization.province = response["province"].strip()
            organization.country = response["country"].strip()
            organization.postal_code = response["postal_code"].strip()
            organization.email = response["email"].strip()
            organization.phone = response["phone"].strip()
            organization.website = response["website"].strip()
            organization.gender_focus = response["gender"].strip()
            organization.age_group = response["age_group"].strip()
            organization.save()
            context['organization'] = organization
        else:
            obj = Organization()
            obj.user = request.user
            obj.type_of_organization = response["type_of_organization"].strip()
            obj.organization_name = response["company_name"].strip()
            obj.parent_organization_name = response["parent_organization"].strip()
            obj.registration_no = response["registration"].strip()
            obj.street = response["street_name"].strip()
            obj.city = response["city"].strip()
            obj.province = response["province"].strip()
            obj.country = response["country"].strip()
            obj.postal_code = response["postal_code"].strip()
            obj.email = response["email"].strip()
            obj.phone = response["phone"].strip()
            obj.website = response["website"].strip()
            obj.gender_focus = response["gender"].strip()
            obj.age_group = response["age_group"].strip()
            obj.save()
            context['organization'] = obj
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