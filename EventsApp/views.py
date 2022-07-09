import calendar
from datetime import datetime, timedelta, date

import openpyxl
import stripe
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from Insportify import settings
from .forms import MultiStepForm, AvailabilityForm, LogoForm, InviteForm
from .models import master_table, Individual, Organization, Venues, SportsCategory, SportsType, Order, User, \
    Availability, Logo, Extra_Loctaions, Events_PositionInfo, Secondary_SportsChoice, Cart, Invite, PositionAndSkillType
import util


@login_required
def multistep(request):
    sports_type = SportsType.objects.all().order_by('sports_type_text')
    venues = Venues.objects.all()
    if request.method == "POST":
        # Had to remove required since some fieldsets are hidden due to pagination causing client side console errors
        # Checking validity here
        form = MultiStepForm(request.POST)
        # Validation
        values_valid = ValidateFormValues(request)
        # Handle Form Post
        if form.is_valid() and values_valid:
            print(list(request.POST.items()))
            # Save data
            obj = form.save(commit=False)
            obj.created_by = request.user
            sports_type_text, sports_catgeory_text = save_sports_type(request)
            skill_list = request.POST.getlist('skill')
            obj.skill = ', '.join(skill_list)
            obj.sport_type = sports_type_text
            obj.sport_category = sports_catgeory_text
            obj.is_recurring = request.POST['recurring_event'] == "Yes"
            obj.datetimes_monday = request.POST.get('datetimes_monday') if obj.is_recurring else ""
            obj.datetimes_tuesday = request.POST.get('datetimes_tuesday') if obj.is_recurring else ""
            obj.datetimes_wednesday = request.POST.get('datetimes_wednesday') if obj.is_recurring else ""
            obj.datetimes_thursday = request.POST.get('datetimes_thursday') if obj.is_recurring else ""
            obj.datetimes_friday = request.POST.get('datetimes_friday') if obj.is_recurring else ""
            obj.datetimes_saturday = request.POST.get('datetimes_saturday') if obj.is_recurring else ""
            obj.datetimes_sunday = request.POST.get('datetimes_sunday') if obj.is_recurring else ""
            obj.datetimes_exceptions = request.POST.get('datetimes_exceptions') if obj.is_recurring else ""
            obj.datetimes = "" if obj.is_recurring else request.POST.get('datetimes')
            obj.save()
            save_event_position_info(request, obj)

            # Take user to event invitation page
            messages.success(request, 'Event Created - Invite Users?')
            redirect_url = f'/invite/' + str(master_table.objects.last().id) + '/'
            return redirect(redirect_url)
        elif not form.is_valid():
            messages.error(request, form.errors)
            messages.error(request, form.non_field_errors)
    else:
        form = MultiStepForm()

    return render(request, 'EventsApp/multi_step.html', {'form': form, 'sports_type': sports_type, 'venues': venues})


def ValidateFormValues(request):
    date_valid = True
    event_count_valid = True
    fields_valid = True
    event_count = len(master_table.objects.filter(created_by=request.user))
    if not request.user.is_mvp and event_count >= 2:
        messages.error(request, "Cannot create event, maximum events possible by non-MVP member is 2")
        event_count_valid = False
    if not request.POST.get('event_title') or not request.POST.get('description') \
            or not request.POST.get('event_type') or not request.POST.get('sport_type') \
            or not request.POST.get('skill') or not request.POST.get('venue'):
        messages.error(request, "All fields are required, please enter valid information")
        fields_valid = False
    if not request.POST.get('recurring_event'):
        messages.error(request, "Please select event recurrence")
        date_valid = False
    else:
        if request.POST['recurring_event'] == "Yes":
            if (not request.POST.get('datetimes_monday') or request.POST['datetimes_monday'] == "") and \
                    (not request.POST.get('datetimes_tuesday') or request.POST['datetimes_tuesday'] == "") and \
                    (not request.POST.get('datetimes_wednesday') or request.POST['datetimes_wednesday'] == "") and \
                    (not request.POST.get('datetimes_thursday') or request.POST['datetimes_thursday'] == "") and \
                    (not request.POST.get('datetimes_friday') or request.POST['datetimes_friday'] == "") and \
                    (not request.POST.get('datetimes_saturday') or request.POST['datetimes_saturday'] == "") and \
                    (not request.POST.get('datetimes_sunday') or request.POST['datetimes_sunday'] == ""):
                messages.error(request, "No date times entered, please enter dates for one of the selected "
                                        "recurring days")
                date_valid = False
        else:
            if not request.POST.get('datetimes') or request.POST['datetimes'] == "":
                messages.error(request, "No date times entered, please enter a date for the event")
                date_valid = False
    for i in range(1, 10):
        if request.POST.get('no_of_position' + str(i)) == '' \
                or request.POST.get('type_of_skill' + str(i)) == '' \
                or request.POST.get('position_cost' + str(i)) == '' \
                or request.POST.get('min_age' + str(i)) == '' \
                or request.POST.get('max_age' + str(i)) == '':
            messages.error(request, "All position fields are required, please enter valid information")
            fields_valid = False

    return date_valid and event_count_valid and fields_valid


