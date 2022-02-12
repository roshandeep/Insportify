from django.contrib import admin
from .models import master_table, Test_City, Test_Person, IsEventTypeMaster, IsEventsDetails, IsEventsMaster, \
    IsEventsNotification, IsEventsScheduler, IsNotificationMaster, IsSportsCategory, IsSportsDetails, IsSportsMaster, \
    IsSportsPosition, IsVenueMaster, IsSportsProficiency


admin.site.register(master_table)
admin.site.register(Test_City)
admin.site.register(Test_Person)
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
