from datetime import timedelta
from doctors.models import Timesheet, Visittime

def get_available_timesheet(timesheet_id):
    try:
        timesheet = Timesheet.objects.get(id=timesheet_id)
    except Timesheet.DoesNotExist:
        return None

    visittimes = Visittime.objects.filter(
        doctor=timesheet.office.doctor,
        office=timesheet.office,
        booked_at__isnull=True,
        canceled_at__isnull=True,
        duration_start__lt=timesheet.end,
        duration_end__gt=timesheet.start,
    )

    if visittimes.exists():
        return None  
    return timesheet


def get_available_time_slots_for_timesheet(timesheet_id):
    timesheet = get_available_timesheet(timesheet_id)
    if not timesheet:
        return []  

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
