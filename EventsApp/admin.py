from django.contrib import admin
#from .models import Is_Event_Master
from .models import master_table, Test_City, Test_Person



#admin.site.register(Venue)
#admin.site.register(MyEventUser)
#admin.site.register(Event)
#admin.site.register(Is_Event_Master)

admin.site.register(master_table)
admin.site.register(Test_City)
admin.site.register(Test_Person)

# @admin.register(Venue)
# class VenueAdmin(admin.ModelAdmin):
# 	list_display = ('name' , 'address', 'phone')
# 	ordering = ('name',)
# 	search_fields = ('name', 'address')

# @admin.register(Event)
# class EventAdmin(admin.ModelAdmin):
# 	fields = (('name','venue'), 'event_date','description', 'manager')
# 	list_display = ('name','event_date', 'venue')
# 	list_filter = ('event_date', 'venue')
# 	ordering = ('event_date',)

#@admin.register(MultiStep)
#class MultiEventAdmin(admin.ModelAdmin):
#	fields = (('event_title'), 'category','event_type','athelete_level','staff_level')
#	list_display = ('event_title','venue')
#	list_filter = ('event_title', 'venue')
#	ordering = ('event_title',)