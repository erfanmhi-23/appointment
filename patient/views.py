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


