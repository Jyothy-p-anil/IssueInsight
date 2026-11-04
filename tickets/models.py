
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):

    DIVISION_CHOICES = [
        ('employee', 'Employee'),
        ('customer', 'Customer'),
    ]

    name = models.CharField(max_length=100)

    division = models.CharField(
        max_length=10,
        choices=DIVISION_CHOICES
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name
