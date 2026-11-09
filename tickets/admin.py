
from django.contrib import admin
from .models import Department, Category, Product, Ticket
from .forms import DepartmentForm


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):

    form = DepartmentForm
    list_display = ('name',)
    search_fields = ('name',)

from .forms import DepartmentForm



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ('name', 'division', 'department')

    list_filter = ('division', 'department')

    search_fields = ('name',)

    ordering = ('division', 'name')





admin.site.register(Product)

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'reporter',
        'division',
        'category',
        'department',
        'status',
        'created_at',
    )

    list_filter = (
        'division',
        'status',
        'department',
    )

    search_fields = (
        'title',
        'description',
        'reporter__username',
    )

    ordering = ('-created_at',)
