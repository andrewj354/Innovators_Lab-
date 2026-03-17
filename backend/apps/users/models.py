from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLES = [
        ('admin', 'Admin'),
        ('team', 'Team'),
        ('jury', 'Jury'),
    ]
    role = models.CharField(max_length=10, choices=ROLES, default='team')

    def __str__(self):
        return f"{self.email} ({self.role})"