from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from doctors.models import *
from patient.models import Patient

def show_nobat (request,Doc) :
    the_Doc = Doctor.objects.get(pk=Doc)
    the_off = the_Doc.offices.all()
    
    offices_with_timesheets = []
    for office in the_off:
        offices_with_timesheets.append({
            'office': office,
            'timesheets': office.time_sheets.all().order_by('start')})

    context = {
        'doctor': the_Doc,
        'offices_with_timesheets': offices_with_timesheets,
    }
    return render(request, 'show_nobat.html', context)


@login_required
def reserve_nobat (request,) :
    pass

@login_required
def cancel_nobat (request,reserved) :
    pass