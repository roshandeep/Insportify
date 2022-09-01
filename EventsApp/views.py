import calendar
from datetime import datetime, timedelta, date

import openpyxl
import stripe
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from Insportify import settings
from .forms import MultiStepForm, AvailabilityForm, LogoForm, InviteForm
from .models import master_table, Individual, Organization, Venues, SportsCategory, SportsType, Order, User, \
    Availability, Logo, Extra_Loctaions, Events_PositionInfo, Secondary_SportsChoice, Invite, \
    PositionAndSkillType, SportsImage, Organization_Availability, OrderItems
import util

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def multistep(request):
    sports_type = SportsType.objects.all().order_by('sports_type_text')
    venues = Venues.objects.all().order_by('vm_name')
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
            obj.sport_type = request.POST['sport_type']
            obj.venue = request.POST['venue']
            obj.street = request.POST['street']
            obj.city = request.POST['city']
            obj.country = request.POST['country']
            obj.province = request.POST['province']
            obj.zipcode = request.POST['zip_code']
            # obj.position = request.POST['position']
            obj.gender = ','.join(item for item in request.POST.getlist('gender'))
            obj.is_recurring = request.POST.get('recurring_event') == "Yes"
            selected_days = request.POST.getlist('recurring_days')
            obj.datetimes_monday = ""
            obj.datetimes_tuesday = ""
            obj.datetimes_wednesday = ""
            obj.datetimes_thursday = ""
            obj.datetimes_friday = ""
            obj.datetimes_saturday = ""
            obj.datetimes_sunday = ""
            if obj.is_recurring and 'Monday' in selected_days:
                date = request.POST.get('datetimes_monday_date').split("-")
                start_date = date[0].strip()
                end_date = date[1].strip()
                # print(start_date, end_date)
                ts = datetime.strptime(request.POST.get('datetimes_monday_start_time'), "%H:%M").strftime("%I:%M %p")
                te = datetime.strptime(request.POST.get('datetimes_monday_end_time'), "%H:%M").strftime("%I:%M %p")
                obj.datetimes_monday = start_date + " " + ts + " - " + end_date + " " + te
            if obj.is_recurring and 'Tuesday' in selected_days:
                date = request.POST.get('datetimes_tuesday_date').split("-")
                start_date = date[0].strip()
                end_date = date[1].strip()
                ts = datetime.strptime(request.POST.get('datetimes_tuesday_start_time'), "%H:%M").strftime("%I:%M %p")
                te = datetime.strptime(request.POST.get('datetimes_tuesday_end_time'), "%H:%M").strftime("%I:%M %p")
                obj.datetimes_tuesday = start_date + " " + ts + " - " + end_date + " " + te
            if obj.is_recurring and 'Wednesday' in selected_days:
                date = request.POST.get('datetimes_wednesday_date').split("-")
                start_date = date[0].strip()
                end_date = date[1].strip()
                ts = datetime.strptime(request.POST.get('datetimes_wednesday_start_time'), "%H:%M").strftime("%I:%M %p")
                te = datetime.strptime(request.POST.get('datetimes_wednesday_end_time'), "%H:%M").strftime("%I:%M %p")
                obj.datetimes_wednesday = start_date + " " + ts + " - " + end_date + " " + te
            if obj.is_recurring and 'Thursday' in selected_days:
                date = request.POST.get('datetimes_thursday_date').split("-")
                start_date = date[0].strip()
                end_date = date[1].strip()
                ts = datetime.strptime(request.POST.get('datetimes_thursday_start_time'), "%H:%M").strftime("%I:%M %p")
                te = datetime.strptime(request.POST.get('datetimes_thursday_end_time'), "%H:%M").strftime("%I:%M %p")
                obj.datetimes_thursday = start_date + " " + ts + " - " + end_date + " " + te
            if obj.is_recurring and 'Friday' in selected_days:
                date = request.POST.get('datetimes_friday_date').split("-")
                start_date = date[0].strip()
                end_date = date[1].strip()
                ts = datetime.strptime(request.POST.get('datetimes_friday_start_time'), "%H:%M").strftime("%I:%M %p")
                te = datetime.strptime(request.POST.get('datetimes_friday_end_time'), "%H:%M").strftime("%I:%M %p")
                obj.datetimes_friday = start_date + " " + ts + " - " + end_date + " " + te
            if obj.is_recurring and 'Saturday' in selected_days:
                date = request.POST.get('datetimes_saturday_date').split("-")
                start_date = date[0].strip()
                end_date = date[1].strip()
                ts = datetime.strptime(request.POST.get('datetimes_saturday_start_time'), "%H:%M").strftime("%I:%M %p")
                te = datetime.strptime(request.POST.get('datetimes_saturday_end_time'), "%H:%M").strftime("%I:%M %p")
                obj.datetimes_saturday = start_date + " " + ts + " - " + end_date + " " + te
            if obj.is_recurring and 'Sunday' in selected_days:
                date = request.POST.get('datetimes_sunday_date').split("-")
                start_date = date[0].strip()
                end_date = date[1].strip()
                ts = datetime.strptime(request.POST.get('datetimes_sunday_start_time'), "%H:%M").strftime("%I:%M %p")
                te = datetime.strptime(request.POST.get('datetimes_sunday_end_time'), "%H:%M").strftime("%I:%M %p")
                obj.datetimes_sunday = start_date + " " + ts + " - " + end_date + " " + te
            obj.datetimes_exceptions = request.POST.get('datetimes_exceptions') if obj.is_recurring else ""
            obj.datetimes = ""
            if not obj.is_recurring:
                date = request.POST.get('datetimes_date')
                ts = datetime.strptime(request.POST.get('datetimes_start_time'), "%H:%M").strftime("%I:%M %p")
                te = datetime.strptime(request.POST.get('datetimes_end_time'), "%H:%M").strftime("%I:%M %p")
                obj.datetimes = date + " " + ts + " - " + date + " " + te
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
            or not request.POST.get('venue'):
        messages.error(request, "All fields are required, please enter valid information")
        fields_valid = False
    if not request.POST.get('recurring_event'):
        messages.error(request, "Please select event recurrence")
        date_valid = False
    else:
        if request.POST['recurring_event'] == "Yes":
            selected_days = request.POST.getlist('recurring_days')
            if len(selected_days) < 1:
                messages.error(request, "Please select event days.")
                date_valid = False
            monday_valid = True
            if 'Monday' in selected_days and \
                    (((not request.POST.get('datetimes_monday_date')) or request.POST['datetimes_monday_date'] == "") or
                     ((not request.POST.get('datetimes_monday_start_time')) or request.POST[
                         'datetimes_monday_start_time'] == "") or
                     ((not request.POST.get('datetimes_monday_end_time')) or request.POST[
                         'datetimes_monday_end_time'] == "")):
                messages.error(request, "Invalid date-time selection for Monday, please enter valid dates and times.")
                monday_valid = False
            tuesday_valid = True
            if 'Tuesday' in selected_days and \
                    (((not request.POST.get('datetimes_tuesday_date')) or request.POST[
                        'datetimes_tuesday_date'] == "") or
                     ((not request.POST.get('datetimes_tuesday_start_time')) or request.POST[
                         'datetimes_tuesday_start_time'] == "") or
                     ((not request.POST.get('datetimes_tuesday_end_time')) or request.POST[
                         'datetimes_tuesday_end_time'] == "")):
                messages.error(request, "Invalid date-time selection for Tuesday, please enter valid dates and times.")
                tuesday_valid = False
            wednesday_valid = True
            if 'Wednesday' in selected_days and \
                    (((not request.POST.get('datetimes_wednesday_date')) or request.POST[
                        'datetimes_wednesday_date'] == "") or
                     ((not request.POST.get('datetimes_wednesday_start_time')) or request.POST[
                         'datetimes_wednesday_start_time'] == "") or
                     ((not request.POST.get('datetimes_wednesday_end_time')) or request.POST[
                         'datetimes_wednesday_end_time'] == "")):
                messages.error(request,
                               "Invalid date-time selection for Wednesday, please enter valid dates and times.")
                wednesday_valid = False
            thursday_valid = True
            if 'Thursday' in selected_days and \
                    (((not request.POST.get('datetimes_thursday_date')) or request.POST[
                        'datetimes_thursday_date'] == "") or
                     ((not request.POST.get('datetimes_thursday_start_time')) or request.POST[
                         'datetimes_thursday_start_time'] == "") or
                     ((not request.POST.get('datetimes_thursday_end_time')) or request.POST[
                         'datetimes_thursday_end_time'] == "")):
                messages.error(request, "Invalid date-time selection for Thursday, please enter valid dates and times.")
                thursday_valid = False
            friday_valid = True
            if 'Friday' in selected_days and \
                    (((not request.POST.get('datetimes_friday_date')) or request.POST[
                        'datetimes_friday_date'] == "") or
                     ((not request.POST.get('datetimes_friday_start_time')) or request.POST[
                         'datetimes_friday_start_time'] == "") or
                     ((not request.POST.get('datetimes_friday_end_time')) or request.POST[
                         'datetimes_friday_end_time'] == "")):
                messages.error(request, "Invalid date-time selection for Friday, please enter valid dates and times.")
                friday_valid = False
            saturday_valid = True
            if 'Saturday' in selected_days and \
                    (((not request.POST.get('datetimes_saturday_date')) or request.POST[
                        'datetimes_saturday_date'] == "") or
                     ((not request.POST.get('datetimes_saturday_start_time')) or request.POST[
                         'datetimes_saturday_start_time'] == "") or
                     ((not request.POST.get('datetimes_saturday_end_time')) or request.POST[
                         'datetimes_saturday_end_time'] == "")):
                messages.error(request, "Invalid date-time selection for Saturday, please enter valid dates and times.")
                saturday_valid = False
            sunday_valid = True
            if 'Sunday' in selected_days and \
                    (((not request.POST.get('datetimes_sunday_date')) or request.POST[
                        'datetimes_sunday_date'] == "") or
                     ((not request.POST.get('datetimes_sunday_start_time')) or request.POST[
                         'datetimes_sunday_start_time'] == "") or
                     ((not request.POST.get('datetimes_sunday_end_time')) or request.POST[
                         'datetimes_sunday_end_time'] == "")):
                messages.error(request, "Invalid date-time selection for Sunday, please enter valid dates and times.")
                sunday_valid = False
            date_valid = date_valid and sunday_valid and monday_valid and tuesday_valid and wednesday_valid and thursday_valid \
                         and friday_valid and saturday_valid
        else:
            if ((not request.POST.get('datetimes_date')) or request.POST['datetimes_date'] == "") or \
                    ((not request.POST.get('datetimes_start_time')) or request.POST['datetimes_start_time'] == "") or \
                    ((not request.POST.get('datetimes_end_time')) or request.POST['datetimes_end_time'] == ""):
                messages.error(request, "No date times entered, please enter a date and time for the event")
                date_valid = False
    for i in range(1, 10):
        if request.POST.get('no_of_position' + str(i)) != '' \
                and (request.POST.get('type_of_skill' + str(i)) == ''
                     or request.POST.get('position_cost' + str(i)) == ''
                     or request.POST.get('min_age' + str(i)) == ''
                     or request.POST.get('max_age' + str(i)) == ''):
            messages.error(request, "All position fields are required, please enter valid information")
            fields_valid = False

    return date_valid and event_count_valid and fields_valid


