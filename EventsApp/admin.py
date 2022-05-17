from django.contrib import admin
from EventsApp.models import master_table, User, \
    Individual, Organization, SportsCategory, SportsType, Venues, Availability, Order, Logo, Extra_Loctaions, \
    Events_PositionInfo

admin.site.register(master_table)
admin.site.register(User)
admin.site.register(SportsCategory)
admin.site.register(SportsType)
admin.site.register(Individual)
admin.site.register(Organization)
admin.site.register(Venues)
admin.site.register(Order)
admin.site.register(Logo)
admin.site.register(Events_PositionInfo)


class Extra_LoctaionsAdmin(admin.ModelAdmin):
    list_display = ('user', 'location_number', 'city', 'province', 'country', )

admin.site.register(Extra_Loctaions, Extra_LoctaionsAdmin)


class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('user', 'day_of_week', 'start_time', 'end_time',)


admin.site.register(Availability, AvailabilityAdmin)
