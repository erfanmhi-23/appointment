from django.db.models import OuterRef, Exists, Subquery
from .models import Timesheet, Visittime, Doctor

def get_available_timesheets_for_doctor(doctor_id):
    # گرفتن دفاتر دکتر
    doctor_offices = Doctor.objects.get(id=doctor_id).offices.all()

    # گرفتن تایم‌شیت‌هایی که هنوز رزرو نشدن
    timesheets = Timesheet.objects.filter(
        office__in=doctor_offices
    )

    # Visittimeهای مرتبط با هر تایم‌شیت خاص
    visittimes = Visittime.objects.filter(
        doctor_id=doctor_id,
        office=OuterRef('office'),
        duration_start__gte=OuterRef('start'),
        duration_start__lt=OuterRef('end'),
        canceled_at__isnull=True  # فقط رزروهای معتبر
    )

    # Annotate برای تشخیص اینکه تایم‌شیت رزرو شده یا نه
    timesheets = timesheets.annotate(
        is_reserved=Exists(visittimes)
    ).filter(is_reserved=False)  # فقط تایم‌های آزاد

    return timesheets
