
from django.contrib import admin
from .models import Department, Category, Product, Ticket


admin.site.register(Department)



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ('name', 'division', 'department')

    list_filter = ('division', 'department')

    search_fields = ('name',)

    ordering = ('division', 'name')





admin.site.register(Product)
admin.site.register(Ticket)
