from django import forms
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


class EmailForm(forms.Form):
    email = forms.EmailField(label="ایمیل", max_length=255)
