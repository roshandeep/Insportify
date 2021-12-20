from django.contrib import admin
from .models import Venue
from .models import MyEventUser
from .models import Event
from .models import MultiStep

#admin.site.register(Venue)
admin.site.register(MyEventUser)
#admin.site.register(Event)

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
	list_display = ('name' , 'address', 'phone')
	ordering = ('name',)
	search_fields = ('name', 'address')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
	fields = (('name','venue'), 'event_date','description', 'manager')
	list_display = ('name','event_date', 'venue')
	list_filter = ('event_date', 'venue')
	ordering = ('event_date',)

@admin.register(MultiStep)
class MultiEventAdmin(admin.ModelAdmin):
	fields = (('event_title'), 'category','event_type','date','athelete_level','staff_level')
	list_display = ('event_title','venue', 'date')
	list_filter = ('event_title', 'venue')
	ordering = ('event_title',)