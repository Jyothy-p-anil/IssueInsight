
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tickets.models import Department, Ticket

User = get_user_model()


class AdminDashboardTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.facilities = Department.objects.create(
            name='Test Facilities'
        )
        cls.product_support = Department.objects.create(
            name='Test Product Support'
        )

        cls.admin = User.objects.create_user(
            username='test_dashboard_admin',
            password='TestPass123!',
            role='admin',
        )

        cls.employee = User.objects.create_user(
            username='test_dashboard_employee',
            password='TestPass123!',
            role='employee',
        )

        cls.customer = User.objects.create_user(
            username='test_dashboard_customer',
            password='TestPass123!',
            role='customer',
        )

        cls.support = User.objects.create_user(
            username='test_dashboard_support',
            password='TestPass123!',
            role='support',
            department=cls.facilities,
        )

        cls.create_ticket(
            cls.employee, 'employee', cls.facilities,
            'submitted', 'Facilities issue'
        )
        cls.create_ticket(
            cls.employee, 'employee', cls.facilities,
            'resolved', 'Resolved facilities issue'
        )
        cls.create_ticket(
            cls.customer, 'customer', cls.product_support,
            'submitted', 'Product issue'
        )
        cls.create_ticket(
            cls.customer, 'customer', cls.product_support,
            'closed', 'Closed product issue'
        )
        cls.create_ticket(
            cls.employee, 'employee', None,
            'submitted', 'Unrouted issue'
        )

    @classmethod
    def create_ticket(cls, reporter, division, department,
                      status, title):
        return Ticket.objects.create(
            reporter=reporter,
            division=division,
            department=department,
            status=status,
            title=title,
            description='Admin dashboard test complaint',
        )

    def setUp(self):
        self.url = reverse('admin_dashboard')
        self.client.force_login(self.admin)

    def test_admin_can_access_dashboard(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'role_dashboard.html'
        )

    def test_non_admin_cannot_access_dashboard(self):
        for user in [self.employee, self.customer, self.support]:
            with self.subTest(role=user.role):
                self.client.force_login(user)
                response = self.client.get(self.url)
                self.assertNotEqual(response.status_code, 200)

    def test_company_wide_statistics(self):
        response = self.client.get(self.url)

        self.assertEqual(response.context['admin_total'], 5)
        self.assertEqual(response.context['admin_employee_total'], 3)
        self.assertEqual(response.context['admin_customer_total'], 2)
        self.assertEqual(response.context['admin_unassigned'], 3)
        self.assertEqual(response.context['admin_resolved'], 1)
        self.assertEqual(response.context['admin_closed'], 1)

    def test_department_filter(self):
        response = self.client.get(self.url, {
            'department': str(self.facilities.id)
        })

        self.assertEqual(response.context['admin_total'], 2)
        self.assertEqual(response.context['admin_employee_total'], 2)
        self.assertEqual(response.context['admin_customer_total'], 0)

    def test_division_filter(self):
        response = self.client.get(self.url, {
            'division': 'customer'
        })

        self.assertEqual(response.context['admin_total'], 2)
        self.assertEqual(response.context['admin_customer_total'], 2)
        self.assertEqual(response.context['admin_employee_total'], 0)

    def test_combined_filters(self):
        response = self.client.get(self.url, {
            'department': str(self.facilities.id),
            'division': 'employee',
        })

        self.assertEqual(response.context['admin_total'], 2)

    def test_invalid_filters(self):
        response = self.client.get(self.url, {
            'department': 'invalid',
            'division': 'invalid',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['admin_total'], 5)

    def test_status_chart_counts(self):
        response = self.client.get(self.url)

        labels = response.context['admin_status_labels']
        counts = response.context['admin_status_counts']
        data = dict(zip(labels, counts))

        self.assertEqual(data['Submitted'], 3)
        self.assertEqual(data['Resolved'], 1)
        self.assertEqual(data['Closed'], 1)
        self.assertEqual(sum(counts), 5)

    def test_department_chart_counts(self):
        response = self.client.get(self.url)

        labels = response.context['department_chart_labels']
        counts = response.context['department_chart_counts']
        data = dict(zip(labels, counts))

        self.assertEqual(data['Test Facilities'], 2)
        self.assertEqual(data['Test Product Support'], 2)
        self.assertEqual(data['Not Yet Routed'], 1)
        self.assertEqual(sum(counts), 5)

    def test_weekly_chart_structure(self):
        response = self.client.get(self.url)

        self.assertEqual(
            len(response.context['admin_trend_labels']), 4
        )
        self.assertEqual(
            len(response.context['admin_trend_received']), 4
        )
        self.assertEqual(
            len(response.context['admin_trend_resolved']), 4
        )
