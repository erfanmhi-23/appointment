from django.shortcuts import render,redirect
from doctors.models import *
from patient.forms import PatientForm

def sign_up(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = PatientForm()
    return render(request, 'sign_up.html', {'form': form})