def get_venue_details(request):
    data = {}
    if request.method == "POST":
        selected_venue = request.POST['selected_venue']
        try:
            selected_venue = Venues.objects.filter(vm_name=selected_venue)
            # print(selected_venue)
        except Exception:
            data['error_message'] = 'error'
            return JsonResponse(data)
        return JsonResponse(list(selected_venue.values()), safe=False)


def save_sports_type(request):
    if request.POST['sport_type']:
        sports_type_id = request.POST['sport_type']
        obj = SportsType.objects.get(pk=sports_type_id)
        return obj.sports_type_text, obj.sports_category.sports_catgeory_text


def save_event_position_info(request, event):
    for i in range(1, 10):
        if 'no_of_position' + str(i) in request.POST:
            position_type = request.POST['type_of_skill' + str(i)].strip()
            no_of_position = request.POST['no_of_position' + str(i)].strip()
            position_cost = request.POST['position_cost' + str(i)].strip()
            min_age = request.POST['min_age' + str(i)].strip()
            max_age = request.POST['max_age' + str(i)].strip() \
                if request.POST['max_age' + str(i)].strip() == "" else "999"
            obj = Events_PositionInfo(event=event, max_age=max_age, min_age=min_age, no_of_position=no_of_position,
                                      position_cost=position_cost, position_number=i, position_type=position_type)
            obj.save()


@login_required
def all_events(request):
    event_list = master_table.objects.filter(created_by=request.user)
    event_list = format_time(event_list)
    # load_pos_skill_type()
    return render(request, 'EventsApp/event_list.html', {'event_list': event_list})


@login_required
def event_by_id(request, event_id):
    event = master_table.objects.get(pk=event_id)
    context = {
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,
        'event': event
    }
    return render(request, 'EventsApp/event_detail.html', context)


@login_required
def user_profile(request):
    context = {
        'user': request.user
    }
    sports_type = SportsType.objects.all().order_by('sports_type_text')
    context['sports_type'] = sports_type

    if request.method == "GET":
        individual = Individual.objects.get(user=request.user)
        # print(individual.__dict__)
        context['individual'] = individual
        return render(request, 'registration/individual_view.html', context)

    elif request.method == "POST":
        individual = Individual.objects.filter(user=request.user)
        response = request.POST.dict()
        print(response)
        if individual.exists():
            individual = Individual.objects.get(user=request.user)
            individual.user = request.user
            if response["first_name"]:
                individual.first_name = response["first_name"].strip() if response["first_name"] else ""
            if response["last_name"]:
                individual.last_name = response["last_name"].strip() if response["last_name"] else ""
            if response["mobile"]:
                mobile = response["mobile"].strip()
                mobile = ''.join(i for i in mobile if i.isdigit())
                individual.phone = mobile
            if response["contact_email"]:
                individual.email = response["contact_email"].strip() if response["contact_email"] else ""
            if response["dob"]:
                individual.dob = response["dob"].strip() if response["dob"] else ""
            if "is_concussion" in response:
                individual.concussion = response["is_concussion"].strip()
            if "is_student" in response:
                individual.is_student = response["is_student"].strip()
            if "interest_gender" in response:
                individual.participation_interest = response["interest_gender"].strip()
            if response["city"]:
                individual.city = response["city"].strip() if response["city"] else ""
            if response["country"]:
                individual.province = response["country"].strip() if response["country"] else ""
            if response["contact_email"]:
                individual.contact_email = response["contact_email"].strip() if response["contact_email"] else ""
            if response["sport_category"]:
                individual.sports_category = response["sport_category"].strip() if response["sport_category"] else ""
            if response["sport_type"]:
                individual.sports_type = response["sport_type"].strip() if response["sport_type"] else ""
            if response["position"]:
                individual.sports_position = response["position"].strip() if response["position"] else ""
            if response["skill"]:
                individual.sports_skill = response["skill"].strip() if response["skill"] else ""
            update_secondary_locations(request.user, response)
            save_secondary_sports_info(request.user, response)
            individual.save()
            context['individual'] = individual
        else:
            obj = Individual()
            obj.user = request.user
            if response["first_name"]:
                obj.first_name = response["first_name"].strip() if response["first_name"] else ""
            if response["last_name"]:
                obj.last_name = response["last_name"].strip() if response["last_name"] else ""
            if response["mobile"]:
                mobile = response["mobile"].strip()
                mobile = ''.join(i for i in mobile if i.isdigit())
                obj.phone = mobile
            if response["contact_email"]:
                obj.email = response["contact_email"].strip() if response["contact_email"] else ""
            if response["dob"]:
                obj.dob = response["dob"].strip() if response["dob"] else ""
            if "is_concussion" in response:
                obj.concussion = response["is_concussion"].strip()
            if "is_student" in response:
                obj.is_student = response["is_student"].strip()
            if "interest_gender" in response:
                obj.participation_interest = response["interest_gender"].strip()
            if response["city"]:
                obj.city = response["city"].strip() if response["city"] else ""
            if response["province"]:
                obj.province = response["province"].strip() if response["province"] else ""
            if response["country"]:
                obj.country = response["country"].strip() if response["country"] else ""
            if response["sport_category"]:
                obj.sports_category = response["sport_category"].strip() if response["sport_category"] else ""
            if response["sport_type"]:
                obj.sports_type = response["sport_type"].strip() if response["sport_type"] else ""
            if response["position"]:
                obj.sports_position = response["position"].strip() if response["position"] else ""
            if response["skill"]:
                obj.sports_skill = response["skill"].strip() if response["skill"] else ""
            save_secondary_locations(request.user, response)
            save_secondary_sports_info(request.user, response)
            obj.save()
            context['individual'] = obj
        messages.success(request, 'Individual details updated!')

    return render(request, 'registration/individual_view.html', context)


