from django.contrib import admin
from EventsApp.models import master_table, User, IsEventTypeMaster, IsEventsDetails, \
    IsEventsNotification, IsEventsScheduler, IsNotificationMaster, \
    Individual, Organization, SportsCategory, SportsType, Venues, Availability, Order, Logo

admin.site.register(master_table)
admin.site.register(User)
admin.site.register(IsEventTypeMaster)
admin.site.register(IsEventsDetails)
admin.site.register(IsEventsNotification)
admin.site.register(IsEventsScheduler)
admin.site.register(IsNotificationMaster)
admin.site.register(SportsCategory)
admin.site.register(SportsType)
admin.site.register(Individual)
admin.site.register(Organization)
admin.site.register(Venues)
admin.site.register(Order)
admin.site.register(Logo)


class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('user', 'day_of_week', 'start_time', 'end_time',)


admin.site.register(Availability, AvailabilityAdmin)
