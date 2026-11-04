
from django.contrib import admin
from .models import Department, Category, Product, Ticket


admin.site.register(Department)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Ticket)
