
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import StaffAccountCreationForm






import logging

from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction

from .services import send_password_setup_email


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
        'is_active',
        'is_staff',
        'is_superuser',
    )

    list_filter = (
        'role',
        'department',
        'is_active',
        'is_staff',
    )



    

    def save_model(self, request, obj, form, change):
        previous_active = None

        if change:
            previous_active = User.objects.filter(
                pk=obj.pk
            ).values_list('is_active', flat=True).first()

        super().save_model(request, obj, form, change)



        if not change and obj.role in ('employee', 'support'):
            send_password_setup_email(request, obj)

            
        if change and previous_active is not None:
            if previous_active != obj.is_active and obj.email:

                status = (
                    'reactivated' if obj.is_active
                    else 'deactivated'
                )

                def send_status_email():
                    try:
                        send_mail(
                            subject=f'IssueInsight Account {status.title()}',
                            message=(
                                f'Hello {obj.username},\n\n'
                                f'Your IssueInsight account has been '
                                f'{status}.\n\n'
                                'Thank you,\nIssueInsight Team'
                            ),
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[obj.email],
                            fail_silently=False,
                        )
                    except Exception:
                        logger.exception(
                            'Account status email failed for user %s',
                            obj.pk
                        )

                transaction.on_commit(send_status_email)

