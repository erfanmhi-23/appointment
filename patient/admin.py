from django.contrib import admin
from patient.models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id','na_id','birth_date')