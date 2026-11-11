
from django.db import models
from django.conf import settings



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


class Product(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name



class Ticket(models.Model):

    DIVISION_CHOICES = [
        ('employee', 'Employee'),
        ('customer', 'Customer'),
    ]

    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
        ('reopened', 'Reopened'),
    ]

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='reported_tickets'
    )

    division = models.CharField(
        max_length=10,
        choices=DIVISION_CHOICES
    )

    title = models.CharField(max_length=200)
    description = models.TextField()

    floor = models.CharField(
        max_length=30,
        blank=True
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    other_product_name = models.CharField(
        max_length=100,
        blank=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tickets'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='submitted'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    first_response_at = models.DateTimeField(
        null=True,
        blank=True
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True
    )
    def __str__(self):
        return self.title


class TicketMessage(models.Model):

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='ticket_messages'
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='written_ticket_messages'
    )

    body = models.TextField()

    is_internal = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at', 'id']

    def __str__(self):
        return f'Message #{self.pk} on Ticket #{self.ticket_id}'