def ValidateUserProfileForm(request, context):
    valid = True
    if not request.POST.get('first_name') or request.POST['first_name'].strip() == "":
        messages.error(request, "Please enter First Name")
        valid = False
    if not request.POST.get('last_name') or request.POST['last_name'].strip() == "":
        messages.error(request, "Please enter Last Name")
        valid = False
    if not request.POST.get('dob') or request.POST['dob'].strip() == "":
        messages.error(request, "Please enter Date of Birth")
        valid = False
    if not request.POST.get('contact_email') or request.POST['contact_email'].strip() == "":
        messages.error(request, "Please enter Contact Email")
        valid = False
    if not request.POST.get('mobile') or request.POST['mobile'].strip() == "":
        messages.error(request, "Please enter Mobile")
        valid = False
    if not request.POST.get('interest_gender') or request.POST['interest_gender'].strip() == "":
        messages.error(request, "Please select Event gender preferences")
        valid = False

    # if len(context['locations']) == 0:
    if not request.POST.get('city') or request.POST['city'].strip() == "":
        messages.error(request, "Please enter City")
        valid = False
    if not request.POST.get('province') or request.POST['province'].strip() == "":
        messages.error(request, "Please enter Province")
        valid = False
    if not request.POST.get('country') or request.POST['country'].strip() == "":
        messages.error(request, "Please enter Country")
        valid = False

    # if not request.POST.get('sport_type') or request.POST['sport_type'].strip() == "":
    #     messages.error(request, "Please select Sports you facilitate")
    #     valid = False
    # if not request.POST.get('position') or request.POST['position'].strip() == "":
    #     messages.error(request, "Please select Position")
    #     valid = False
    # if not request.POST.get('skill') or request.POST['skill'].strip() == "":
    #     messages.error(request, "Please select Skill")
    #     valid = False

    return valid


def ValidateOrgProfileForm(request, context):
    valid = True
    if not request.POST.get('company_name') or request.POST['company_name'].strip() == "":
        messages.error(request, "Please enter Organization Name")
        valid = False
    if not request.POST.get('registration') or request.POST['registration'].strip() == "":
        messages.error(request, "Please enter Registration Number")
        valid = False
    if not request.POST.get('email') or request.POST['email'].strip() == "":
        messages.error(request, "Please enter Contact Email")
        valid = False
    if not request.POST.get('phone') or request.POST['phone'].strip() == "":
        messages.error(request, "Please enter Contact Phone Number")
        valid = False
    # if len(context['locations']) == 0:
    if not request.POST.get('street_name') or request.POST['street_name'].strip() == "":
        messages.error(request, "Please enter Street Name")
        valid = False
    if not request.POST.get('city') or request.POST['city'].strip() == "":
        messages.error(request, "Please enter City")
        valid = False
    if not request.POST.get('province') or request.POST['province'].strip() == "":
        messages.error(request, "Please enter Province")
        valid = False
    if not request.POST.get('country') or request.POST['country'].strip() == "":
        messages.error(request, "Please enter Country")
        valid = False
    if not request.POST.get('postal_code') or request.POST['postal_code'].strip() == "":
        messages.error(request, "Please enter Postal Code")
        valid = False
    if not request.POST.get('gender') or request.POST['gender'].strip() == "":
        messages.error(request, "Please select Focus")
        valid = False
    if not request.POST.get('age_group') or request.POST['age_group'].strip() == "":
        messages.error(request, "Please select Age Group")
        valid = False
    if not request.POST.get('sport_type') or request.POST['sport_type'].strip() == "":
        messages.error(request, "Please select Sports you facilitate")
        valid = False

    return valid


