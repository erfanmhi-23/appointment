from django.db import models

from doctors.models import Doctor,Visittime
from patient.models import Patient

class Review(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="reviews")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="reviews")
    comment = models.TextField(max_length=5000)
    added_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField()
    visit_time = models.ForeignKey(Visittime, on_delete=models.CASCADE)

    def __str__(self):
        return f"Review by {self.patient.user.get_full_name()} for {self.doctor.user.get_full_name()} - Rating: {self.rating}"

