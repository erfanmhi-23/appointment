from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from doctors.models import Doctor, Visittime
from patient.models import Patient
from review.models import Review
from datetime import date

@login_required
def add_comment(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)

    # اگر Patient موجود نباشه، خودکار بساز
    patient, created = Patient.objects.get_or_create(
        user=request.user,
        defaults={
            'name': request.user.get_full_name() or "کاربر",
            'birth_date': date(2000,1,1)  # مقدار پیش‌فرض
        }
    )

    if request.method == 'POST':
        comment_text = request.POST.get("comment_text")
        rating = request.POST.get("rating")
        visit_time_id = request.POST.get("visit_time_id")

        if not visit_time_id:
            messages.error(request, "برای نظر دادن باید ابتدا یک نوبت انتخاب کنید.")
            return redirect('doctor_detail', doctor_id=doctor_id)

        visit_time = get_object_or_404(Visittime, id=visit_time_id)

        if Review.objects.filter(visit_time=visit_time).exists():
            messages.error(request, "برای این نوبت قبلا نظر داده‌اید.")
            return redirect('doctor_detail', doctor_id=doctor_id)

        if comment_text and rating:
            Review.objects.create(
                doctor=doctor,
                patient=patient,
                comment=comment_text,
                rating=int(rating),
                visit_time=visit_time
            )
            messages.success(request, "نظر شما با موفقیت ثبت شد.")

    return redirect('doctor_detail', doctor_id=doctor_id)