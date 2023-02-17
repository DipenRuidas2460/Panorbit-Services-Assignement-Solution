from typing import AbstractSet
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=20)
    otp = models.CharField(max_length=6)



class CustomUser(AbstractSet):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=10)
    email = models.EmailField(unique=True, primary_key=True)
    phone_number = models.CharField(max_length=20)

AUTH_USER_MODEL = 'your_app.CustomUser'