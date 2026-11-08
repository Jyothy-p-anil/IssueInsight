
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import StaffAccountCreationForm








from .services import (
    send_password_setup_email,
    send_account_status_email,
)


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
            if previous_active != obj.is_active:
                send_account_status_email(obj)

        
        