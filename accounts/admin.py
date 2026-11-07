
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import StaffAccountCreationForm



import logging

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import transaction
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


logger = logging.getLogger(__name__)

@admin.register(User)
class CustomUserAdmin(UserAdmin):

    add_form = StaffAccountCreationForm

    fieldsets = UserAdmin.fieldsets + (
        ('IssueInsight Details', {
            'fields': ('role', 'department')
        }),
    )

    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'department'),
        }),
    )


    list_display = (
        'username',
        'email',
        'role',
        'department',
        'is_staff',
        'is_superuser',
    )

    list_filter = (
        'role',
        'department',
        'is_staff',
    )


    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not change and obj.role in ('employee', 'support'):

            uid = urlsafe_base64_encode(force_bytes(obj.pk))
            token = default_token_generator.make_token(obj)

            path = reverse(
                'password_reset_confirm',
                kwargs={'uidb64': uid, 'token': token}
            )

            setup_link = request.build_absolute_uri(path)

            def send_setup_email():
                try:
                    send_mail(
                        subject='Set Up Your IssueInsight Password',
                        message=(
                            f'Hello {obj.username},\n\n'
                            'Your IssueInsight account has been created.\n\n'
                            'Set your password using this link:\n'
                            f'{setup_link}\n\n'
                            'Thank you,\nIssueInsight Team'
                        ),
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[obj.email],
                        fail_silently=False,
                    )
                except Exception:
                    logger.exception(
                        'Password setup email failed for user %s',
                        obj.pk
                    )

            transaction.on_commit(send_setup_email)
