from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor_profile")
    field = models.CharField(max_length=150)
    expertise = models.TextField(blank=True, null=True)
    np = models.CharField(max_length=10, unique=True)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='doctor_images/', blank=True, null=True)
    
    def __str__(self):
        name = self.user.get_full_name() or self.user.username
        return f"Dr.{name} - {self.field}"

class Office (models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="offices")
    location = models.CharField(max_length=255)
    phone_num = models.CharField(max_length=11)
    price = models.DecimalField(max_digits=8, decimal_places=3)

    def __str__(self):
        return f"{self.doctor} - {self.location}"


class Timesheet(models.Model):
    office = models.ForeignKey(Office, on_delete=models.CASCADE, related_name="time_sheets")
    start = models.DateTimeField()
    end = models.DateTimeField()
    duration = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.office} ({self.start} - {self.end})"



class Visittime(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="visit_times")
    office = models.ForeignKey(Office, on_delete=models.CASCADE, related_name="visit_times")
    patient = models.ForeignKey(User, null=True, blank=True ,on_delete=models.SET_NULL, related_name="visits")
    duration_start = models.DateTimeField()
    duration_end = models.DateTimeField()
    booked_at = models.DateTimeField(null=True, blank=True)
    canceled_at = models.DateTimeField(null=True, blank=True)


    class Meta:
        unique_together = ("doctor", "duration_start")

    def __str__(self):
        return f"{self.doctor} - {self.duration_start} "