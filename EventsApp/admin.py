from django.contrib import admin
from EventsApp.models import master_table, User, IsEventTypeMaster, IsEventsDetails, IsEventsMaster, \
    IsEventsNotification, IsEventsScheduler, IsNotificationMaster, IsSportsCategory, IsSportsDetails, IsSportsMaster, \
    IsSportsPosition, IsVenueMaster, IsSportsProficiency, Individual

admin.site.register(master_table)
admin.site.register(User)
admin.site.register(IsEventTypeMaster)
admin.site.register(IsEventsDetails)
admin.site.register(IsEventsMaster)
admin.site.register(IsEventsNotification)
admin.site.register(IsEventsScheduler)
admin.site.register(IsNotificationMaster)
admin.site.register(IsSportsCategory)
admin.site.register(IsSportsDetails)
admin.site.register(IsSportsMaster)
admin.site.register(IsSportsPosition)
admin.site.register(IsSportsProficiency)
admin.site.register(IsVenueMaster)

admin.site.register(Individual)
