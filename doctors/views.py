from django.shortcuts import render, get_object_or_404, redirect
from doctors.models import Doctor,Office,Timesheet,Visittime
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.core.paginator import Paginator
from .forms import DoctorCreateForm , OfficeForm , TimesheetForm



def doctor_list(request):
    doctors = Doctor.objects.all()
    field = request.GET.get("field")
    location = request.GET.get("location")
    if field:
        doctors = doctors.filter(field__icontains=field)

    if location:
        doctors = doctors.filter(offices__location__icontains=location).distinct()
    paginator = Paginator(doctors, 10)
    page_num = request.GET.get("page")
    page_obj = paginator.get_page(page_num)
    return render(request, 'doctors/doctor_list.html', {
        'page_obj': page_obj,
        'field': field,
        'location': location,
    })


def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)

    
    timesheets = Timesheet.objects.filter(office__doctor=doctor).order_by('start')

    return render(request, 'doctors/doctor_detail.html', {
        'doctor': doctor,
        'timesheets': timesheets,
    })


def doctor_search(request):
    query = request.GET.get('q', '')
    if query:
        doctors = Doctor.objects.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(field__icontains=query)
        )
    else:
        doctors = Doctor.objects.all()

    return render(request, 'doctors/doctor_search.html', {'doctors': doctors, 'query': query})

def office_list(request):
    location = request.GET.get('location')
    if location:
        offices = Office.objects.filter(location__icontains = location)
    else:
        offices = Office.objects.all()
    return render(request, 'doctors/office_list.html',{'offices': offices})


@staff_member_required
def office_detail(request, office_id):
    office = get_object_or_404(Office, id=office_id)
    timesheets = office.time_sheets.all().order_by('start')
    return render(request, 'doctors/office_detail.html', {'office': office, 'timesheets': timesheets})


@staff_member_required
def office_edit(request, office_id):
    office = get_object_or_404(Office, id=office_id)

    if request.method == 'POST':
        form = OfficeForm(request.POST, instance=office)
        if form.is_valid():
            form.save()
            return redirect('office_detail', office_id=office.id)
    else:
        form = OfficeForm(instance=office)

    return render(request, 'doctors/office_edit.html', {'form': form, 'office': office})


@staff_member_required
def timesheet_list(request):
    offices = Office.objects.select_related('doctor__user').all()
    return render(request, 'doctors/timesheet_list.html', {'offices': offices})


@staff_member_required
def timesheet_edit(request, timesheet_id):
    timesheet = get_object_or_404(Timesheet, id=timesheet_id)

    if request.method == 'POST':
        form = TimesheetForm(request.POST, instance=timesheet)
        if form.is_valid():
            form.save()
            return redirect('timesheet_list')
    else:
        form = TimesheetForm(instance=timesheet)

    return render(request, 'doctors/timesheet_edit.html', {'form': form, 'timesheet': timesheet})


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
    return render(request, 'home.html')


def is_admin(user):
    return user.is_superuser or user.groups.filter(name='Admins').exists()

@login_required
@user_passes_test(is_admin)
def add_doctor(request):
    if request.method == 'POST':
        form = DoctorCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('doctor_list')
    else:
        form = DoctorCreateForm()
    return render(request, 'doctors/add_doctor.html', {'form': form})


