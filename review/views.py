from django.shortcuts import render

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from doctors.models import Doctor, Visittime
from patient.models import Patient
from review.models import Review

@login_required
def add_comment(request, doctor_id):
    if request.method == 'POST':
        doctor = get_object_or_404(Doctor, id=doctor_id)
        patient = get_object_or_404(Patient, user=request.user)
        comment_text = request.POST.get("comment_text")
        rating = request.POST.get("rating")
        visit_time = Visittime.objects.first()  # فرضی یا تستی

        if comment_text and rating:
            Review.objects.create(
                doctor=doctor,
                patient=patient,
                comment=comment_text,
                rating=int(rating),
                visit_time=visit_time
            )
        return redirect('doctor_detail', doctor_id=doctor_id)
    else:
        # اگر کاربر با GET اومده به این ویو، می‌تونه ریدایرکت بشه یا 405 بده
        return redirect('doctor_detail', doctor_id=doctor_id)