def save_secondary_sports_info(user, response):
    obj = Secondary_SportsChoice.objects.filter(user=user).exists()
    print(response)
    if obj:
        for i in range(1, 4):
            obj = Secondary_SportsChoice.objects.filter(user=user, sport_entry_number=i).exists()
            if obj:
                obj = Secondary_SportsChoice.objects.get(user=user, sport_entry_number=i)
                if 'category_' + str(i) in response:
                    obj.sport_category = response['category_' + str(i)].strip()
                    obj.sport_type = response['type_' + str(i)].strip()
                    obj.position = response['position_' + str(i)].strip()
                    obj.save()
                # else:
                #     sport_category = response['category_' + str(i)].strip()
                #     sport_type = response['type_' + str(i)].strip()
                #     position = response['position_' + str(i)].strip()
                #     obj = Secondary_SportsChoice(user=user, sport_category=sport_category, sport_type=sport_type,
                #                                  position=position, sport_entry_number=i)
                #     obj.save()
    else:
        for i in range(1, 4):
            if 'category_' + str(i) in response:
                sport_category = response['category_' + str(i)].strip()
                sport_type = response['type_' + str(i)].strip()
                position = response['position_' + str(i)].strip()
                obj = Secondary_SportsChoice(user=user, sport_category=sport_category, sport_type=sport_type,
                                             position=position, sport_entry_number=i)
                obj.save()


def update_secondary_locations(user, response):
    # print("Update Old Locs")
    for i in range(1, 5):
        obj = Extra_Loctaions.objects.filter(user=user, location_number=i).exists()
        if obj:
            obj = Extra_Loctaions.objects.get(user=user, location_number=i)
            if 'city' + str(i) in response:
                obj.city = response['city' + str(i)].strip()
                obj.province = response['province' + str(i)].strip()
                obj.country = response['country' + str(i)].strip()
                obj.save()
        else:
            if 'city' + str(i) in response:
                city = response['city' + str(i)].strip()
                province = response['province' + str(i)].strip()
                country = response['country' + str(i)].strip()
                obj = Extra_Loctaions(user=user, city=city, province=province, country=country, location_number=i)
                obj.save()


def save_secondary_locations(user, response):
    for i in range(1, 5):
        if 'city' + str(i) in response:
            city = response['city' + str(i)].strip()
            province = response['province' + str(i)].strip()
            country = response['country' + str(i)].strip()
            obj = Extra_Loctaions(user=user, city=city, province=province, country=country, location_number=i)
            obj.save()


def get_selected_sports_type(request):
    data = {}
    if request.method == "POST":
        selected_category = request.POST['selected_category_text']
        try:
            selected_type = SportsType.objects.filter(sports_category__sports_catgeory_text=selected_category)
            # print(selected_type)
        except Exception:
            data['error_message'] = 'error'
            return JsonResponse(data)
        return JsonResponse(list(selected_type.values('pk', 'sports_type_text')), safe=False)


def get_sports_category(request):
    data = {}
    if request.method == "GET":
        try:
            selected_type = SportsCategory.objects.all()
        except Exception:
            data['error_message'] = 'error'
            return JsonResponse(data)
        return JsonResponse(list(selected_type.values('pk', 'sports_catgeory_text')), safe=False)


