
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from tickets.models import Category, Department, Ticket

User = get_user_model()


class AdminComplaintFilterTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.facilities = Department.objects.create(
            name='Facilities Support'
        )
        cls.product = Department.objects.create(
            name='Product Support'
        )

        cls.facilities_category = Category.objects.create(
            name='Facilities Issues',
            division='employee',
            department=cls.facilities,
        )
        cls.product_category = Category.objects.create(
            name='Software Errors',
            division='customer',
            department=cls.product,
        )

        cls.admin = User.objects.create_user(
            username='filter_admin',
            password='TestPass123!',
            role='admin',
        )
        cls.employee = User.objects.create_user(
            username='filter_employee',
            password='TestPass123!',
            role='employee',
        )

        cls.ac_ticket = Ticket.objects.create(
            reporter=cls.employee,
            division='employee',
            title='AC Not Cooling',
            description='Office air conditioner issue',
            department=cls.facilities,
            category=cls.facilities_category,
            status='submitted',
            urgency='high',
        )

        cls.report_ticket = Ticket.objects.create(
            reporter=cls.employee,
            division='customer',
            title='Report Generation Failure',
            description='Application reporting issue',
            department=cls.product,
            category=cls.product_category,
            status='resolved',
            urgency='low',
        )

        cls.old_ticket = Ticket.objects.create(
            reporter=cls.employee,
            division='employee',
            title='Water Leakage',
            description='Water leaking near stairs',
            department=cls.facilities,
            category=cls.facilities_category,
            status='closed',
            urgency='medium',
        )

        Ticket.objects.filter(
            pk=cls.old_ticket.pk
        ).update(
            created_at=timezone.now() - timedelta(days=30)
        )

    def setUp(self):
        self.url = reverse('admin_all_complaints')
        self.client.force_login(self.admin)

    def check_results(self, params, expected_ids):
        response = self.client.get(self.url, params)

        self.assertEqual(response.status_code, 200)
        actual_ids = {
            ticket.pk for ticket in response.context['tickets']
        }
        self.assertEqual(actual_ids, set(expected_ids))

    def test_admin_access(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_non_admin_access_denied(self):
        self.client.force_login(self.employee)
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)

    def test_search_by_title(self):
        self.check_results(
            {'q': 'AC'},
            [self.ac_ticket.pk],
        )

    def test_search_by_ticket_id(self):
        self.check_results(
            {'q': f'#{self.ac_ticket.pk}'},
            [self.ac_ticket.pk],
        )

    def test_status_filter(self):
        self.check_results(
            {'status': 'resolved'},
            [self.report_ticket.pk],
        )

    def test_department_filter(self):
        self.check_results(
            {'department': str(self.facilities.pk)},
            [self.ac_ticket.pk, self.old_ticket.pk],
        )

    def test_division_filter(self):
        self.check_results(
            {'division': 'customer'},
            [self.report_ticket.pk],
        )

    def test_category_filter(self):
        self.check_results(
            {'category': str(self.product_category.pk)},
            [self.report_ticket.pk],
        )

    def test_urgency_filter(self):
        self.check_results(
            {'urgency': 'high'},
            [self.ac_ticket.pk],
        )

    def test_date_range_filter(self):
        today = timezone.localdate().isoformat()

        self.check_results(
            {'date_from': today, 'date_to': today},
            [self.ac_ticket.pk, self.report_ticket.pk],
        )

    def test_combined_filters(self):
        self.check_results(
            {
                'q': 'AC',
                'department': str(self.facilities.pk),
                'status': 'submitted',
                'urgency': 'high',
            },
            [self.ac_ticket.pk],
        )

    def test_invalid_filters(self):
        self.check_results(
            {
                'status': 'invalid',
                'department': 'abc',
                'category': 'abc',
                'urgency': 'invalid',
                'date_from': 'invalid',
                'date_to': 'invalid',
            },
            [
                self.ac_ticket.pk,
                self.report_ticket.pk,
                self.old_ticket.pk,
            ],
        )