def get_venue_details(request):
    data = {}
    if request.method == "POST":
        selected_venue = request.POST['selected_venue']
        try:
            selected_venue = Venues.objects.filter(vm_name=selected_venue).order_by('vm_name')
            # print(selected_venue)
        except Exception:
            data['error_message'] = 'error'
            return JsonResponse(data)
        return JsonResponse(list(selected_venue.values()), safe=False)


def save_event_position_info(request, event):
    for i in range(1, 10):
        if 'no_of_position' + str(i) in request.POST and request.POST['no_of_position' + str(i)].strip() != "":
            position_name = request.POST['position_name' + str(i)].strip()
            position_type = request.POST['type_of_skill' + str(i)].strip()
            no_of_position = request.POST['no_of_position' + str(i)].strip()
            position_cost = request.POST['position_cost' + str(i)].strip()
            min_age = request.POST['min_age' + str(i)].strip()
            max_age = request.POST['max_age' + str(i)].strip() if request.POST['max_age' + str(i)] else "999"
            print(request.POST['min_age' + str(i)].strip(), request.POST['max_age' + str(i)].strip())
            obj = Events_PositionInfo(event=event, position_name=position_name, max_age=max_age, min_age=min_age,
                                      no_of_position=no_of_position,
                                      position_cost=position_cost, position_number=i, position_type=position_type)
            obj.save()


@login_required
def all_events(request):
    event_list = master_table.objects.filter(created_by=request.user)
    event_list = format_time(event_list)
    # load_pos_skill_type()
    return render(request, 'EventsApp/event_list.html', {'event_list': event_list})


@login_required
def committed_events(request):
    event_list = set()

    cart = OrderItems.objects.filter(user=request.user)
    if len(cart) > 0:
        for item in cart:
            event = master_table.objects.get(pk=item.event.pk)
            event_list.add(event)
        event_list = format_time(event_list)
    return render(request, 'EventsApp/events_committed.html', {'event_list': list(event_list)})



@login_required
def user_profile(request):
    context = {
        'user': request.user
    }
    sports_type = SportsType.objects.all().order_by('sports_type_text')
    sec_sport_choices = Secondary_SportsChoice.objects.filter(user=request.user).order_by("sport_type")
    locations = Extra_Loctaions.objects.filter(user=request.user).order_by("city")
    user_avaiability = Availability.objects.filter(user=request.user)
    get_day_of_week(user_avaiability)
    context['sports_type'] = sports_type
    context['sec_sport_choices'] = sec_sport_choices
    context['locations'] = locations
    context['user_avaiability'] = user_avaiability
    if request.method == "GET":
        individual = Individual.objects.get(user=request.user)
        # print(individual.__dict__)
        context['individual'] = individual
        return render(request, 'registration/individual_view.html', context)

    elif request.method == "POST":
        individual = Individual.objects.filter(user=request.user)
        response = request.POST.dict()
        if not ValidateUserProfileForm(request, context):
            individual = Individual.objects.get(user=request.user)
            context['individual'] = individual
            return render(request, 'registration/individual_view.html', context)
        if individual.exists():
            individual = Individual.objects.get(user=request.user)
            individual.user = request.user
            if "first_name" in response:
                individual.first_name = response["first_name"].strip() if response["first_name"] else ""
            if "last_name" in response:
                individual.last_name = response["last_name"].strip() if response["last_name"] else ""
            if "mobile" in response:
                mobile = response["mobile"].strip()
                mobile = ''.join(i for i in mobile if i.isdigit())
                individual.phone = mobile
            if "contact_email" in response:
                individual.email = response["contact_email"].strip() if response["contact_email"] else ""
            if "website" in response:
                individual.website = response["website"].strip()
            if "job_title" in response:
                individual.job_title = response["job_title"].strip()
            if "dob" in response:
                individual.dob = response["dob"].strip() if response["dob"] else ""
            if "is_concussion" in response:
                individual.concussion = response["is_concussion"].strip()
            if "is_student" in response:
                individual.is_student = response["is_student"].strip()
            if "interest_gender" in response:
                individual.participation_interest = ','.join(item for item in request.POST.getlist('interest_gender'))
            if "city" in response:
                individual.city = response["city"].strip() if response["city"] else ""
            if "province" in response:
                individual.province = response["province"].strip() if response["province"] else ""
            if "country" in response:
                individual.country = response["country"].strip() if response["country"] else ""
            if "contact_email" in response:
                individual.contact_email = response["contact_email"].strip() if response["contact_email"] else ""
            if "sport_type" in response:
                individual.sports_type = response["sport_type"].strip() if response["sport_type"] else ""
            if "position" in response:
                individual.sports_position = response["position"].strip() if response["position"] else ""
            if "skill" in response:
                individual.sports_skill = response["skill"].strip() if response["skill"] else ""
            individual.save()
            context['individual'] = individual
        else:
            obj = Individual()
            obj.user = request.user
            if "first_name" in response:
                obj.first_name = response["first_name"].strip() if response["first_name"] else ""
            if "last_name" in response:
                obj.last_name = response["last_name"].strip() if response["last_name"] else ""
            if "mobile" in response:
                mobile = response["mobile"].strip()
                mobile = ''.join(i for i in mobile if i.isdigit())
                obj.phone = mobile
            if "contact_email" in response:
                obj.email = response["contact_email"].strip() if response["contact_email"] else ""
            if "dob" in response:
                obj.dob = response["dob"].strip() if response["dob"] else ""
            if "is_concussion" in response:
                obj.concussion = response["is_concussion"].strip()
            if "is_student" in response:
                obj.is_student = response["is_student"].strip()
            if "interest_gender" in response:
                obj.participation_interest = ','.join(item for item in request.POST.getlist('interest_gender'))
            if "city" in response:
                obj.city = response["city"].strip() if response["city"] else ""
            if "province" in response:
                obj.province = response["province"].strip() if response["province"] else ""
            if "country" in response:
                obj.country = response["country"].strip() if response["country"] else ""
            if "sport_type" in response:
                obj.sports_type = response["sport_type"].strip() if response["sport_type"] else ""
            if "position" in response:
                obj.sports_position = response["position"].strip() if response["position"] else ""
            if "skill" in response:
                obj.sports_skill = response["skill"].strip() if response["skill"] else ""

            obj.save()
            context['individual'] = obj
        messages.success(request, 'Individual details updated!')

    return render(request, 'registration/individual_view.html', context)


