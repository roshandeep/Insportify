from django.contrib import admin
from EventsApp.models import master_table, User, \
    Individual, Organization, SportsCategory, SportsType, Venues, Availability, Order, Logo, Extra_Loctaions, \
    Events_PositionInfo, Secondary_SportsChoice, OrderItems, PositionAndSkillType, SportsImage, Organization_Availability

admin.site.register(master_table)
admin.site.register(User)
admin.site.register(SportsCategory)
admin.site.register(SportsType)
admin.site.register(Individual)
admin.site.register(Organization)
admin.site.register(Logo)
admin.site.register(PositionAndSkillType)
admin.site.register(SportsImage)

class VenuesAdmin(admin.ModelAdmin):
    list_display = ('vm_name', 'vm_venue_street', 'vm_venuecity', 'vm_venue_province', 'vm_venue_country', 'vm_venue_zip',)
    search_fields = ['vm_name', 'vm_venue_street', 'vm_venuecity', 'vm_venue_province', 'vm_venue_country', 'vm_venue_zip',]


admin.site.register(Venues, VenuesAdmin)


class Events_PositionInfoAdmin(admin.ModelAdmin):
    list_display = ('position_number', 'event', 'position_name', 'position_type', 'max_age', 'min_age', 'no_of_position', 'position_cost',)


admin.site.register(Events_PositionInfo, Events_PositionInfoAdmin)


class Secondary_SportsChoiceAdmin(admin.ModelAdmin):
    list_display = ('user', 'sport_type', 'position',)


admin.site.register(Secondary_SportsChoice, Secondary_SportsChoiceAdmin)


class Extra_LoctaionsAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'province', 'country',)


admin.site.register(Extra_Loctaions, Extra_LoctaionsAdmin)


class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('user', 'day_of_week', 'start_time', 'end_time',)


admin.site.register(Availability, AvailabilityAdmin)


class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'position_type', 'skill', 'no_of_position', 'position_cost', 'total_cost', )


admin.site.register(OrderItems, OrderItemsAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('orderId', 'customer', 'order_date', 'paymentId', 'order_amount',)


admin.site.register(Order, OrderAdmin)



class Organization_AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('user', 'day_of_week', 'start_time', 'end_time',)


admin.site.register(Organization_Availability, Organization_AvailabilityAdmin)

