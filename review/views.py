from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
        visit_time_id = request.POST.get("visit_time_id")

        
        if not visit_time_id:
            messages.error(request,"برای نظر دهی اول باید نوبت بگیرید")
            return redirect('doctor_detail', doctor_id=doctor_id)

        visit_time = get_object_or_404(Visittime, id=visit_time_id)

        
        if Review.objects.filter(visit_time=visit_time).exists():
            messages.error(request,"برای این نوبت قبلا نظر داده اید")
            return redirect('doctor_detail', doctor_id=doctor_id)

        if comment_text and rating:
            Review.objects.create(
                doctor=doctor,
                patient=patient,
                comment=comment_text,
                rating=int(rating),
                visit_time=visit_time
            )

        return redirect('doctor_detail', doctor_id=doctor_id)

    return redirect('doctor_detail', doctor_id=doctor_id)
