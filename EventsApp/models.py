from django.db import models

# Create your models here.

class Events(models.Model):
    Event_ID = models.Auto_Field(primary_key = True)
    Event_Title = models.CharField()
    Event_Description = models.TextField()
    Event_Type = models.CharField()
    Cost = models.NumericOutputFieldMixin()
    Gender = models.CharField()
    Min_Age = models.NumericOutputFieldMixin()
    Max_Age = models.NumericOutputFieldMixin()
    Created_By = models.CharField()
    Created_Date = models.datetime()
    Updated_By = models.CharField()
    Updated_Date = models.datetime()

