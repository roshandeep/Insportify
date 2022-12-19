from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    is_individual = models.BooleanField(default=False)
    is_organization = models.BooleanField(default=False)
    first_name = models.CharField(max_length=40, null=True)
    last_name = models.CharField(max_length=40, null=True)
    is_active = models.BooleanField(default=False, null=True)
    is_mvp = models.BooleanField(default=False, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)


class master_table(models.Model):
    EVENT_TYPE_CHOICES = (('Camp', 'Camp'), ('Charity', 'Charity'), ('Conditioning', 'Conditioning'),
                          ('Development', 'Development'), ('Game/Session', 'Game/Session'), ('Online', 'Online'),
                          ('Registration', 'Registration'), ('Social', 'Social'), ('Tournament', 'Tournament'))
    REGISTRATION_TYPE_CHOICES = (('Drop-in', 'Drop-in'), ('Registration', 'Registration'))

    event_title = models.CharField(max_length=300, blank=True, null=True)
    description = models.CharField(max_length=300, blank=True, null=True)
    event_type = models.CharField(max_length=300, choices=EVENT_TYPE_CHOICES, blank=True, null=True)
    registration_type = models.CharField(max_length=300, choices=REGISTRATION_TYPE_CHOICES, default='Drop-in',
                                         blank=True, null=True)
    datetimes = models.CharField(max_length=100, blank=True, null=True)
    is_recurring = models.BooleanField(default=False, null=True)
    datetimes_monday = models.CharField(max_length=100, blank=True, null=True)
    datetimes_tuesday = models.CharField(max_length=100, blank=True, null=True)
    datetimes_wednesday = models.CharField(max_length=100, blank=True, null=True)
    datetimes_thursday = models.CharField(max_length=100, blank=True, null=True)
    datetimes_friday = models.CharField(max_length=100, blank=True, null=True)
    datetimes_saturday = models.CharField(max_length=100, blank=True, null=True)
    datetimes_sunday = models.CharField(max_length=100, blank=True, null=True)
    datetimes_all = models.TextField(blank=True, null=True)
    datetimes_exceptions = models.CharField(max_length=500, blank=True, null=True)
    gender = models.CharField(max_length=300, blank=True, null=True)
    sport_type = models.CharField(max_length=300, blank=True, null=True)
    position = models.CharField(max_length=300, blank=True, null=True)
    city = models.CharField(max_length=300, blank=True, null=True)
    max_age = models.IntegerField(blank=True, null=True)
    min_age = models.IntegerField(blank=True, null=True)
    venue = models.CharField(max_length=300, blank=True, null=True)
    street = models.CharField(max_length=300, blank=True, null=True)
    province = models.CharField(max_length=300, blank=True, null=True)
    country = models.CharField(max_length=300, blank=True, null=True)
    zipcode = models.CharField(max_length=300, blank=True, null=True)
    no_of_position = models.IntegerField(blank=True, null=True)
    position_cost = models.IntegerField(blank=True, null=True)
    sport_logo = models.CharField(max_length=300, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    current_datetimes = models.CharField(max_length=500, blank=True, null=True)

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
    job_title = models.CharField(max_length=100, null=True)
    website = models.CharField(max_length=100, null=True)
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
    postal_code = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, null=True)
    website = models.CharField(max_length=50, null=True)
    gender_focus = models.CharField(max_length=50, null=True)
    age_group = models.CharField(max_length=50, null=True)
    participants = models.CharField(max_length=100, null=True)

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
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    all_day = models.BooleanField(default=False)


class Organization_Availability(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=100)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    all_day = models.BooleanField(default=False)

class Logo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.user.first_name + "_logo"


class Events_PositionInfo(models.Model):
    event = models.ForeignKey(master_table, on_delete=models.CASCADE)
    datetimes = models.CharField(max_length=100, blank=True, null=True)
    position_number = models.IntegerField(blank=True, null=True)
    position_name = models.CharField(max_length=100, blank=True, null=True)
    # Position Type refers to Skill relevant to the position
    position_type = models.CharField(max_length=100, blank=True, null=True)
    max_age = models.IntegerField(blank=True, null=True)
    min_age = models.IntegerField(blank=True, null=True)
    no_of_position = models.IntegerField(blank=True, null=True)
    position_cost = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.event.event_title + " Position_" + str(self.position_number)


class Extra_Loctaions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street = models.CharField(max_length=300, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    province = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=250, blank=True, null=True)
    zipcode = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.first_name + " Location_" + str(self.pk)


class Secondary_SportsChoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sport_type = models.CharField(max_length=30, blank=True, null=True)
    position = models.CharField(max_length=30, blank=True, null=True)
    skill = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.user.first_name + " Sport_Choice_" + str(self.pk)


class SportsImage(models.Model):
    sport = models.CharField(max_length=250, default=None, blank=True, null=True)
    img = models.ImageField(upload_to='images/', default=None, blank=True, null=True)

    def __str__(self):
        return self.sport


class OrderItems(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(master_table, on_delete=models.CASCADE)
    position_id = models.ForeignKey(Events_PositionInfo, on_delete=models.CASCADE)
    date = models.DateField()
    position_type = models.CharField(max_length=100, blank=True, null=True)
    skill = models.CharField(max_length=100, blank=True, null=True)
    no_of_position = models.IntegerField(blank=True, null=True)
    position_cost = models.FloatField(blank=True, null=True)
    total_cost = models.FloatField(blank=True, null=True)
    purchased = models.BooleanField(blank=True, null=True, default=False)
    checkout_timer = models.DateTimeField(blank=True, null=True)


class Order(models.Model):
    PAYMENT_CHOICES = (
        ("--Select--", "--Select--"),
        ("Cash Pickup", "Cash Pickup"),
        ("Card", "Card"),
    )

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItems)
    order_date = models.DateTimeField()
    order_amount = models.FloatField()
    payment = models.BooleanField(blank=True, null=True)
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default='--Select--'
    )
    created = models.DateTimeField(auto_now_add=True)
    paymentId = models.CharField(max_length=200, blank=True, null=True)
    orderId = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.customer.first_name


class Advertisement(models.Model):
    GEOGRAPHICAL_SCOPE_CHOICES = (('Local', 'Local'), ('Provincial', 'Provincial'), ('National', 'National'))

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_time = models.DateTimeField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    header = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    geographical_scope = models.CharField(max_length=100, choices=GEOGRAPHICAL_SCOPE_CHOICES, blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    province = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    client = models.TextField(blank=True, null=True)
    hit_count = models.IntegerField(blank=True, null=True)
    max_hits = models.IntegerField(blank=True, null=True)
