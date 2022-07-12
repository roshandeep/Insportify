from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


class User(AbstractUser):
    is_individual = models.BooleanField(default=False)
    is_organization = models.BooleanField(default=False)
    first_name = models.CharField(max_length=40, null=True)
    last_name = models.CharField(max_length=40, null=True)
    is_active = models.BooleanField(default=False, null=True)
    is_mvp = models.BooleanField(default=False, null=True)



class master_table(models.Model):
    EVENT_TYPE_CHOICES = (('Camp', 'Camp'), ('Charity', 'Charity'), ('Conditioning', 'Conditioning'),
                          ('Development', 'Development'), ('Game/Session', 'Game/Session'), ('Online', 'Online'),
                          ('Registration', 'Registration'), ('Social', 'Social'), ('Tournament', 'Tournament'))

    event_title = models.CharField(max_length=300, blank=True, null=True)
    description = models.CharField(max_length=300, blank=True, null=True)
    event_type = models.CharField(max_length=300, choices=EVENT_TYPE_CHOICES, blank=True, null=True)
    datetimes = models.CharField(max_length=100, blank=True, null=True)
    is_recurring = models.BooleanField(default=False, null=True)
    datetimes_monday = models.CharField(max_length=100, blank=True, null=True)
    datetimes_tuesday = models.CharField(max_length=100, blank=True, null=True)
    datetimes_wednesday = models.CharField(max_length=100, blank=True, null=True)
    datetimes_thursday = models.CharField(max_length=100, blank=True, null=True)
    datetimes_friday = models.CharField(max_length=100, blank=True, null=True)
    datetimes_saturday = models.CharField(max_length=100, blank=True, null=True)
    datetimes_sunday = models.CharField(max_length=100, blank=True, null=True)
    datetimes_exceptions = models.CharField(max_length=500, blank=True, null=True)
    sport_type = models.CharField(max_length=300, blank=True, null=True)
    position = models.CharField(max_length=300, blank=True, null=True)
    city = models.CharField(max_length=300, blank=True, null=True)
    max_age = models.IntegerField(blank=True, null=True)
    min_age = models.IntegerField(blank=True, null=True)
    venue = models.CharField(max_length=300, blank=True, null=True)
    province = models.CharField(max_length=300, blank=True, null=True)
    country = models.CharField(max_length=300, blank=True, null=True)
    no_of_position = models.IntegerField(blank=True, null=True)
    position_cost = models.IntegerField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.event_title

    class Meta:
        managed = True
        db_table = 'master_table'


class Individual(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, null=True)
    dob = models.CharField(max_length=50, blank=True, null=True)
    concussion = models.CharField(max_length=100, blank=True, null=True)
    is_student = models.CharField(max_length=100, blank=True, null=True)
    participation_interest = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(verbose_name="City", max_length=50, blank=True, null=True)
    province = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=250, blank=True, null=True)
    sports_category = models.CharField(max_length=50, null=True)
    sports_type = models.CharField(max_length=50, null=True)
    sports_position = models.CharField(max_length=50, null=True)
    sports_skill = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.first_name


class Organization(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    organization_name = models.CharField(max_length=50, null=True)
    parent_organization_name = models.CharField(max_length=50, null=True)
    registration_no = models.CharField(max_length=50, null=True)
    type_of_organization = models.CharField(max_length=50, blank=True, null=True)
    year_established = models.CharField(max_length=50, blank=True, null=True)
    street = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    province = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=250, blank=True, null=True)
    postal_code = models.CharField(max_length=6, blank=True, null=True)
    phone = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, null=True)
    website = models.CharField(max_length=50, null=True)
    gender_focus = models.CharField(max_length=50, null=True)
    age_group = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.organization_name


class EventsappMasterTable(models.Model):
    id = models.BigAutoField(primary_key=True)
    event_title = models.CharField(max_length=30, blank=True, null=True)
    description = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    country = models.CharField(max_length=30, blank=True, null=True)
    datetimes = models.CharField(max_length=50, blank=True, null=True)
    event_type = models.IntegerField(blank=True, null=True)
    province = models.CharField(max_length=30, blank=True, null=True)
    skill = models.CharField(max_length=30, blank=True, null=True)
    sport_category = models.CharField(max_length=30, blank=True, null=True)
    sport_type = models.CharField(max_length=30, blank=True, null=True)
    venue = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'EventsApp_master_table'


class Venues(models.Model):
    vm_name = models.CharField(max_length=500, blank=True, null=True)
    vm_venue_description = models.CharField(max_length=500, blank=True, null=True)
    vm_venue_street = models.CharField(max_length=500, blank=True, null=True)
    vm_venuecity = models.CharField(max_length=500, blank=True, null=True)
    vm_venue_province = models.CharField(max_length=500, blank=True, null=True)
    vm_venue_country = models.CharField(max_length=500, blank=True, null=True)
    vm_venue_zip = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.vm_name


class SportsCategory(models.Model):
    sports_catgeory_text = models.CharField(max_length=100)

    def __str__(self):
        return self.sports_catgeory_text


class SportsType(models.Model):
    sports_category = models.ForeignKey(SportsCategory, on_delete=models.CASCADE)
    sports_type_text = models.CharField(max_length=100)

    def __str__(self):
        return self.sports_type_text


class PositionAndSkillType(models.Model):
    sports_category = models.ForeignKey(SportsCategory, on_delete=models.CASCADE)
    sports_type = models.ForeignKey(SportsType, on_delete=models.CASCADE)
    position_type = models.CharField(max_length=100)
    skill_type = models.CharField(max_length=100)

    def __str__(self):
        return self.position_type + ' ' + self.skill_type


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(master_table, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    order_amount = models.IntegerField()

    def __str__(self):
        return self.customer.first_name + " " + self.event.event_title


class Invite(models.Model):
    email = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(master_table, on_delete=models.CASCADE, blank=True, null=True)
    invite_date = models.DateField(null=True)


class Availability(models.Model):
    class Day(models.IntegerChoices):
        MONDAY = 1
        TUESDAY = 2
        WEDNESDAY = 3
        THURSDAY = 4
        FRIDAY = 5
        SATURDAY = 6
        SUNDAY = 7

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day_of_week = models.IntegerField(choices=Day.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()


class Logo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.user.first_name + "_logo"


class Events_PositionInfo(models.Model):
    event = models.ForeignKey(master_table, on_delete=models.CASCADE)
    position_number = models.IntegerField(blank=True, null=True)
    position_type = models.CharField(max_length=100, blank=True, null=True)
    max_age = models.IntegerField(blank=True, null=True)
    min_age = models.IntegerField(blank=True, null=True)
    no_of_position = models.IntegerField(blank=True, null=True)
    position_cost = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.event.event_title + " Position_" + str(self.position_number)


class Extra_Loctaions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location_number = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    province = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.user.first_name + " Location_" + str(self.location_number)


class Secondary_SportsChoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sport_entry_number = models.IntegerField(blank=True, null=True)
    sport_category = models.CharField(max_length=100, blank=True, null=True)
    sport_type = models.CharField(max_length=30, blank=True, null=True)
    position = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.user.first_name + " Sport_Choice_" + str(self.sport_entry_number)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(master_table, on_delete=models.CASCADE)
    position_id = models.ForeignKey(Events_PositionInfo, on_delete=models.CASCADE)
    date = models.DateField()
    position_type = models.CharField(max_length=100, blank=True, null=True)
    no_of_position = models.IntegerField(blank=True, null=True)
    position_cost = models.IntegerField(blank=True, null=True)
    total_cost = models.IntegerField(blank=True, null=True)
