
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (
        ('IssueInsight Details', {
            'fields': ('role', 'department')
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('IssueInsight Details', {
            'fields': ('role', 'department')
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
