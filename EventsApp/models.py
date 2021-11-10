from django.db import models

# Create your models here.

class IS_EVENT_MASTER(models.Model):
    EM_EVENT_ID = models.Auto_Field(primary_key = True)
    EM_EVENT_TITLE = models.CharField()
    EM_EVENT_DESC = models.TextField()
    ETM_FK_EM_EVENT_TYPE_ID = models.IntegerField()
    EM_COST = models.NumericOutputFieldMixin()
    EM_GENDER = models.TextField()
    EM_MIN_AGE = models.NumericOutputFieldMixin()
    EM_MAX_AGE = models.NumericOutputFieldMixin()
    EM_CREATED_BY = models.IntegerField()
    EM_CREATED_DATE = models.datetime()
    EM_UPDATED_BY = models.IntegerField()
    EM_UPDATED_DATE = models.datetime()

