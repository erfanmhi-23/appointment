from django.db import models
from django.contrib.auth.models import AbstractUser

sex_choices = ((True, "female"), (False, "male"))

class User(AbstractUser):
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    sex = models.BooleanField(choices=sex_choices, null=True, blank=True)

    class Meta:
        db_table = "user"

    def __str__(self):
        return self.username
####email otp
from django.db import models
from django.utils import timezone
import datetime
import random

class EmailOTP(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.email} - {self.code}"
    
    def is_expired(self):
        return timezone.now() > self.created_at + datetime.timedelta(minutes=5)
    
    def generate_otp():
        return f"{random.randint(100000, 999999)}"

                

