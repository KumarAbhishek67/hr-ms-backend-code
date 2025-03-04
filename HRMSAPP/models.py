from django.db import models
from django.contrib.auth.models import AbstractUser

class HR(AbstractUser):
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    email = models.CharField(max_length=200, unique=True)
    username = models.CharField(max_length=255, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    gender = models.CharField(max_length=100, choices=GENDER, default='Female', null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    IsDeleted = models.BooleanField(default=False)

    def __str__(self):
        return self.email
    
