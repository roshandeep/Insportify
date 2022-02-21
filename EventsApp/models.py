# import the standard Django Model
# from built-in library
from django.core import checks
from django.db import models

class master_table(models.Model):
    event_title = models.CharField(max_length=30, blank=True, null=True)
    description = models.CharField(max_length=30, blank=True, null=True)
    event_type = models.IntegerField(blank=True, null=True)
    datetimes = models.CharField(max_length=50, blank=True, null=True)
    sport_category = models.CharField(max_length=30, blank=True, null=True)
    sport_type = models.CharField(max_length=30, blank=True, null=True)
    position = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    # name = models.CharField(max_length=30,blank=True, null=True)
    skill = models.CharField(max_length=30, blank=True, null=True)
    max_age = models.IntegerField(blank=True, null=True)
    min_age = models.IntegerField(blank=True, null=True)
    venue = models.CharField(max_length=30, blank=True, null=True)
    country = models.CharField(max_length=30, blank=True, null=True)
    province = models.CharField(max_length=30, blank=True, null=True)
    country = models.CharField(max_length=30, blank=True, null=True)
    # name = models.CharField(max_length=30,blank=True,null=True)
    no_of_position = models.IntegerField(blank=True, null=True)
    position_cost = models.IntegerField(blank=True, null=True)

    # renames the instances of the model
    # with their title name
    def __str__(self):
        return self.event_title

    class Meta:
        managed = True
        db_table = 'master_table'


class Test_City(models.Model):
    test_country = models.ForeignKey(master_table, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, null=True)

    class Meta:
        managed = True
        db_table = 'Test_City'