def add_sports_positions(request):
    if request.method == "POST":
        selected_sport = request.POST['selected_sport_text']
        selected_position = request.POST['selected_position_text']
        selected_skill = request.POST['selected_skill_text']
        # print(selected_skill, selected_position, selected_sport)
        try:
            if Secondary_SportsChoice.objects.filter(user=request.user, sport_type=selected_sport,
                                                     position=selected_position, skill=selected_skill).exists():
                return JsonResponse({'status': 'Duplicate Position cannot be added!'}, safe=False)
            else:
                obj = Secondary_SportsChoice(user=request.user, sport_type=selected_sport,
                                             position=selected_position, skill=selected_skill)
                obj.save()
            return JsonResponse({'status': 'New Position added!'}, safe=False)
        except Exception:
            return JsonResponse({'status': 'An error occured!'}, safe=False)


def fetch_user_sports_positions(request):
    if request.is_ajax():
        position_choices = Secondary_SportsChoice.objects.filter(user=request.user).order_by("sport_type")
        position_choices = list(position_choices.values("sport_type", "position", "skill", "pk"))
        return JsonResponse(position_choices, safe=False)


def delete_sports_choice(request):
    if request.POST:
        try:
            id = request.POST['id']
            obj = Secondary_SportsChoice.objects.get(pk=id)
            obj.delete()
            return JsonResponse({'status': 'Sports Choice removed successfully!'}, safe=False)
        except:
            return JsonResponse({'status': 'Some error occurred!'}, safe=False)


def add_user_locations(request):
    if request.method == "POST":
        selected_city = request.POST['selected_city_text'].strip() if request.POST['selected_city_text'] else ""
        selected_province = request.POST['selected_province_text'].strip() if request.POST[
            'selected_province_text'] else ""
        selected_country = request.POST['selected_country_text'].strip() if request.POST[
            'selected_country_text'] else ""
        # print(selected_city, selected_province, selected_country)
        try:
            if selected_city != "" and selected_province != "" and selected_country != "":
                if Extra_Loctaions.objects.filter(user=request.user, city=selected_city,
                                                  province=selected_province, country=selected_country).exists():
                    return JsonResponse({'status': 'Duplicate Location cannot be added!'}, safe=False)
                else:
                    obj = Extra_Loctaions(user=request.user, city=selected_city,
                                          province=selected_province, country=selected_country)
                    obj.save()
                return JsonResponse({'status': 'New Location added!'}, safe=False)
            else:
                return JsonResponse({'status': 'Missing values!'}, safe=False)
        except Exception:
            return JsonResponse({'status': 'An error occured!'}, safe=False)


def fetch_user_locations(request):
    if request.is_ajax():
        location_choices = Extra_Loctaions.objects.filter(user=request.user).order_by("city")
        location_choices = list(location_choices.values("city", "province", "country", "pk"))
        return JsonResponse(location_choices, safe=False)


def delete_user_location(request):
    if request.POST:
        try:
            id = request.POST['id']
            # print(id)
            obj = Extra_Loctaions.objects.get(pk=id)
            obj.delete()
            return JsonResponse({'status': 'Location removed successfully!'}, safe=False)
        except:
            return JsonResponse({'status': 'Some error occurred!'}, safe=False)


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


def get_sports_type(request):
    data = {}
    if request.method == "GET":
        try:
            sports_type = SportsType.objects.all().order_by('sports_type_text')
        except Exception:
            data['error_message'] = 'error'
            return JsonResponse(data)
        return JsonResponse(list(sports_type.values('pk', 'sports_type_text')), safe=False)


def get_selected_sports_position_and_skill(request):
    data = {}
    data_list = []
    if request.method == "POST":
        selected_sport = request.POST['selected_type_text']
        try:
            positions = PositionAndSkillType.objects.filter(sports_type__sports_type_text=selected_sport).values(
                'position_type').distinct('position_type')
            for position in positions:
                skills = PositionAndSkillType.objects.filter(position_type=position.position_type).values(
                    'pk', 'skill_type').distinct('skill_type')

                print(position.position_type, skills)
            print(data_list)
        except Exception:
            data['error_message'] = 'error'
            return JsonResponse(data)
        return JsonResponse()


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
        locations = Extra_Loctaions.objects.filter(user=request.user).order_by("city")
        sports_type = SportsType.objects.all().order_by('sports_type_text')
        context['locations'] = locations
        context['sports_type'] = sports_type
        context['organization'] = organization
        return render(request, 'registration/organization_view.html', context)

    if request.method == "POST":
        organization = Organization.objects.filter(user=request.user)
        locations = Extra_Loctaions.objects.filter(user=request.user).order_by("city")
        sports_type = SportsType.objects.all().order_by('sports_type_text')
        context['locations'] = locations
        context['sports_type'] = sports_type
        response = request.POST.dict()
        if not ValidateOrgProfileForm(request, context):
            organization = Organization.objects.get(user=request.user)
            context['organization'] = organization
            return render(request, 'registration/organization_view.html', context)
        if organization.exists():
            organization = Organization.objects.get(user=request.user)
            organization.user = request.user
            if "type_of_organization" in response:
                organization.type_of_organization = response["type_of_organization"].strip() if response[
                    "type_of_organization"] else ""
            if "company_name" in response:
                organization.organization_name = response["company_name"].strip() if response["company_name"] else ""
            if "parent_organization" in response:
                organization.parent_organization_name = response["parent_organization"].strip() if response[
                    "parent_organization"] else ""
            if "registration" in response:
                organization.registration_no = response["registration"].strip() if response["registration"] else ""
            if "year_established" in response:
                organization.year_established = response["year_established"].strip() if response[
                    "year_established"] else ""
            if "street_name" in response:
                organization.street = response["street_name"].strip() if response["street_name"] else ""
            if "city" in response:
                organization.city = response["city"].strip() if response["city"] else ""
            if "province" in response:
                organization.province = response["province"].strip() if response["province"] else ""
            if "country" in response:
                organization.country = response["country"].strip() if response["country"] else ""
            if "postal_code" in response:
                organization.postal_code = response["postal_code"].strip() if response["postal_code"] else ""
            if "email" in response:
                organization.email = response["email"].strip() if response["email"] else ""
            if "phone" in response:
                phone = response["phone"].strip()
                phone = ''.join(i for i in phone if i.isdigit())
                organization.phone = phone
            if "website" in response:
                organization.website = response["website"].strip() if response["website"] else ""
            if "gender" in response:
                organization.gender_focus = ','.join(item for item in request.POST.getlist('gender'))
            if "age_group" in response:
                organization.age_group = ','.join(item for item in request.POST.getlist('age_group'))
            if "participants" in response:
                organization.participants = response["participants"].strip() if response["participants"] else ""
            if "sport_type" in response:
                save_organization_sports(request.user, request.POST.getlist('sport_type'))
            save_organization_timings(request.user, response)
            organization.save()
            context['organization'] = organization
        else:
            obj = Organization()
            obj.user = request.user
            if "type_of_organization" in response:
                obj.type_of_organization = response["type_of_organization"].strip() if response[
                    "type_of_organization"] else ""
            if "company_name" in response:
                obj.organization_name = response["company_name"].strip() if response["company_name"] else ""
            if "parent_organization" in response:
                obj.parent_organization_name = response["parent_organization"].strip() if response[
                    "parent_organization"] else ""
            if "registration" in response:
                obj.registration_no = response["registration"].strip() if response["registration"] else ""
            if "year_established" in response:
                obj.year_established = response["year_established"].strip() if response["year_established"] else ""
            if "street_name" in response:
                obj.street = response["street_name"].strip() if response["street_name"] else ""
            if "city" in response:
                obj.city = response["city"].strip() if response["city"] else ""
            if "province" in response:
                obj.province = response["province"].strip() if response["province"] else ""
            if "country" in response:
                obj.country = response["country"].strip() if response["country"] else ""
            if "postal_code" in response:
                obj.postal_code = response["postal_code"].strip() if response["postal_code"] else ""
            if "email" in response:
                obj.email = response["email"].strip() if response["email"] else ""
            if "phone" in response:
                phone = response["phone"].strip()
                phone = ''.join(i for i in phone if i.isdigit())
                obj.phone = phone
            if "website" in response:
                obj.website = response["website"].strip() if response["website"] else ""
            if "gender" in response:
                obj.gender_focus = ','.join(item for item in request.POST.getlist('gender'))
            if "age_group" in response:
                obj.age_group = ','.join(item for item in request.POST.getlist('age_group'))
            if "participants" in response:
                organization.participants = response["participants"].strip() if response["participants"] else ""
            if "sport_type" in response:
                save_organization_sports(request.user, request.POST.getlist('sport_type'))
            save_organization_timings(request.user, response)
            obj.save()
            context['organization'] = obj
        messages.success(request, 'Organization details updated!')
    return render(request, 'registration/organization_view.html', context)


