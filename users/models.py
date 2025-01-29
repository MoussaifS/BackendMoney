from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    REGION_CHOICES = [
        ('MY', 'Malaysia'),
        ('WW', 'Worldwide'),
    ]
    
    region = models.CharField(max_length=2, choices=REGION_CHOICES)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    is_verified = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.username} ({self.get_region_display()})"
