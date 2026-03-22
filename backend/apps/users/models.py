from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLES = [
        ('admin', 'Admin'),
        ('team', 'Team'),
        ('jury', 'Jury'),
    ]
    role = models.CharField(max_length=10, choices=ROLES, default='team')
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50,blank=True)
    last_name = models.CharField(max_length=50,blank=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']



    def __str__(self):
        return f"{self.email} ({self.role})"