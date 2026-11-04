
from django.core.management.base import BaseCommand
from tickets.models import Department, Category, Product


class Command(BaseCommand):
    help = 'Create initial IssueInsight data'

    def handle(self, *args, **kwargs):

        departments = [
            'Internal IT Support',
            'Facilities Support',
            'Administration Support',
            'Product Support',
        ]

        for name in departments:
            Department.objects.get_or_create(name=name)

        categories = [
            ('employee', 'IT Issues', 'Internal IT Support'),
            ('employee', 'Facilities Issues', 'Facilities Support'),
            ('employee', 'Administration Issues', 'Administration Support'),
            ('employee', 'Other', None),

            ('customer', 'Login & Access', 'Product Support'),
            ('customer', 'Software Errors', 'Product Support'),
            ('customer', 'Performance Issues', 'Product Support'),
            ('customer', 'Data & Reports', 'Product Support'),
            ('customer', 'Billing, Account & Subscription', 'Product Support'),
            ('customer', 'Security & Privacy', 'Product Support'),
            ('customer', 'Setup & Integration', 'Product Support'),
            ('customer', 'Other', None),
        ]

        for division, name, department_name in categories:
            department = None

            if department_name:
                department = Department.objects.get(
                    name=department_name
                )

            Category.objects.get_or_create(
                name=name,
                division=division,
                defaults={'department': department}
            )

        products = ['PayrollPro', 'InvoiceApp', 'TaskFlow']

        for name in products:
            Product.objects.get_or_create(
                name=name,
                defaults={'is_active': True}
            )

        self.stdout.write(
            self.style.SUCCESS(
                'Initial data setup completed successfully!'
            )
        )
