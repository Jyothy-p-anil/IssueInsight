
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import StaffAccountCreationForm


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