class Test_Person(models.Model):
    name = models.CharField(max_length=30, null=True)
    birthdate = models.DateField(null=True, blank=True)
    test_country = models.ForeignKey(master_table, on_delete=models.SET_NULL, null=True)
    test_city = models.ForeignKey(Test_City, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'Test_Person'


class EventsappMasterTable(models.Model):
    id = models.BigAutoField(primary_key=True)
    event_title = models.CharField(max_length=30, blank=True, null=True)
    description = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    country = models.CharField(max_length=30, blank=True, null=True)
    datetimes = models.CharField(max_length=50, blank=True, null=True)
    event_type = models.IntegerField(blank=True, null=True)
    max_age = models.IntegerField(blank=True, null=True)
    min_age = models.IntegerField(blank=True, null=True)
    position = models.CharField(max_length=30, blank=True, null=True)
    province = models.CharField(max_length=30, blank=True, null=True)
    skill = models.CharField(max_length=30, blank=True, null=True)
    sport_category = models.CharField(max_length=30, blank=True, null=True)
    sport_type = models.CharField(max_length=30, blank=True, null=True)
    venue = models.CharField(max_length=30, blank=True, null=True)
    no_of_position = models.IntegerField(blank=True, null=True)
    position_cost = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'EventsApp_master_table'


class EventsappTestCity(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    test_country = models.ForeignKey(EventsappMasterTable, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'EventsApp_test_city'


class EventsappTestPerson(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    test_city = models.ForeignKey(EventsappTestCity, models.DO_NOTHING, blank=True, null=True)
    test_country = models.ForeignKey(EventsappMasterTable, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'EventsApp_test_person'


class IsEventTypeMaster(models.Model):
    etm_id = models.IntegerField()
    etm_category = models.CharField(max_length=100, blank=True, null=True)
    etm_title = models.CharField(max_length=100, blank=True, null=True)
    etm_description = models.CharField(max_length=250, blank=True, null=True)
    etm_isactive = models.CharField(max_length=1, blank=True, null=True)
    etm_created_by = models.IntegerField(blank=True, null=True)
    etm_updated_by = models.IntegerField(blank=True, null=True)
    etm_updated_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.etm_id

    def __str__(self):
        return self.etm_category

    class Meta:
        managed = True
        db_table = 'is_event_type_master'


class IsEventsDetails(models.Model):
    ed_id = models.IntegerField()
    ed_fk_em_id = models.IntegerField(blank=True, null=True)
    ed_fk_sc_id = models.IntegerField(blank=True, null=True)
    ed_fk_sm_id = models.IntegerField(blank=True, null=True)
    ed_fk_sp_id = models.IntegerField(blank=True, null=True)
    ed_fk_spc_id = models.IntegerField(blank=True, null=True)
    ed_fk_sports_position_cost = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    ed_created_date = models.DateTimeField(blank=True, null=True)
    ed_created_by = models.IntegerField(blank=True, null=True)
    ed_updated_by = models.IntegerField(blank=True, null=True)
    ed_updated_date = models.DateTimeField(blank=True, null=True)
    is_active = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'is_events_details'


class IsEventsMaster(models.Model):
    em_id = models.IntegerField()
    em_title = models.CharField(max_length=100, blank=True, null=True)
    em_desc = models.CharField(max_length=250, blank=True, null=True)
    em_fk_etm_id = models.IntegerField(blank=True, null=True)
    em_gender = models.CharField(max_length=10, blank=True, null=True)
    em_isactive = models.CharField(max_length=1, blank=True, null=True)
    em_created_date = models.DateTimeField(blank=True, null=True)
    em_created_by = models.IntegerField(blank=True, null=True)
    em_updated_by = models.IntegerField(blank=True, null=True)
    em_updated_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'is_events_master'


class IsEventsNotification(models.Model):
    en_id = models.IntegerField()
    en_fk_em_id = models.IntegerField(blank=True, null=True)
    en_fk_nm_id = models.IntegerField(blank=True, null=True)
    en_created_by = models.IntegerField(blank=True, null=True)
    en_updated_by = models.IntegerField(blank=True, null=True)
    en_updated_date = models.DateTimeField(blank=True, null=True)
    is_active = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'is_events_notification'


class IsEventsScheduler(models.Model):
    es_id = models.IntegerField()
    es_fk_em_id = models.IntegerField(blank=True, null=True)
    es_from_date = models.DateTimeField(blank=True, null=True)
    es_to_date = models.DateTimeField(blank=True, null=True)
    es_venue_name = models.CharField(max_length=100, blank=True, null=True)
    es_event_venue_street = models.CharField(max_length=100, blank=True, null=True)
    es_event_venue_city = models.CharField(max_length=50, blank=True, null=True)
    es_event_venue_province = models.CharField(max_length=50, blank=True, null=True)
    es_event_venue_country = models.CharField(max_length=100, blank=True, null=True)
    es_event_venue_zip = models.CharField(max_length=6, blank=True, null=True)
    em_fk_etm_id = models.IntegerField(blank=True, null=True)
    es_fk_ef_id = models.IntegerField(blank=True, null=True)
    es_min_age = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    es_max_age = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    em_isactive = models.CharField(max_length=1, blank=True, null=True)
    es_created_date = models.DateTimeField(blank=True, null=True)
    es_created_by = models.IntegerField(blank=True, null=True)
    es_updated_by = models.IntegerField(blank=True, null=True)
    es_updated_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'is_events_scheduler'


class IsNotificationMaster(models.Model):
    nm_id = models.IntegerField()
    nm_title = models.CharField(max_length=100, blank=True, null=True)
    nm_description = models.CharField(max_length=250, blank=True, null=True)
    nm_trigger = models.CharField(max_length=10, blank=True, null=True)
    nm_trigger_frequency = models.CharField(max_length=10, blank=True, null=True)
    nm_isactive = models.CharField(max_length=1, blank=True, null=True)
    nm_created_by = models.IntegerField(blank=True, null=True)
    nm_updated_by = models.IntegerField(blank=True, null=True)
    nm_updated_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'is_notification_master'


class IsSportsCategory(models.Model):
    sc_id = models.IntegerField()
    sc_sports_catgeory = models.CharField(max_length=100)
    sc_created_by = models.IntegerField(blank=True, null=True)
    sc_created_date = models.DateTimeField(blank=True, null=True)
    sc_updated_by = models.IntegerField(blank=True, null=True)
    sc_updated_date = models.DateTimeField(blank=True, null=True)
    is_active = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'is_sports_category'


class IsSportsDetails(models.Model):
    sd_id = models.IntegerField()
    sd_fk_sc_id = models.IntegerField(blank=True, null=True)
    sd_fk_sm_id = models.IntegerField(blank=True, null=True)
    sd_fk_sp_id = models.IntegerField(blank=True, null=True)
    sd_created_by = models.IntegerField(blank=True, null=True)
    sd_created_date = models.DateTimeField(blank=True, null=True)
    sd_updated_by = models.IntegerField(blank=True, null=True)
    sd_updated_date = models.DateTimeField(blank=True, null=True)
    is_active = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'is_sports_details'


class IsSportsMaster(models.Model):
    sm_id = models.IntegerField()
    sm_sports_name = models.CharField(max_length=100)
    sm_created_by = models.IntegerField(blank=True, null=True)
    sm_created_date = models.DateTimeField(blank=True, null=True)
    sm_updated_by = models.IntegerField(blank=True, null=True)
    sm_updated_date = models.DateTimeField(blank=True, null=True)
    is_active = models.CharField(max_length=1, blank=True, null=True)
    sm_fk_sc_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'is_sports_master'


class IsSportsPosition(models.Model):
    sp_id = models.IntegerField()
    sp_fk_sc_id = models.IntegerField(blank=True, null=True)
    sp_position_name = models.CharField(max_length=100)
    sp_created_by = models.IntegerField(blank=True, null=True)
    sp_created_date = models.DateTimeField(blank=True, null=True)
    sp_updated_by = models.IntegerField(blank=True, null=True)
    sp_updated_date = models.DateTimeField(blank=True, null=True)
    is_active = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'is_sports_position'


class IsSportsProficiency(models.Model):
    spc_id = models.IntegerField(blank=False, null=False)
    spc_prof_name = models.CharField(max_length=100, blank=True, null=True)
    spc_created_date = models.DateTimeField(blank=True, null=True)
    spc_updated_by = models.IntegerField(blank=True, null=True)
    spc_updated_date = models.DateTimeField(blank=True, null=True)
    is_active = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'is_sports_proficiency'


class IsVenueMaster(models.Model):
    vm_id = models.IntegerField()
    vm_name = models.CharField(max_length=100, blank=True, null=True)
    vm_venue_description = models.CharField(max_length=250, blank=True, null=True)
    vm_venue_street = models.CharField(max_length=250, blank=True, null=True)
    vm_venuecity = models.CharField(max_length=50, blank=True, null=True)
    vm_venue_province = models.CharField(max_length=50, blank=True, null=True)
    vm_venue_country = models.CharField(max_length=50, blank=True, null=True)
    vm_venue_zip = models.CharField(max_length=6, blank=True, null=True)
    vm_isactive = models.CharField(max_length=1, blank=True, null=True)
    vm_created_by = models.IntegerField(blank=True, null=True)
    vm_updated_by = models.IntegerField(blank=True, null=True)
    vm_updated_date = models.DateTimeField(blank=True, null=True)
    venu_name = models.CharField(max_length=17, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'is_venue_master'

