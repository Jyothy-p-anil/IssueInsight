from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    ROLE_CHOICES = [
        ('employee', 'Employee'),
        ('customer', 'Customer'),
        ('support', 'Support Staff'),
        ('admin', 'Admin'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='customer'
    )