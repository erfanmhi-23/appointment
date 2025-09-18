from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Patient(models.Model) :
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="patient_profile")
    na_id = models.CharField(max_length=10)
    birth_date = models.DateField()

    def __str__(self):
        return f"paitent {self.user.get_full_name()} , birthtime {self.birth_date}"
    