def save_organization_timings(user, response):
    if "sunday_start_time" in response and response["sunday_start_time"] != "" and "sunday_end_time" in response and \
            response["sunday_end_time"] != "":
        if Organization_Availability.objects.filter(user=user, day_of_week="Sunday").exists():
            obj = Organization_Availability.objects.get(user=user, day_of_week="Sunday")
            obj.start_time = response["sunday_start_time"]
            obj.end_time = response["sunday_end_time"]
            obj.save()
        else:
            obj = Organization_Availability(user=user, day_of_week="Sunday", start_time=response["sunday_start_time"],
                                            end_time=response["sunday_end_time"])
            obj.save()
    if "monday_start_time" in response and response["monday_start_time"] != "" and "monday_end_time" in response and \
            response["monday_end_time"] != "":
        if Organization_Availability.objects.filter(user=user, day_of_week="Monday").exists():
            obj = Organization_Availability.objects.get(user=user, day_of_week="Monday")
            obj.start_time = response["monday_start_time"]
            obj.end_time = response["monday_end_time"]
            obj.save()
        else:
            obj = Organization_Availability(user=user, day_of_week="Monday", start_time=response["monday_start_time"],
                                            end_time=response["monday_end_time"])
            obj.save()
    if "tuesday_start_time" in response and response["tuesday_start_time"] != "" and "tuesday_end_time" in response and \
            response["tuesday_end_time"] != "":
        if Organization_Availability.objects.filter(user=user, day_of_week="Tuesday").exists():
            obj = Organization_Availability.objects.get(user=user, day_of_week="Tuesday")
            obj.start_time = response["tuesday_start_time"]
            obj.end_time = response["tuesday_end_time"]
            obj.save()
        else:
            obj = Organization_Availability(user=user, day_of_week="Tuesday", start_time=response["tuesday_start_time"],
                                            end_time=response["tuesday_end_time"])
            obj.save()
    if "wednesday_start_time" in response and response[
        "wednesday_start_time"] != "" and "wednesday_end_time" in response and response["wednesday_end_time"] != "":
        if Organization_Availability.objects.filter(user=user, day_of_week="Wednesday").exists():
            obj = Organization_Availability.objects.get(user=user, day_of_week="Wednesday")
            obj.start_time = response["wednesday_start_time"]
            obj.end_time = response["wednesday_end_time"]
            obj.save()
        else:
            obj = Organization_Availability(user=user, day_of_week="Wednesday",
                                            start_time=response["wednesday_start_time"],
                                            end_time=response["wednesday_end_time"])
            obj.save()
    if "thursday_start_time" in response and response[
        "thursday_start_time"] != "" and "thursday_end_time" in response and response["thursday_end_time"] != "":
        if Organization_Availability.objects.filter(user=user, day_of_week="Thursday").exists():
            obj = Organization_Availability.objects.get(user=user, day_of_week="Thursday")
            obj.start_time = response["thursday_start_time"]
            obj.end_time = response["thursday_end_time"]
            obj.save()
        else:
            obj = Organization_Availability(user=user, day_of_week="Thursday",
                                            start_time=response["thursday_start_time"],
                                            end_time=response["thursday_end_time"])
            obj.save()
    if "friday_start_time" in response and response["friday_start_time"] != "" and "friday_end_time" in response and \
            response["friday_end_time"] != "":
        if Organization_Availability.objects.filter(user=user, day_of_week="Friday").exists():
            obj = Organization_Availability.objects.get(user=user, day_of_week="Friday")
            obj.start_time = response["friday_start_time"]
            obj.end_time = response["friday_end_time"]
            obj.save()
        else:
            obj = Organization_Availability(user=user, day_of_week="Friday",
                                            start_time=response["friday_start_time"],
                                            end_time=response["friday_end_time"])
            obj.save()
    if "saturday_start_time" in response and response[
        "saturday_start_time"] != "" and "saturday_end_time" in response and response["saturday_end_time"] != "":
        if Organization_Availability.objects.filter(user=user, day_of_week="Saturday").exists():
            obj = Organization_Availability.objects.get(user=user, day_of_week="Saturday")
            obj.start_time = response["saturday_start_time"]
            obj.end_time = response["saturday_end_time"]
            obj.save()
        else:
            obj = Organization_Availability(user=user, day_of_week="Saturday",

                                            start_time=response["saturday_start_time"],
                                            end_time=response["saturday_end_time"])
            obj.save()


def get_organization_timings(request):
    if request.is_ajax():
        availability = Organization_Availability.objects.filter(user=request.user)
        availability = list(availability.values("day_of_week", "start_time", "end_time", "pk"))
        return JsonResponse(availability, safe=False)


def save_organization_sports(user, sport_type_list):
    user_choice = Secondary_SportsChoice.objects.filter(user=user)
    # Remove the sport choces from DB if they have been removed from current list
    if len(user_choice):
        for item in user_choice:
            if item.sport_type not in sport_type_list:
                Secondary_SportsChoice.objects.filter(id=item.pk).delete()

    # Add/Update sport choices for user
    for sport in sport_type_list:
        if not Secondary_SportsChoice.objects.filter(user=user, sport_type=sport).exists():
            obj = Secondary_SportsChoice(user=user, sport_type=sport)
            obj.save()
    return