def get_selected_sports_skill(request):
    data = {}
    if request.method == "POST":
        sport_position = request.POST['selected_position_text']
        selected_sport = request.POST['selected_type_text']
        # print(selected_sport, sport_position)
        try:
            selected_skills = PositionAndSkillType.objects.filter(sports_type__sports_type_text=selected_sport).filter(
                position_type=sport_position).values('pk', 'skill_type').distinct('skill_type')
            # print(selected_skills)
        except Exception:
            data['error_message'] = 'error'
            return JsonResponse(data)
        return JsonResponse(list(selected_skills.values('pk', 'skill_type')), safe=False)


def get_selected_sports_positions(request):
    data = {}
    if request.method == "POST":
        selected_sport = request.POST['selected_type_text']
        # print(selected_sport)
        try:
            selected_skills = PositionAndSkillType.objects.filter(sports_type__sports_type_text=selected_sport).values(
                'pk', 'position_type').distinct('position_type')
        except Exception:
            data['error_message'] = 'error'
            return JsonResponse(data)
        return JsonResponse(list(selected_skills.values('pk', 'position_type')), safe=False)


@login_required
def organization_profile(request):
    context = {
        'user': request.user
    }
    if request.method == "GET":
        organization = Organization.objects.get(user=request.user)
        # print(organization.__dict__)
        context['organization'] = organization
        return render(request, 'registration/organization_view.html', context)

    if request.method == "POST":
        organization = Organization.objects.filter(user=request.user)
        response = request.POST.dict()
        if organization.exists():
            organization = Organization.objects.get(user=request.user)
            organization.user = request.user
            if response["type_of_organization"]:
                organization.type_of_organization = response["type_of_organization"].strip() if response[
                    "type_of_organization"] else ""
            if response["company_name"]:
                organization.organization_name = response["company_name"].strip() if response["company_name"] else ""
            if response["parent_organization"]:
                organization.parent_organization_name = response["parent_organization"].strip() if response[
                    "parent_organization"] else ""
            if response["registration"]:
                organization.registration_no = response["registration"].strip() if response["registration"] else ""
            if response["year_established"]:
                organization.year_established = response["year_established"].strip() if response[
                    "year_established"] else ""
            if response["street_name"]:
                organization.street = response["street_name"].strip() if response["street_name"] else ""
            if response["city"]:
                organization.city = response["city"].strip() if response["city"] else ""
            if response["province"]:
                organization.province = response["province"].strip() if response["province"] else ""
            if response["country"]:
                organization.country = response["country"].strip() if response["country"] else ""
            if response["postal_code"]:
                organization.postal_code = response["postal_code"].strip() if response["postal_code"] else ""
            if response["email"]:
                organization.email = response["email"].strip() if response["email"] else ""
            if response["phone"]:
                phone = response["phone"].strip()
                phone = ''.join(i for i in phone if i.isdigit())
                organization.phone = phone
            if response["website"]:
                organization.website = response["website"].strip() if response["website"] else ""
            if response["gender"]:
                organization.gender_focus = response["gender"].strip() if response["gender"] else ""
            if response["age_group"]:
                organization.age_group = response["age_group"].strip() if response["age_group"] else ""
            organization.save()
            context['organization'] = organization
        else:
            obj = Organization()
            obj.user = request.user
            if response["type_of_organization"]:
                obj.type_of_organization = response["type_of_organization"].strip() if response[
                    "type_of_organization"] else ""
            if response["company_name"]:
                obj.organization_name = response["company_name"].strip() if response["company_name"] else ""
            if response["parent_organization"]:
                obj.parent_organization_name = response["parent_organization"].strip() if response[
                    "parent_organization"] else ""
            if response["registration"]:
                obj.registration_no = response["registration"].strip() if response["registration"] else ""
            if response["year_established"]:
                obj.year_established = response["year_established"].strip() if response["year_established"] else ""
            if response["street_name"]:
                obj.street = response["street_name"].strip() if response["street_name"] else ""
            if response["city"]:
                obj.city = response["city"].strip() if response["city"] else ""
            if response["province"]:
                obj.province = response["province"].strip() if response["province"] else ""
            if response["country"]:
                obj.country = response["country"].strip() if response["country"] else ""
            if response["postal_code"]:
                obj.postal_code = response["postal_code"].strip() if response["postal_code"] else ""
            if response["email"]:
                obj.email = response["email"].strip() if response["email"] else ""
            if response["phone"]:
                phone = response["phone"].strip()
                phone = ''.join(i for i in phone if i.isdigit())
                obj.phone = phone
            if response["website"]:
                obj.website = response["website"].strip() if response["website"] else ""
            if response["gender"]:
                obj.gender_focus = response["gender"].strip() if response["gender"] else ""
            if response["age_group"]:
                obj.age_group = response["age_group"].strip() if response["age_group"] else ""
            obj.save()
            context['organization'] = obj
        messages.success(request, 'Organization details updated!')
    return render(request, 'registration/organization_view.html', context)


