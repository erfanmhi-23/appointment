from django.db import models

from .models import Doctor , Patient , Visittime

class review(models.Model):
    doctor_id = models.OneToManyField(Doctor,on_delete=models.CASCADE,related_name="doc_name")
    paitent_id = models.OneToManyField(Patient,on_delete=models.CASCADE,related_name="pat_name")
    comment = models.TextField(max_length=5000)
    added_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField()
    visit_time_id = models.OneToOneField(Visittime, on_delete=models.CASCADE)

