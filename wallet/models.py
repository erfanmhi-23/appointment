from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL
# Create your models here.
class wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wallet")
    cart_num= models.PositiveIntegerFiel(max_length=16)
    inventory= models.PositiveIntegerField(max_length=15)


    def __str__(self):
        return f"{self.user.get_full_name()} with {self.inventory} ({self.balance})"