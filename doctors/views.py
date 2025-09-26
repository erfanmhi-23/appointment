from django.shortcuts import render, get_object_or_404, redirect
from doctors.models import Doctor,Office,Timesheet,Visittime
from django.db.models import Q , F
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.core.paginator import Paginator
from .forms import DoctorCreateForm , OfficeForm , TimesheetForm
from doctors.services import get_available_timeslots_for_doctor
from django.utils.dateparse import parse_datetime
from django.http import HttpResponseBadRequest
from wallet.models import Wallet
from django.http import HttpResponseBadRequest , HttpResponseRedirect
from django.contrib.auth import login , get_user_model
from patient.models import Patient


User = get_user_model()




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

    doctor_times = None
    if request.user.is_authenticated:
        try:
            patient = request.user.patient_profile
            doctor_times = Visittime.objects.filter(
                doctor=doctor,
                patient=request.user,
                canceled_at__isnull=True
            ).order_by('-duration_start')
        except Patient.DoesNotExist:
            doctor_times = None

    return render(request, 'doctors/doctor_detail.html', {
        'doctor': doctor,
        'doctor_times': doctor_times,
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


@staff_member_required
def office_detail(request, office_id):
    office = get_object_or_404(Office, id=office_id)
    timesheets = office.time_sheets.all().order_by('start')
    return render(request, 'doctors/office_detail.html', {'office': office, 'timesheets': timesheets})


@staff_member_required
def add_office(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)

    if request.method == 'POST':
        form = OfficeForm(request.POST)
        if form.is_valid():
            office = form.save(commit=False)
            office.doctor = doctor
            office.save()
            return redirect('add_timesheet', doctor_id=doctor.id, office_id=office.id)
    else:
        form = OfficeForm()

    return render(request, 'doctors/add_office.html', {'form': form, 'doctor': doctor})

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
def add_timesheet(request, doctor_id, office_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    office = get_object_or_404(Office, id=office_id, doctor=doctor)

    if request.method == 'POST':
        form = TimesheetForm(request.POST)
        if form.is_valid():
            timesheet = form.save(commit=False)
            timesheet.office = office
            timesheet.save()
            return redirect('home') 
    else:
        form = TimesheetForm()

    return render(request, 'doctors/add_timesheet.html', {
        'form': form,
        'doctor': doctor,
        'office': office
    })

@staff_member_required
def timesheet_list(request):
    offices = Office.objects.select_related('doctor__user').all().order_by('doctor__user__first_name', 'doctor__user__last_name')
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


def available_times_for_doctor(request, doctor_id):
    timesheet_slots = get_available_timeslots_for_doctor(doctor_id)

    return render(request, 'doctors/show_timesheet.html', {
        'doctor_id': doctor_id,
        'timesheet_slots': timesheet_slots,
    })

@login_required
def reserve_time(request , doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    start = request.GET.get('start')
    end = request.GET.get('end')

    start_date = parse_datetime(start) if start else None
    end_date = parse_datetime(end) if end else None

    try:
        wallet = Wallet.objects.get(user=request.user)
    except Wallet.DoesNotExist:
        wallet = None  

    return render(request, 'doctors/reserve_time.html', {
        'doctor': doctor,
        'start': start,
        'end': end,
        'wallet': wallet,
        'start_date':start_date,
        'end_date': end_date,  
    })


@login_required
def reserve_visit_time(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    office = doctor.offices.first()
    patient = request.user

    if request.method == 'POST':
        start_str = request.POST.get('start')
        end_str = request.POST.get('end')
    else:
        
        return HttpResponseBadRequest("درخواست نامعتبر است.")

    if not start_str or not end_str:
        return HttpResponseBadRequest("پارامترهای زمان ارسال نشده‌اند.")

    start = parse_datetime(start_str)
    end = parse_datetime(end_str)

    if not start or not end:
        return HttpResponseBadRequest("فرمت زمان معتبر نیست.")
        
    already_reserved = Visittime.objects.filter(
        doctor=doctor,
        office=office,
        duration_start=start,
        canceled_at__isnull=True
    ).exists()

    if already_reserved:
        return HttpResponseBadRequest("این زمان قبلاً رزرو شده است.")

    Visittime.objects.create(
        doctor=doctor,
        office=office,
        patient=patient,
        duration_start=start,
        duration_end=end,
        booked_at=timezone.now(),
    )
    price = office.price
    wallet = get_object_or_404(Wallet, user=request.user)
    if wallet.inventory >= price:
        Wallet.objects.filter(user=request.user).update(inventory=F('inventory') - price)
        send_visit_confirmation_email(patient, doctor, office, start, end, price)
        return redirect('doctor_list')
    if wallet.inventory < price :
        return HttpResponseBadRequest("موجودی کیف پول کافی نمیباشد از قسمت پروفایل نسبت به شارژ آن اقدام نمایید")
    else:
        return redirect('home')

   




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
            doctor = form.save()
            if doctor.is_active:
                return redirect('add_office',doctor_id=doctor.id)
            else:
                return redirect('doctor_list')
    else:
        form = DoctorCreateForm()
    return render(request, 'doctors/add_doctor.html', {'form': form})



def near_doctor(request):
    field = request.GET.get("field", "")
    location = request.GET.get("location", "")
    doctors = Doctor.objects.all()

    if field:
        doctors = doctors.filter(field__icontains=field)
    if location:
        doctors = doctors.filter(offices__location__icontains=location).distinct()

    paginator = Paginator(doctors, 10)
    page_num = request.GET.get("page")
    page_obj = paginator.get_page(page_num)

    return render(request, "doctors/near_doctor.html", {
        "page_obj": page_obj,
        "field": field,
        "location": location
    })

def google_callback(request):
    code = request.GET.get("code")
    if not code:
        return HttpResponseRedirect("/login/")
    email = "test@gmail.com"
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = User.objects.create_user(username=email.split("@")[0], email=email)
    login(request, user)
    return HttpResponseRedirect("/")

def send_visit_confirmation_email(patient, doctor, office, start, end, price):
    if not patient.email:
        return

    subject = 'تایید رزرو نوبت'
    message = f"""
سلام {patient.get_full_name()}،

نوبت شما با موفقیت رزرو شد.

جزئیات نوبت:
دکتر: {doctor.user.get_full_name()}
مطب: {office.location}
تاریخ: {start.date()}
ساعت شروع: {start.time().strftime('%H:%M')}
ساعت پایان: {end.time().strftime('%H:%M')}
هزینه ویزیت: {price} تومان

با تشکر،
تیم کلینیک
    """
    from django.core.mail import send_mail

    send_mail(
        subject,
        message,
        'noreply@example.com',
        [patient.email],
        fail_silently=False,
    )
