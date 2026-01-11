from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    is_2fa_enabled=models.BooleanField(default=False)
    otp_secret=models.CharField(max_length=32,blank=True,null=True)
    
