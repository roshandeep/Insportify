from django.contrib import admin
from EventsApp.models import master_table, User, IsEventTypeMaster, IsEventsDetails, IsEventsMaster, \
    IsEventsNotification, IsEventsScheduler, IsNotificationMaster,\
    IsVenueMaster, Individual, Organization, SportsCategory, SportsType

admin.site.register(master_table)
admin.site.register(User)
admin.site.register(IsEventTypeMaster)
admin.site.register(IsEventsDetails)
admin.site.register(IsEventsMaster)
admin.site.register(IsEventsNotification)
admin.site.register(IsEventsScheduler)
admin.site.register(IsNotificationMaster)
admin.site.register(IsVenueMaster)
admin.site.register(SportsCategory)
admin.site.register(SportsType)
admin.site.register(Individual)
admin.site.register(Organization)