def add_organization_locations(request):
    if request.method == "POST":
        selected_street = request.POST['selected_street_text'].strip() if request.POST['selected_street_text'] else ""
        selected_city = request.POST['selected_city_text'].strip() if request.POST['selected_city_text'] else ""
        selected_province = request.POST['selected_province_text'].strip() if request.POST[
            'selected_province_text'] else ""
        selected_country = request.POST['selected_country_text'].strip() if request.POST[
            'selected_country_text'] else ""
        selected_zipcode = request.POST['selected_zipcode_text'].strip() if request.POST[
            'selected_zipcode_text'] else ""

        try:
            if selected_city != "" and selected_province != "" and selected_country != "" and selected_zipcode != "":
                if Extra_Loctaions.objects.filter(user=request.user, street=selected_street, city=selected_city,
                                                  province=selected_province, country=selected_country,
                                                  zipcode=selected_zipcode).exists():
                    return JsonResponse({'status': 'Duplicate Location cannot be added!'}, safe=False)
                else:
                    obj = Extra_Loctaions(user=request.user, street=selected_street, city=selected_city,
                                          province=selected_province, country=selected_country,
                                          zipcode=selected_zipcode)
                    obj.save()
                return JsonResponse({'status': 'New Location added!'}, safe=False)
            else:
                return JsonResponse({'status': 'Missing values!'}, safe=False)
        except Exception:
            return JsonResponse({'status': 'An error occured!'}, safe=False)


def fetch_organization_locations(request):
    if request.is_ajax():
        location_choices = Extra_Loctaions.objects.filter(user=request.user).order_by("city")
        location_choices = list(location_choices.values("street", "city", "province", "country", "zipcode", "pk"))
        return JsonResponse(location_choices, safe=False)


def home(request):
    # Individual.objects.filter(pk=16).delete()
    sports = SportsType.objects.values('pk', 'sports_type_text').order_by('sports_type_text')

    if request.user.is_authenticated and request.user.is_individual:
        user_sports = Secondary_SportsChoice.objects.filter(user=request.user).values('sport_type')
        for item in sports:
            flag = False
            for item2 in user_sports:
                if item['sports_type_text'] == item2['sport_type']:
                    flag = True

            if not flag:
                sports = sports.exclude(sports_type_text=item['sports_type_text'])

    venues = Venues.objects.values('pk', 'vm_name').order_by('vm_name')
    events = master_table.objects.all()

    events = format_time(events)

    recommended_events = []
    if request.user.is_authenticated:
        recommended_events = get_recommended_events(request)

    recommended_events = format_time(recommended_events)
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
        for event in recommended_events:
            sport_img = SportsImage.objects.filter(sport=event.sport_type).values("img")
            if len(sport_img):
                event.sport_logo = "/media/" + sport_img[0]["img"]
            else:
                event.sport_logo = "/media/images/Multisport.jpg"

    recommended_events = [recommended_events[i:i + 3] for i in range(0, len(recommended_events), 3)]

    for event in events:
        sport_img = SportsImage.objects.filter(sport=event.sport_type).values("img")
        if len(sport_img):
            event.sport_logo = "/media/" + sport_img[0]["img"]
        else:
            event.sport_logo = "/media/images/Multisport.jpg"

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
    user = User.objects.get(email=request.user.email)
    user_avaiability = Availability.objects.filter(user=user)
    events = master_table.objects.all()
    week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    locations_saved = Extra_Loctaions.objects.filter(user=user)
    loc_list = [item.city.lower() for item in locations_saved]
    recommended_events = set()

    # FILTER by DateTime
    # If there is no user availability then add all events to recommended events
    if len(user_avaiability):
        # print(user_avaiability)
        for event in events:
            event_date, event_start_time, event_end_time = extract_event_datetime(event)
            if event_date is not None and event_start_time is not None and event_end_time is not None:

                for avail in user_avaiability:
                    if avail.day_of_week == (event_date.weekday() + 1):
                        # print(event.event_title, avail.start_time, avail.end_time, event_start_time, event_end_time, event_start_time >= avail.start_time, event_end_time <= avail.end_time)
                        if event_start_time >= avail.start_time and event_end_time <= avail.end_time:
                            recommended_events.add(event)

            else:
                recommended_events.add(event)
    else:
        recommended_events = [event for event in events]

    recommended_events = list(recommended_events)
    print("Availability Filter", recommended_events)

    # FILTER BY Location
    for event in recommended_events[:]:
        if event.city is not None:
            if event.city.lower() not in loc_list:
                recommended_events.remove(event)

    recommended_events = list(recommended_events)
    print("Location Filter", recommended_events)

    # FILTER BY Age
    if user.is_individual:
        individual = Individual.objects.get(user=user)
        if individual.dob:
            dob = datetime.strptime(individual.dob, '%Y-%m-%d').date()
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            for event in recommended_events[:]:
                positions = Events_PositionInfo.objects.filter(event=event)
                age_fail_count = 0
                for position in positions:
                    if position.max_age >= age >= position.min_age:
                        continue
                    else:
                        age_fail_count = age_fail_count + 1

                if age_fail_count == len(positions):
                    recommended_events.remove(event)

    print("Age Filter", recommended_events)

    # FILTER BY Gender
    if user.is_individual:
        individual = Individual.objects.get(user=user)
        individual_gender = []
        if individual.participation_interest and individual.participation_interest != "":
            # print(individual.participation_interest)
            individual_gender = individual.participation_interest.split(",")
        # print(individual_gender)
        for event in recommended_events[:]:
            flag = 0
            if event.gender:
                gender_list = event.gender.split(",")
                for item in individual_gender:
                    if item in gender_list:
                        flag = flag + 1
                        # print(event.event_title, gender_list, individual_gender, flag, item)

                if flag == 0:
                    # print(event.event_title, gender_list, individual_gender, flag)
                    recommended_events.remove(event)

    print("Gender Filter", recommended_events)

    # FILTER BY Sports
    sport_choices = Secondary_SportsChoice.objects.filter(user=user).order_by("sport_type")
    sports_list = []
    for item in sport_choices:
        sports_list.append(item.sport_type)

    for event in recommended_events[:]:
        if event.sport_type not in sports_list:
            recommended_events.remove(event)

    print("Sports Filter", recommended_events)

    # FILTER BY Positions
    if user.is_individual:
        position_choices = Secondary_SportsChoice.objects.filter(user=user)
        position_list = []
        for item in position_choices:
            position_list.append(item.position)

        for event in recommended_events[:]:
            event_positions_list = Events_PositionInfo.objects.filter(event=event.pk)
            flag = 0
            for item in event_positions_list:
                if item.position_name not in position_list:
                    flag = flag + 1

            if flag > 0:
                recommended_events.remove(event)

    print("Positions Filter", recommended_events)

    # FILTER BY Skills
    if user.is_individual:
        skill_choices = Secondary_SportsChoice.objects.filter(user=user)
        skill_list = []
        for item in skill_choices:
            skill_list.append(item.skill)

        for event in recommended_events[:]:
            event_skill_list = Events_PositionInfo.objects.filter(event=event.pk)
            flag = 0
            for item in event_skill_list:
                if item.position_type not in skill_list:
                    flag = flag + 1

            if flag > 0:
                recommended_events.remove(event)

    print("Skills Filter", recommended_events)

    return list(recommended_events)


