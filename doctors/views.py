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
from django.db.models import OuterRef, Exists
from wallet.models import Wallet
from django.http import HttpResponseBadRequest , HttpResponseRedirect
from django.contrib.auth import login , get_user_model
from django.contrib import messages
from django.core.mail import send_mail

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
    unbooked_visits = Visittime.objects.filter(
        doctor=doctor,
        office=OuterRef('office'),
        booked_at__isnull=True,  
        canceled_at__isnull=True,
        duration_start__lt=OuterRef('end'),
        duration_end__gt=OuterRef('start'),
    )
    timesheets = Timesheet.objects.filter(
        office__doctor=doctor
    ).annotate(
        has_unbooked_visit=Exists(unbooked_visits)
    ).filter(
        has_unbooked_visit=True
    ).order_by('start')

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

##del
def doctor_free_times(request, doctor_id):
    free_times = Visittime.objects.filter(doctor_id = doctor_id, patient__isnull=True, canceled_at__isnull=True)
    return render(request, 'doctors/doctor_free_times.html', {'free_times': free_times})

##del
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
    offices = Office.objects.select_related('doctor__user').all().order_by('doctor__user__first_name', 'doctor__user__last_name')
    return render(request, 'doctors/timesheet_list.html', {'offices': offices})


def available_times_for_doctor(request, doctor_id):
    timesheet_slots = get_available_timeslots_for_doctor(doctor_id)
    doctor = get_object_or_404(Doctor, id=doctor_id)

    return render(request, 'doctors/show_timesheet.html', {
        'doctor': doctor,
        'doctor_id': doctor_id,
        'timesheet_slots': timesheet_slots,
    })


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


@login_required
def reserve_visit_time(request,doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    office = doctor.offices.first()
    patient = request.user

    
    start_str = request.GET.get('start')
    end_str = request.GET.get('end')

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
        
    else:
        redirect('home')

    return render(request, 'doctors/reserve_time.html')



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


@login_required
def book_visit(request,doctor_id) :
    doctor = get_object_or_404 (Doctor , id=doctor_id)

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

def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    doctor_times = Visittime.objects.filter(
        doctor=doctor,
        booked_at__isnull=True,
        canceled_at__isnull=True,
        review__isnull=True
    )
    return render(request, 'doctors/doctor_detail.html', {
        'doctor': doctor,
        'doctor_times': doctor_times
    })

@login_required
def reserve_visit(request, visit_id):
    # گرفتن نوبت موردنظر که هنوز رزرو نشده
    visit = get_object_or_404(
        Visittime,
        id=visit_id,
        patient__isnull=True,
        canceled_at__isnull=True
    )

    # گرفتن یا ساخت کیف پول کاربر
    wallet, _ = Wallet.objects.get_or_create(user=request.user)

    if request.method == "POST":
        price = visit.office.price
        if wallet.inventory >= price:
            # کم کردن موجودی
            Wallet.objects.filter(user=request.user).update(inventory=F('inventory') - price)
            # رزرو نوبت
            visit.patient = request.user
            visit.booked_at = timezone.now()
            visit.save()

            # ارسال ایمیل
            send_mail(
                subject="مشخصات نوبت رزرو شده شما",
                message=f"سلام {request.user.get_full_name()},\n\nنوبت شما رزرو شد.\nتاریخ: {visit.duration_start.strftime('%Y-%m-%d')}\nساعت: {visit.duration_start.strftime('%H:%M')}\nدفتر: {visit.office.location}",
                from_email="noreply@example.com",
                recipient_list=[request.user.email],
                fail_silently=True
            )

            messages.success(request, "✅ نوبت رزرو شد و ایمیل ارسال شد.")
            return redirect('doctor_detail', doctor_id=visit.doctor.id)
        else:
            messages.error(request, "❌ موجودی کافی نیست. لطفاً کیف پول خود را شارژ کنید.")

    return render(request, "doctors/reserve_time.html", {"visit": visit, "wallet": wallet})
