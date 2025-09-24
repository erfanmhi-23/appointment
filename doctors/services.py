from datetime import timedelta
from django.db.models import OuterRef, Exists
from .models import Doctor, Timesheet, Visittime

def get_available_timesheets_for_doctor(doctor_id):
    doctor_offices = Doctor.objects.get(id=doctor_id).offices.all()

    timesheets = Timesheet.objects.filter(
        office__in=doctor_offices
    )

    visittimes = Visittime.objects.filter(
    doctor_id=doctor_id,
    office=OuterRef('office'),
    booked_at__isnull=True,  
    canceled_at__isnull=True,  
    duration_start__lt=OuterRef('end'),
    duration_end__gt=OuterRef('start'),
)

    timesheets = timesheets.annotate(
        is_reserved=Exists(visittimes)
    ).filter(is_reserved=False)

    return timesheets


def available_time_slots(timesheet):
    slots = []
    start = timesheet.start
    end = timesheet.end
    duration = timedelta(minutes=timesheet.duration)

    current = start
    while current + duration <= end:
        slot_start = current
        slot_end = current + duration

        reserved = Visittime.objects.filter(
        office=timesheet.office,
        doctor=timesheet.office.doctor,
        booked_at__isnull=False,  
        canceled_at__isnull=True,
        duration_start__lt=slot_end,
        duration_end__gt=slot_start,
        ).exists()

        if not reserved:
            slots.append({
                'start': slot_start,
                'end': slot_end
            })

        current += duration

    return slots


def get_available_timeslots_for_doctor(doctor_id):
    timesheets = get_available_timesheets_for_doctor(doctor_id)

    timesheet_slots = {}
    for ts in timesheets:
        timesheet_slots[ts] = available_time_slots(ts)

    return timesheet_slots
