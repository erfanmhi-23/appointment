from django.contrib import admin
from doctors.models import Doctor, Timesheet, Office, Visittime

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'field', 'expertise', 'np', 'is_active')

    def full_name(self, obj):
        full = obj.user.get_full_name()
        return full if full else obj.user.username
    full_name.short_description = 'نام کامل'

@admin.register(Office) 
class OfficeAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'location', 'phone_num')

@admin.register(Timesheet)
class TimesheetAdmin(admin.ModelAdmin):
    list_display = ('office', 'start', 'end', 'duration')

@admin.register(Visittime) 
class VisittimeAdmin(admin.ModelAdmin):
    pass
