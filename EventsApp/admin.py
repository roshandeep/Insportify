from django.contrib import admin
from EventsApp.models import master_table, User, \
    Individual, Organization, SportsCategory, SportsType, Venues, Availability, Order, Logo, Extra_Loctaions, \
    Events_PositionInfo, Secondary_SportsChoice, OrderItems, PositionAndSkillType, SportsImage, \
    Organization_Availability, Advertisement, Profile, Ad_HitCount

admin.site.register(master_table)
# admin.site.register(User)
admin.site.register(SportsCategory)
admin.site.register(SportsType)
admin.site.register(Individual)
admin.site.register(Organization)
admin.site.register(Logo)
admin.site.register(SportsImage)


class UserAdmin(admin.ModelAdmin):
    list_filter = ('is_individual', 'is_organization',)


admin.site.register(User, UserAdmin)


class PositionAndSkillTypeAdmin(admin.ModelAdmin):
    list_display = ('sports_category', 'sports_type', 'position_type', 'skill_type', 'skill_rank')
    search_fields = ['sports_category', 'sports_type', 'position_type', 'skill_type']
    list_filter = ('sports_category', 'sports_type', 'position_type', 'skill_type',)


admin.site.register(PositionAndSkillType, PositionAndSkillTypeAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'active_user',)
    search_fields = ['name', 'active_user', ]


admin.site.register(Profile, ProfileAdmin)


class VenuesAdmin(admin.ModelAdmin):
    list_display = (
        'vm_name', 'vm_venue_street', 'vm_venuecity', 'vm_venue_province', 'vm_venue_country', 'vm_venue_zip',)
    search_fields = ['vm_name', 'vm_venue_street', 'vm_venuecity', 'vm_venue_province', 'vm_venue_country',
                     'vm_venue_zip', ]


admin.site.register(Venues, VenuesAdmin)


class Events_PositionInfoAdmin(admin.ModelAdmin):
    list_display = ('position_number', 'datetimes', 'event', 'position_name', 'position_type', 'max_age',
                    'min_age', 'no_of_position', 'position_cost',)


admin.site.register(Events_PositionInfo, Events_PositionInfoAdmin)


class Secondary_SportsChoiceAdmin(admin.ModelAdmin):
    list_display = ('profile', 'sport_type', 'position', 'skill')


admin.site.register(Secondary_SportsChoice, Secondary_SportsChoiceAdmin)


class Extra_LoctaionsAdmin(admin.ModelAdmin):
    list_display = ('profile', 'city', 'province', 'country',)


admin.site.register(Extra_Loctaions, Extra_LoctaionsAdmin)


class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('profile', 'day_of_week', 'start_time', 'end_time',)


admin.site.register(Availability, AvailabilityAdmin)


class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ('profile', 'event', 'position_type', 'skill', 'no_of_position', 'position_cost', 'total_cost',)


admin.site.register(OrderItems, OrderItemsAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('orderId', 'customer', 'order_date', 'paymentId', 'order_amount',)


admin.site.register(Order, OrderAdmin)


class Organization_AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('profile', 'day_of_week', 'start_time', 'end_time',)


admin.site.register(Organization_Availability, Organization_AvailabilityAdmin)


class AdvertisementAdmin(admin.ModelAdmin):
    list_display = (
        'header', 'created_by', 'creation_time', 'start_time', 'end_time', 'geographical_scope', 'hit_count')


admin.site.register(Advertisement, AdvertisementAdmin)


class Ad_HitCountAdmin(admin.ModelAdmin):
    list_display = ('ad', 'user_ip')


admin.site.register(Ad_HitCount, Ad_HitCountAdmin)