def extract_event_datetime(event):
    event_date = None
    event_start_time = None
    event_end_time = None

    if event.datetimes:
        time = event.datetimes.split("-")
    elif event.datetimes_monday:
        time = event.datetimes_monday.split("-")
    elif event.datetimes_tuesday:
        time = event.datetimes_tuesday.split("-")
    elif event.datetimes_wednesday:
        time = event.datetimes_wednesday.split("-")
    elif event.datetimes_thursday:
        time = event.datetimes_thursday.split("-")
    elif event.datetimes_friday:
        time = event.datetimes_friday.split("-")
    elif event.datetimes_saturday:
        time = event.datetimes_saturday.split("-")
    elif event.datetimes_sunday:
        time = event.datetimes_sunday.split("-")

    # print(event.event_title, time, type(time))
    if time is not None and time != "":
        event_start_datetime = datetime.strptime(time[0].strip(), '%m/%d/%Y %I:%M %p')
        event_end_datetime = datetime.strptime(time[-1].strip(), '%m/%d/%Y %I:%M %p')
        event_date = event_start_datetime.date()
        event_start_time = event_start_datetime.time()
        event_end_time = event_end_datetime.time()

        return event_date, event_start_time, event_end_time

    return event_date, event_start_time, event_end_time


def format_time(events):
    for event in events:
        if event.datetimes:
            time = event.datetimes.split("-")
        elif event.datetimes_monday:
            time = event.datetimes_monday.split("-")
        elif event.datetimes_tuesday:
            time = event.datetimes_tuesday.split("-")
        elif event.datetimes_wednesday:
            time = event.datetimes_wednesday.split("-")
        elif event.datetimes_thursday:
            time = event.datetimes_thursday.split("-")
        elif event.datetimes_friday:
            time = event.datetimes_friday.split("-")
        elif event.datetimes_saturday:
            time = event.datetimes_saturday.split("-")
        elif event.datetimes_sunday:
            time = event.datetimes_sunday.split("-")

        # print(event.event_title, time, type(time))
        if time is not None and time != "":
            start_time = datetime.strptime(time[0].strip(), '%m/%d/%Y %I:%M %p').time()
            end_time = datetime.strptime(time[-1].strip(), '%m/%d/%Y %I:%M %p').time()
            start_time = start_time.strftime("%I:%M %p")
            end_time = end_time.strftime('%I:%M %p')

            start_date = datetime.strptime(time[0].strip(), '%m/%d/%Y %I:%M %p').date()
            end_date = datetime.strptime(time[-1].strip(), '%m/%d/%Y %I:%M %p').date()
            start_date = start_date.strftime("%B %d")
            end_date = end_date.strftime("%B %d")
            if start_date == end_date:
                str_datetime = start_date + " from " + start_time + " - " + end_time
            else:
                str_datetime = start_date + " - " + end_date + " from " + start_time + " - " + end_time

            if event.datetimes:
                event.datetimes = str_datetime
            elif event.datetimes_monday:
                event.datetimes_monday = str_datetime
            elif event.datetimes_tuesday:
                event.datetimes_tuesday = str_datetime
            elif event.datetimes_wednesday:
                event.datetimes_wednesday = str_datetime
            elif event.datetimes_thursday:
                event.datetimes_thursday = str_datetime
            elif event.datetimes_friday:
                event.datetimes_friday = str_datetime
            elif event.datetimes_saturday:
                event.datetimes_saturday = str_datetime
            elif event.datetimes_sunday:
                event.datetimes_sunday = str_datetime

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
        print(request.POST.dict())
        response = request.POST.dict()
        for key in response:
            if 'chk' in key:
                print(key)
                idx = key.split("_")[-1]
                position_id = response['posId_' + idx]
                pos_name = response['posName_' + idx]
                skill = response['skill_' + idx]
                needed_pos = response['needed_' + idx]
                no_of_pos = response['noOfPos_' + idx]
                pos_cost = response['cost_' + idx]
                ## Add to cart
                cart = OrderItems()
                cart.event = master_table.objects.get(pk=event_id)
                cart.user = User.objects.get(email=request.user.email)
                cart.position_id = Events_PositionInfo.objects.get(pk=position_id)
                cart.date = date.today()
                cart.position_type = pos_name
                cart.skill = skill
                cart.no_of_position = needed_pos
                cart.position_cost = pos_cost
                cart.total_cost = int(pos_cost) * int(needed_pos)
                cart.checkout_timer = datetime.now(timezone.utc)
                cart.save()

                # Update Inventory
                event_pos = Events_PositionInfo.objects.get(pk=position_id)
                event_pos.no_of_position = int(event_pos.no_of_position) - int(needed_pos)
                event_pos.save()

                # Email Creator - New Subscriber
                event_subject = "New subscriber for Event: " + event.event_title
                event_message = "A new user has subscribed to event: " + event.event_title + "\n" + \
                                "Subscriber Name: " + request.user.first_name + " " + request.user.last_name + "\n" + \
                                "Subscriber Email: " + request.user.email + "\n"
                # if event.created_by:
                #     util.email(event_subject, event_message, [event.created_by.email])

                messages.info(request, "Order Items will be present in your cart for only 30 mins!")

        return redirect('EventsApp:cart_summary')

    return render(request, "EventsApp/detail_dashboard.html", context)

@csrf_exempt
def delete_cart_item(request):
    if request.POST:
        try:
            event_pos_id = request.POST['event_pos_id']
            cart_item_id = request.POST['cart_item_id']
            # print(event_pos_id, cart_item_id)
            order_item = OrderItems.objects.get(pk=cart_item_id)
            evnt_pos_info = Events_PositionInfo.objects.get(pk=event_pos_id)
            evnt_pos_info.no_of_position = evnt_pos_info.no_of_position + order_item.no_of_position
            evnt_pos_info.save()
            order_item.delete()
            return JsonResponse({'status': 'Order Item deleted!'}, safe=False)
        except:
            return JsonResponse({'status': 'Some error occurred!'}, safe=False)


def fetch_cart_items(request):
    total = 0
    order_items = []
    remove_expired_cart_items(request)
    if request.is_ajax():
        cart = OrderItems.objects.filter(user=request.user, purchased=False)
        for item in cart:
            total = total + item.total_cost

        for item in cart:
            order_items.append({
                'event_title': item.event.event_title,
                'position_type': item.position_type,
                'no_of_position': item.no_of_position,
                'position_cost': item.position_cost,
                'position_id': item.position_id.pk,
                'pk': item.pk,
            })
        return JsonResponse({"cart": order_items, "total": total}, safe=False)


def remove_expired_cart_items(request):
    cart = OrderItems.objects.filter(user=request.user, purchased=False)
    for item in cart:
        time_delta = (datetime.now(timezone.utc) - item.checkout_timer)
        total_mins = (time_delta.total_seconds()) / 60
        if total_mins > 30:
            order_item = OrderItems.objects.get(pk=item.pk)
            evnt_pos_info = Events_PositionInfo.objects.get(pk=item.position_id.pk)
            evnt_pos_info.no_of_position = evnt_pos_info.no_of_position + order_item.no_of_position
            evnt_pos_info.save()
            order_item.delete()


