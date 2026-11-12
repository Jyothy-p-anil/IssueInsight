
from django.db import models
from django.conf import settings


from datetime import timedelta
from django.utils import timezone


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

    resolution_summary = models.TextField(
        blank=True
    )

    resolved_at = models.DateTimeField(
        null=True,
        blank=True
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True
    )

    # Step 78: Pending resolution confirmation reminder

    @property
    def confirmation_reminder_due(self):
        if (
            self.status != 'resolved'
            or self.resolved_at is None
        ):
            return False

        return timezone.now() >= (
            self.resolved_at + timedelta(hours=72)
        )
    
    @property
    def response_duration(self):
        if not self.first_response_at:
            return None

        return self.first_response_at - self.created_at

    @property
    def resolution_duration(self):
        if not self.resolved_at:
            return None

        return self.resolved_at - self.created_at


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


# Step 81: Ticket activity and status history

class TicketActivity(models.Model):

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='activities'
    )

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    action = models.CharField(max_length=50)

    old_status = models.CharField(
        max_length=20,
        blank=True
    )

    new_status = models.CharField(
        max_length=20,
        blank=True
    )

    description = models.TextField(blank=True)

    created_at = models.DateTimeField(
        default=timezone.now,
        editable=False
    )

    class Meta:
        ordering = ['created_at', 'id']

    def __str__(self):
        return f'{self.action} - Ticket #{self.ticket_id}'


class Notification(models.Model):

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    message = models.CharField(max_length=255)

    event_key = models.CharField(
    max_length=150,
    null=True,
    blank=True
)

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(
        default=timezone.now,
        editable=False
    )

    class Meta:
        ordering = ['-created_at', '-id']
        constraints = [
            models.UniqueConstraint(
                fields=['recipient', 'event_key'],
                name='unique_notification_per_event'
            )
        ]

    def __str__(self):
        return f'Notification for {self.recipient.username}'