def home(request):
    # Individual.objects.filter(pk=16).delete()
    sports = SportsCategory.objects.values('pk', 'sports_catgeory_text').order_by('sports_catgeory_text')
    if request.user.is_authenticated and request.user.is_individual:
        user_sports = Secondary_SportsChoice.objects.filter(user=request.user).values('sport_category')
        for item in sports:
            flag = False
            for item2 in user_sports:
                if item['sports_catgeory_text'] == item2['sport_category']:
                    flag = True

            if not flag:
                sports = sports.exclude(sports_catgeory_text=item['sports_catgeory_text'])

    venues = Venues.objects.values('pk', 'vm_name')
    events = master_table.objects.all()

    events = format_time(events)

    recommended_events = []
    if request.user.is_authenticated:
        recommended_events = get_recommended_events(request)

    # print(request.GET.getlist('events_types'))

    if request.GET.get('events_types'):
        selected_events_types = request.GET.get('events_types')
        # events = events.filter(Q(event_type__icontains=selected_events_types))
        events = events.filter(event_type=selected_events_types)

    if request.GET.get('sports'):
        selected_sports = request.GET.get('sports')
        events = events.filter(sport_type=selected_sports)

    if request.GET.get('venues'):
        selected_venues = request.GET.get('venues')
        events = events.filter(venue=selected_venues)

    if request.GET.get('date_range'):
        selected_date = request.GET.get('date_range')
        selected_date = datetime.strptime(selected_date.strip(), '%Y-%m-%d').date()
        events = get_events_by_date(events, selected_date)

    if request.user.is_authenticated:
        recommended_events = [recommended_events[i:i + 3] for i in range(0, len(recommended_events), 3)]

    events = [events[i:i + 3] for i in range(0, len(events), 3)]
    context = {
        'sports_list': sports,
        'venues_list': venues,
        'events': events,
        'recommended_events': recommended_events
    }
    html_template = loader.get_template('EventsApp/home.html')
    return HttpResponse(html_template.render(context, request))


def get_recommended_events(request):
    user = User.objects.get(username=request.user.username)
    user_avaiability = Availability.objects.filter(user=user)
    events = master_table.objects.all()
    week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    recommended_events = set()

    # FILTER by DateTime
    for event in events:
        if event.datetimes:
            time = event.datetimes.split("-")
            start_datetime = datetime.strptime(time[0].strip(), '%m/%d/%Y %I:%M %p')
            end_datetime = datetime.strptime(time[-1].strip(), '%m/%d/%Y %I:%M %p')

            for i in range((end_datetime - start_datetime).days):
                days_between = calendar.day_name[(start_datetime + timedelta(days=i + 1)).weekday()]
                for avail in user_avaiability:
                    if week_days[avail.day_of_week - 1] == days_between:
                        if avail.start_time <= end_datetime.time() or avail.end_time >= start_datetime.time():
                            recommended_events.add(event)

    recommended_events = list(recommended_events)

    # FILTER BY Location
    locations_saved = Extra_Loctaions.objects.filter(user=user)
    loc_list = []
    for item in locations_saved:
        loc_list.append(item.city.lower())

    for event in recommended_events:
        if event.city:
            if event.city.lower() not in loc_list:
                recommended_events.remove(event)

    recommended_events = list(recommended_events)

    # FILTER BY Age
    if user.is_individual:
        individual = Individual.objects.get(user=user)
        if individual.dob:
            dob = datetime.strptime(individual.dob, '%Y-%m-%d').date()
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            for event in recommended_events:
                positions = Events_PositionInfo.objects.filter(event=event)
                age_fail_count = 0
                for position in positions:
                    if position.max_age >= age >= position.min_age:
                        print(position.max_age, position.min_age)
                    else:
                        age_fail_count = age_fail_count + 1

                if age_fail_count == len(positions):
                    recommended_events.remove(event)

    # FILTER BY Gender, Skill, position,

    return list(recommended_events)


def format_time(events):
    for event in events:
        if event.datetimes:
            time = event.datetimes.split("-")
            start_time = datetime.strptime(time[0].strip(), '%m/%d/%Y %I:%M %p').time()
            end_time = datetime.strptime(time[-1].strip(), '%m/%d/%Y %I:%M %p').time()
            start_time = start_time.strftime("%I:%M %p")
            end_time = end_time.strftime('%I:%M %p')

            start_date = datetime.strptime(time[0].strip(), '%m/%d/%Y %I:%M %p').date()
            end_date = datetime.strptime(time[-1].strip(), '%m/%d/%Y %I:%M %p').date()
            start_date = start_date.strftime("%B %d, %Y")
            end_date = end_date.strftime("%B %d, %Y")
            if start_date == end_date:
                str_datetime = start_date + " " + start_time + " to " + end_time
            else:
                str_datetime = start_date + " " + start_time + " to " + end_date + " " + end_time

            event.datetimes = str_datetime
    return events


