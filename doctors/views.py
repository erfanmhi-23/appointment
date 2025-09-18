from django.shortcuts import render, get_object_or_404, redirect
from doctors.models import Doctor,Office,Timesheet,Visittime
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator




def doctor_list(request):
    doctors = Doctor.objects.all()
    paginator = Paginator(doctors, 10)
    page_num = request.GET.get("page")
    page_obj = paginator.get_page(page_num)
    return render(request, 'doctor_list.html', {'page_obj': page_obj,})

def office_list(request):
    location = request.GET.get('location')
    if location:
        offices = Office.objects.filter(location__icontains = location)
    else:
        offices = Office.objects.all()
    return render(request, 'doctors/office_list.html',{'offices': offices})

def doctor_search(request):
    query = request.GET.get('q')
    if query:
        doctors = Doctor.objects.filter(
            Q(field__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        )
    else:
        doctors = Doctor.objects.all()
    return render(request, 'doctors/doctor_search.html', {'doctors': doctors})

@staff_member_required
def timesheet_list(request):
    timesheets = Timesheet.objects.all()
    return render(request, 'doctors/timesheet_list.html', {'timesheets':timesheets})

def doctor_free_times(request, doctor_id):
    free_times = Visittime.objects.filter(doctor_id = doctor_id, patient__isnull=True, canceled_at__isnull=True)
    return render(request, 'doctors/doctor_free_times.html', {'free_times': free_times})

@login_required
def reserve_visit_time(request, visit_id):
    visit_time = get_object_or_404(Visittime, id=visit_id, patient__isnull=True, canceled_at__isnull=True)
    if request.method == "POST":
        visit_time.patient = request.user
        visit_time.booked_at = timezone.now()
        visit_time.save()
        return redirect('doctor_free_times', doctor_id=visit_time.doctor.id)
    return render(request, 'doctors/reserve_visit_time.html', {'visit_time': visit_time})

@login_required
def cancel_visit_time(request, visit_id):
    visit_time = get_object_or_404(Visittime, id=visit_id, patient=request.user, canceled_at__isnull=True)
    if request.method == "POST":
        visit_time.canceled_at = timezone.now()
        visit_time.save()
        return redirect('doctor_free_times', doctor_id=visit_time.doctor.id)
    return render(request, 'doctors/cancel_visit_time.html', {'visit_time': visit_time})

def home(request):
    return render(request, 'base.html')
