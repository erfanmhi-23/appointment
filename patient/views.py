from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from doctors.models import *
from patient.models import Patient
from patient.forms import PatientForm
from django.contrib.auth import login

def sign_up(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = PatientForm()
    return render(request, 'sign_up.html', {'form': form})



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