@login_required
def cart_summary(request):
    context = {}
    total = 0
    user = request.user
    remove_expired_cart_items(request)
    context['STRIPE_PUBLISHABLE_KEY'] = settings.STRIPE_PUBLISHABLE_KEY,
    cart = OrderItems.objects.filter(user=user, purchased=False)
    for item in cart:
        total = total + item.total_cost

    context["cart"] = cart
    context["total"] = total
    if request.method == 'POST':
        order_obj = Order.objects.filter(customer=request.user, payment=False)
        if order_obj.exists():
            order_obj = Order.objects.get(customer=request.user, payment=False)
            order_obj.items.clear()
            order_obj.order_amount = total
            order_obj.order_date = timezone.now()
            for order_items in cart:
                order_obj.items.add(order_items)
        else:
            order = Order()
            order.customer = User.objects.get(email=request.user.email)
            order.order_date = timezone.now()
            order.order_amount = total
            order.payment = False
            order.save()
            for order_items in cart:
                order.items.add(order_items)

        return redirect('EventsApp:charge')

    return render(request, "EventsApp/cart_summary.html", context)



@login_required
def charge(request):
    context={}
    user = request.user
    char_set = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    key = settings.STRIPE_PUBLISHABLE_KEY
    context['key'] = key
    order = Order.objects.get(customer=request.user, payment=False)
    cart = order.items.all()
    context["order"] = order
    context["cart"] = cart
    context['orderAmount'] = order.order_amount
    totalCents = order.order_amount * 100
    context['totalCents'] = totalCents
    print(cart)
    if request.method == 'POST':
        try:
            charge = stripe.Charge.create(amount=totalCents,
                                          currency='cad',
                                          description=order,
                                          source=request.POST['stripeToken'])
            print(charge)
            if charge.status == "succeeded":
                print('payment success')
                orderId = get_random_string(length=16, allowed_chars=char_set)
                paymentId = get_random_string(length=16, allowed_chars=char_set)
                order.orderId = f'#{request.user}{orderId}'
                order.paymentId = paymentId
                order.payment = True
                order.payment_method = "Card"
                for order_item in order.items.all():
                    item = OrderItems.objects.get(pk=order_item.pk)
                    item.purchased = True
                    item.save()

                order.save()

                return redirect('EventsApp:payment-success')

            elif charge.status == "failed":
                return redirect('EventsApp:payment-cancel')

        except Exception as e:
            print(e)

    return render(request, 'EventsApp/charge.html', context)


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


def pay_at_venue(request):
    context = {
        "payment_status": "VenuePay"
    }
    char_set = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    order = Order.objects.get(customer=request.user, payment=False)
    print(order.order_amount)
    orderId = get_random_string(length=16, allowed_chars=char_set)
    paymentId = get_random_string(length=16, allowed_chars=char_set)
    order.orderId = f'#{request.user}{orderId}'
    order.paymentId = paymentId
    order.payment = True
    order.payment_method = "Cash Pickup"
    for order_item in order.items.all():
        item = OrderItems.objects.get(pk=order_item.pk)
        item.purchased = True
        item.save()

    order.save()

    order_subject = "Order Confirmed: " + f'#{request.user}{orderId}'
    order_message = "Your seat has been reserved. Payment would be made on the day of the event. " + \
                    "Customer Name: " + request.user.first_name + " " + request.user.last_name + "\n" + \
                    "Customer Email: " + request.user.email + "\n"

    util.email(order_subject, order_message, [request.user.email])

    return render(request, "EventsApp/confirmation.html", context)


@login_required
def add_availability(request):
    context = {}
    form = AvailabilityForm(request.POST or None,
                            instance=Availability(),
                            initial={'user': request.user})

    context['form'] = form
    user = User.objects.get(email=request.user.email)
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


def get_user_availability(request):
    if request.is_ajax():
        user = User.objects.get(email=request.user.email)
        user_availability = Availability.objects.filter(user=user)
        user_availability = list(user_availability.values("day_of_week", "start_time", "end_time", "pk"))
        for avail in user_availability:
            if avail["day_of_week"] == 1:
                avail["day_of_week"] = "Monday"
            if avail["day_of_week"] == 2:
                avail["day_of_week"] = "Tuesday"
            if avail["day_of_week"] == 3:
                avail["day_of_week"] = "Wednesday"
            if avail["day_of_week"] == 4:
                avail["day_of_week"] = "Thursday"
            if avail["day_of_week"] == 5:
                avail["day_of_week"] = "Friday"
            if avail["day_of_week"] == 6:
                avail["day_of_week"] = "Saturday"
            if avail["day_of_week"] == 7:
                avail["day_of_week"] = "Sunday"

            avail["start_time"] = avail["start_time"].strftime("%I:%M %p")
            avail["end_time"] = avail["end_time"].strftime("%I:%M %p")

    return JsonResponse(user_availability, safe=False)


def add_user_availability(request):
    user = User.objects.get(email=request.user.email)
    user_avaiability = Availability.objects.filter(user=user)
    print(request.POST['start_time'])
    if request.method == "POST":
        obj = Availability(user=user,
                           day_of_week=request.POST['day_of_week'],
                           start_time=request.POST['start_time'],
                           end_time=request.POST['end_time'])
        is_duplicate = check_duplicate_availability(user_avaiability, obj)
        if is_duplicate:
            return JsonResponse({'status': 'Duplicate Availability!'}, safe=False)
        else:
            obj.save()
            user_avaiability = Availability.objects.filter(user=user)
            get_day_of_week(user_avaiability)
            return JsonResponse({'status': 'New Availability Added!'}, safe=False)
    else:
        return JsonResponse({'status': 'Enter a valid time!'}, safe=False)


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

    for avail in user_avaiability:
        if avail.day_of_week == int(new_availability.day_of_week) and \
                (new_availability.start_time >= avail.start_time.strftime("%H:%M") or \
                 new_availability.end_time <= avail.end_time.strftime("%H:%M")):
            return True

    return False


@login_required
def delete_availability(request):
    if request.POST:
        try:
            id = request.POST['id']
            avail = Availability.objects.get(pk=id)
            avail.delete()
            return JsonResponse({'status': 'Availability removed successfully!'}, safe=False)
        except:
            return JsonResponse({'status': 'Some error occurred!'}, safe=False)


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
            # print(i, sports_category, sports_type, obj)
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
        user = User.objects.get(email=request.user.email)
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

        for cart_item in OrderItems.objects.filter(event=event):
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
def invite_by_id(request, event_id, email=None):
    context = {}
    form = InviteForm(request.POST or None,
                      instance=Invite(),
                      initial={'user': request.user})

    context['form'] = form
    user = User.objects.get(email=request.user.email)
    event = master_table.objects.get(pk=event_id)
    context["event"] = event
    context["invites"] = Invite.objects.all().filter(event=event).distinct('email')

    if email:
        if user.first_name and user.last_name:
            full_name = user.first_name + " " + user.last_name
        else:
            full_name = ""
        util.email("Invitation from Insportify", "Hi there! " + full_name
                   + " has invited you to the event: " + event.event_title
                   + ". Join Insportify now: " + request.get_host() + "/" + str(event_id),
                   [email])
        messages.success(request, "Another invitation email sent to " + email)

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
            messages.success(request, "Invitation email sent to " + form.cleaned_data['email'])
            context["invites"] = Invite.objects.all().filter(event=event).distinct('email')
        else:
            messages.error(request, form.errors)

    return render(request, "EventsApp/invite.html", context)


@login_required
def invite(request):
    context = {}
    form = InviteForm(request.POST or None,
                      instance=Invite(),
                      initial={'user': request.user})

    context['form'] = form
    user = User.objects.get(email=request.user.email)
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
