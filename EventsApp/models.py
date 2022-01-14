# import the standard Django Model
# from built-in library
from django.db import models
  
# # declare a new model with a name "GeeksModel"
# class Is_Event_Master(models.Model):
#         # fields of the model
#     title = models.CharField(max_length = 30)
#     description = models.CharField(max_length=30)


#     def __str__(self):
#         return self.title

class master_table(models.Model):
    event_title = models.CharField(max_length=30,blank=True, null=True)
    description = models.CharField(max_length=30,blank=True, null=True)
    event_type = models.IntegerField(blank=True, null=True)
    datetimes = models.CharField(max_length=50,blank=True, null=True)
    sport_category = models.CharField(max_length=30,blank=True, null=True)
    sport_type = models.CharField(max_length=30,blank=True, null=True)
    position = models.CharField(max_length=30,blank=True, null=True)
    city = models.CharField(max_length=30,blank=True, null=True)
    #name = models.CharField(max_length=30,blank=True, null=True)
    skill = models.CharField(max_length=30,blank=True, null=True)
    max_age = models.IntegerField(blank=True, null=True)
    min_age = models.IntegerField(blank=True, null=True)
    venue = models.CharField(max_length=30,blank=True, null=True)
    country = models.CharField(max_length=30,blank=True, null=True)
    province = models.CharField(max_length=30,blank=True, null=True)
    country = models.CharField(max_length=30,blank=True, null=True)
    #name = models.CharField(max_length=30,blank=True,null=True)
    no_of_position = models.IntegerField(blank=True,null=True)
    position_cost = models.IntegerField(blank=True,null=True)
        # renames the instances of the model
        # with their title name
    def __str__(self):
        return self.event_title

class Test_City(models.Model):
    test_country = models.ForeignKey(master_table, on_delete=models.CASCADE)
    name = models.CharField(max_length=30,null=True)

class Test_Person(models.Model):
    name = models.CharField(max_length=30, null=True)
    birthdate = models.DateField(null=True, blank=True)
    test_country = models.ForeignKey(master_table, on_delete=models.SET_NULL, null=True)
    test_city = models.ForeignKey(Test_City, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    def __str__(self):
        return self.name