from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """
    User model with extra information while Django still handles the authentication process
    """
    company_name = models.CharField(blank=False, max_length=100, verbose_name='Company name')
    email = models.EmailField(blank=False, max_length=254, verbose_name='Email')
    phone = models.CharField(max_length=10, verbose_name="Phone number")
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=4, null=True, blank=True)
