from django.contrib import admin
from EventsApp.models import master_table, User, \
    Individual, Organization, SportsCategory, SportsType, Venues, Availability, Order, Logo, Extra_Loctaions, \
    Events_PositionInfo, Secondary_SportsChoice

admin.site.register(master_table)
admin.site.register(User)
admin.site.register(SportsCategory)
admin.site.register(SportsType)
admin.site.register(Individual)
admin.site.register(Organization)
admin.site.register(Venues)
admin.site.register(Order)
admin.site.register(Logo)


class Events_PositionInfoAdmin(admin.ModelAdmin):
    list_display = ('event', 'position_number', 'max_age', 'min_age', 'no_of_position', 'position_cost',)


admin.site.register(Events_PositionInfo)


class Secondary_SportsChoiceAdmin(admin.ModelAdmin):
    list_display = ('user', 'sport_entry_number', 'sport_category', 'sport_type', 'position',)


admin.site.register(Secondary_SportsChoice, Secondary_SportsChoiceAdmin)


class Extra_LoctaionsAdmin(admin.ModelAdmin):
    list_display = ('user', 'location_number', 'city', 'province', 'country',)


admin.site.register(Extra_Loctaions, Extra_LoctaionsAdmin)


class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('user', 'day_of_week', 'start_time', 'end_time',)


admin.site.register(Availability, AvailabilityAdmin)
