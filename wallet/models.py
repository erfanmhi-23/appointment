from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


User = settings.AUTH_USER_MODEL

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wallet")
    cart_num = models.PositiveBigIntegerField(
        validators=[MaxValueValidator(9999999999999999)]  # 16 digit
    )
    inventory = models.PositiveBigIntegerField(
        validators=[MaxValueValidator(999999999999999)]   # 15 digit

    def __str__(self):
        return f"{self.user.get_full_name()} with {self.inventory}"
