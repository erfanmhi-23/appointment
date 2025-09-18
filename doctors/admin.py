from django.contrib import admin
from doctors.models import Doctor , Timesheet , Office , Visittime
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin) :
    list_display = ('id' , 'user' , 'field' , 'expertise' , 'np' , 'is_active' )

@admin.register(Office) 
class OfficeAdmin(admin.ModelAdmin) :
    list_display = ('doctor' , 'location' , 'phone_num' )

@admin.register(Timesheet)
class TimesheetAdmin(admin.ModelAdmin) :
    list_display = ('office' , 'start' , 'end' , 'duration')

@admin.register(Visittime) 
class VisittimeAdmin(admin.ModelAdmin) :
    pass