def get_events_by_date(events, selected_date):
    for event in events:
        time = event.datetimes.split("-")
        start_date = datetime.strptime(time[0].strip(), '%m/%d/%Y %I:%M %p').date()
        end_date = datetime.strptime(time[-1].strip(), '%m/%d/%Y %I:%M %p').date()
        if selected_date < start_date or selected_date > end_date:
            events = events.exclude(pk=event.id)

    return events


@login_required
def event_details(request, event_id):
    context = {}
    event = master_table.objects.get(pk=event_id)
    event_postions = Events_PositionInfo.objects.filter(event=event_id)
    context['event'] = event
    context['event_postions'] = event_postions

    if request.method == 'POST':
        # print(request.POST.dict())
        response = request.POST.dict()
        for key in response:
            if 'chk' in key:
                idx = key.split("_")[-1]
                position_id = response['posId_' + idx]
                pos_type = response['posType_' + idx]
                needed_pos = response['needed_' + idx]
                no_of_pos = response['noOfPos_' + idx]
                pos_cost = response['cost_' + idx]
                # print(pos_type, needed_pos, no_of_pos, pos_cost)
                ## Add to cart
                cart = Cart()
                cart.event = master_table.objects.get(pk=event_id)
                cart.user = User.objects.get(username=request.user.username)
                cart.position_id = Events_PositionInfo.objects.get(pk=position_id)
                cart.date = date.today()
                cart.position_type = pos_type
                cart.no_of_position = needed_pos
                cart.position_cost = pos_cost
                cart.total_cost = int(pos_cost) * int(needed_pos)
                cart.save()

                ## Update Inventory
                event_pos = Events_PositionInfo.objects.get(pk=position_id)
                event_pos.no_of_position = int(event_pos.no_of_position) - int(needed_pos)
                event_pos.save()

                ## Email Creator - New Subscriber
                event_subject = "New subscriber for Event: " + event.event_title
                event_message = "A new user has subscribed to event: " + event.event_title + "\n" + \
                                "Subscriber Name: " + request.user.first_name + " " + request.user.last_name + "\n" + \
                                "Subscriber Email: " + request.user.email + "\n" + \
                                "Subscriber User Name: " + request.user.username
                if event.created_by:
                    util.email(event_subject, event_message, [event.created_by.email])
                return redirect('EventsApp:cart_summary')

    return render(request, "EventsApp/detail_dashboard.html", context)


@login_required
def cart_summary(request):
    context = {}
    total = 0
    user = request.user
    context['STRIPE_PUBLISHABLE_KEY'] = settings.STRIPE_PUBLISHABLE_KEY,
    cart = Cart.objects.filter(user=user)
    for item in cart:
        total = total + item.total_cost
    context["cart"] = cart
    context["total"] = total
    return render(request, "EventsApp/cart_summary.html", context)


@csrf_exempt
def create_checkout_session(request, id):
    user = request.user
    cart = Cart.objects.filter(user=user)
    name = cart[0].event.event_title
    event = cart[0].event
    total = 0
    for item in cart:
        total = total + item.total_cost

    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'cad',
                        'product_data': {
                            'name': name,
                        },
                        'unit_amount': int(total),
                    },
                    'quantity': 1,
                }
            ],
            mode='payment',
            success_url=request.build_absolute_uri(
                reverse('EventsApp:payment-success')) + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.build_absolute_uri(reverse('EventsApp:payment-cancel')),
        )

        order = Order()
        order.customer = User.objects.get(username=request.user.username)
        order.event = event
        order.order_date = timezone.now()
        order.order_amount = int(total)
        order.save()

        return JsonResponse({'sessionId': checkout_session.id})

    except Exception as e:
        print(str(e))
        return JsonResponse({'error': str(e)})


def paymentSuccess(request):
    print("Success ho gaya")
    context = {
        "payment_status": "success"
    }
    return render(request, "EventsApp/confirmation.html", context)


def paymentCancel(request):
    print("cancel ho gaya")
    context = {
        "payment_status": "fail"
    }
    return render(request, "EventsApp/confirmation.html", context)


@login_required
def add_availability(request):
    context = {}
    form = AvailabilityForm(request.POST or None,
                            instance=Availability(),
                            initial={'user': request.user})

    context['form'] = form
    user = User.objects.get(username=request.user.username)
    user_avaiability = Availability.objects.filter(user=user)
    get_day_of_week(user_avaiability)

    context["user_availability"] = user_avaiability

    if request.POST:
        if form.is_valid():
            obj = Availability(user=user,
                               day_of_week=form.cleaned_data['day_of_week'],
                               start_time=form.cleaned_data['start_time'],
                               end_time=form.cleaned_data['end_time'])
            is_duplicate = check_duplicate_availability(user_avaiability, obj)
            if is_duplicate:
                messages.error(request, "Duplicate Availability!")
            else:
                obj.save()
                user_avaiability = Availability.objects.filter(user=user)
                get_day_of_week(user_avaiability)
                context["user_availability"] = user_avaiability
                messages.success(request, "New Availability Added!")
        else:
            messages.error(request, "Enter a valid time!")
            print(form.errors)

    form = AvailabilityForm()
    context['form'] = form
    return render(request, "EventsApp/add_availability.html", context)


def check_duplicate_availability(user_avaiability, new_availability):
    if new_availability.day_of_week == 1:
        new_availability.day_of_week = "Monday"
    if new_availability.day_of_week == 2:
        new_availability.day_of_week = "Tuesday"
    if new_availability.day_of_week == 3:
        new_availability.day_of_week = "Wednesday"
    if new_availability.day_of_week == 4:
        new_availability.day_of_week = "Thursday"
    if new_availability.day_of_week == 5:
        new_availability.day_of_week = "Friday"
    if new_availability.day_of_week == 6:
        new_availability.day_of_week = "Saturday"
    if new_availability.day_of_week == 7:
        new_availability.day_of_week = "Sunday"

    new_availability.start_time = new_availability.start_time.strftime("%H:%M:%S")
    new_availability.end_time = new_availability.end_time.strftime("%H:%M:%S")

    for avail in user_avaiability:
        if avail.day_of_week == new_availability.day_of_week and str(
                avail.start_time) == new_availability.start_time and str(avail.end_time) == new_availability.end_time:
            return True

    return False


@login_required
def notifications(request):
    context = {}
    form = AvailabilityForm(request.POST or None,
                            instance=Availability(),
                            initial={'user': request.user})

    context['form'] = form
    user = User.objects.get(username=request.user.username)
    user_avaiability = Availability.objects.filter(user=user)
    get_day_of_week(user_avaiability)

    context["user_availability"] = user_avaiability

    if request.POST:
        if form.is_valid():
            obj = Availability(user=user,
                               day_of_week=form.cleaned_data['day_of_week'],
                               start_time=form.cleaned_data['start_time'],
                               end_time=form.cleaned_data['end_time'])
            obj.save()
            user_avaiability = Availability.objects.filter(user=user)
            get_day_of_week(user_avaiability)
            context["user_availability"] = user_avaiability
            messages.success(request, "New Availability Added!")
        else:
            print(form.errors)

    return render(request, "EventsApp/add_availability.html", context)


def get_day_of_week(user_avaiability):
    for avail in user_avaiability:
        if avail.day_of_week == 1:
            avail.day_of_week = "Monday"
        if avail.day_of_week == 2:
            avail.day_of_week = "Tuesday"
        if avail.day_of_week == 3:
            avail.day_of_week = "Wednesday"
        if avail.day_of_week == 4:
            avail.day_of_week = "Thursday"
        if avail.day_of_week == 5:
            avail.day_of_week = "Friday"
        if avail.day_of_week == 6:
            avail.day_of_week = "Saturday"
        if avail.day_of_week == 7:
            avail.day_of_week = "Sunday"


def load_venues_excel():
    path = "./venue.xlsx"
    wb_obj = openpyxl.load_workbook(path)
    sheet_obj = wb_obj.active
    # Venues.objects.all().delete()
    for i in range(1, sheet_obj.max_row + 1):
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


def load_pos_skill_type():
    path = "./INsportify sport database.xlsx"
    wb_obj = openpyxl.load_workbook(path)
    sheet_obj = wb_obj.active
    for i in range(2, sheet_obj.max_row + 1):
        sports_category = SportsCategory.objects.get(sports_catgeory_text=sheet_obj.cell(row=i, column=1).value.strip())
        try:
            sports_type = SportsType.objects.get(sports_type_text=sheet_obj.cell(row=i, column=2).value.strip())
            position = sheet_obj.cell(row=i, column=3).value.strip()
            skill = sheet_obj.cell(row=i, column=4).value.strip()
            obj = PositionAndSkillType(sports_category=sports_category,
                                       sports_type=sports_type,
                                       position_type=position,
                                       skill_type=skill)
            print(i, sports_category, sports_type, obj)
            obj.save()
        except SportsType.DoesNotExist:
            s = SportsType(sports_category=sports_category,
                           sports_type_text=sheet_obj.cell(row=i, column=2).value.strip())
            s.save()
        # obj.save()


@login_required
def delete_by_id(request, event_id):
    try:
        event = master_table.objects.get(pk=event_id)
        event.delete()
        user = User.objects.get(username=request.user.username)
        event_subject = "Event Cancelled - " + event.event_title
        event_data = " Event Title: " + event.event_title + "\n Event Description: " \
                     + event.description + "\n Event Location: " + event.venue + ", " + event.city \
                     + "\n Event Dates: " + \
                     (event.datetimes if not event.is_recurring else (
                                                                         "\nMon: " + event.datetimes_monday if event.datetimes_monday is not None else "")
                                                                     + (
                                                                         "\nTue: " + event.datetimes_tuesday if event.datetimes_tuesday is not None else "")
                                                                     + (
                                                                         "\nWed: " + event.datetimes_wednesday if event.datetimes_wednesday is not None else "")
                                                                     + (
                                                                         "\nThu: " + event.datetimes_thursday if event.datetimes_thursday is not None else "")
                                                                     + (
                                                                         "\nFri: " + event.datetimes_friday if event.datetimes_friday is not None else "")
                                                                     + (
                                                                         "\nSat: " + event.datetimes_saturday if event.datetimes_saturday is not None else "")
                                                                     + (
                                                                         "\nSun: " + event.datetimes_sunday if event.datetimes_sunday is not None else "")
                                                                     + (
                                                                         "\nExc: " + event.datetimes_exceptions if event.datetimes_exceptions is not None else ""))

        for cart_item in Cart.objects.filter(event=event):
            subs_email = cart_item.user.email
            util.email(event_subject, "Hello " + user.first_name + " " + user.last_name
                       + ", the following subscribed event in your cart has been cancelled by the creator:\n\n"
                       + event_data
                       , [subs_email])
        for order_item in Order.objects.filter(event=event):
            order_email = order_item.customer.email
            util.email(event_subject, "Hello " + user.first_name + " " + user.last_name
                       + ", the following event has been cancelled by the creator:\n\n" + event_data
                       , [order_email])
        util.email(event_subject, "Hello " + user.first_name + " " + user.last_name
                   + ", the following event has been cancelled as requested (subscribers and customers have been "
                     "notified):\n\n" + event_data
                   , [user.email])
        messages.success(request, "Event removed successfully!")

    except Exception as e:
        print(e)

    return redirect('EventsApp:list-events')


@login_required
def invite_by_id(request, event_id):
    context = {}
    form = InviteForm(request.POST or None,
                      instance=Invite(),
                      initial={'user': request.user})

    context['form'] = form
    user = User.objects.get(username=request.user.username)
    event = master_table.objects.get(pk=event_id)
    context["event"] = event
    context["invites"] = Invite.objects.all().filter(event=event)

    if request.POST:
        if form.is_valid():
            obj = Invite(user=user,
                         event=event,
                         email=form.cleaned_data['email'])
            obj.save()
            if user.first_name and user.last_name:
                full_name = user.first_name + " " + user.last_name
            else:
                full_name = ""
            util.email("Invitation from Insportify", "Hi there! " + full_name
                       + " has invited you to the event: " + event.event_title
                       + ". Join Insportify now: " + request.get_host() + "/" + str(event_id),
                       [form.cleaned_data['email']])
            context["invites"] = Invite.objects.all().filter(event=event)
        else:
            print(form.errors)

    return render(request, "EventsApp/invite.html", context)


@login_required
def invite(request):
    context = {}
    form = InviteForm(request.POST or None,
                      instance=Invite(),
                      initial={'user': request.user})

    context['form'] = form
    user = User.objects.get(username=request.user.username)
    context["invites"] = Invite.objects.all().filter(user=user)

    if request.POST:
        if form.is_valid():
            obj = Invite(user=user,
                         event=None,
                         email=form.cleaned_data['email'])
            obj.save()
            if user.first_name and user.last_name:
                full_name = user.first_name + " " + user.last_name
            else:
                full_name = ""
            util.email("Invitation from Insportify", "Hi there! " + full_name
                       + " has invited you to Insportify! Join Now: " + "http://127.0.0.1:8000/",
                       [form.cleaned_data['email']])
            context["invites"] = Invite.objects.all().filter(user=user)
        else:
            print(form.errors)

    return render(request, "EventsApp/invite.html", context)


@login_required
def delete_availability(request, id):
    try:
        avail = Availability.objects.get(pk=id)
        avail.delete()
        messages.success(request, "Availability removed successfully!")

    except:
        print("Some error occurred!")

    return redirect('EventsApp:add_availability')


@login_required
def logo_upload_view(request):
    if request.method == 'POST':
        img_obj = ""
        form = LogoForm(request.POST, request.FILES)
        if form.is_valid():
            if Logo.objects.filter(user=request.user).exists():
                img_obj = Logo.objects.get(user=request.user)
                img_obj.image = form.instance.image
                img_obj.save()
            else:
                obj = form.save(commit=False)
                obj.user = request.user
                obj.save()
            return render(request, 'EventsApp/add_logo.html', {'form': form, 'img_obj': img_obj})
    else:
        img_obj = ""
        form = LogoForm()
        if Logo.objects.filter(user=request.user).exists():
            img_obj = Logo.objects.get(user=request.user)

    return render(request, 'EventsApp/add_logo.html', {'form': form, 'img_obj': img_obj})
