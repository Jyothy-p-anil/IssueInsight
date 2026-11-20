
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tickets.models import Department, Ticket

User = get_user_model()


class SupportDashboardTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.department = Department.objects.create(
            name='Dashboard Facilities'
        )
        cls.other_department = Department.objects.create(
            name='Dashboard Product'
        )

        cls.support = User.objects.create_user(
            username='dashboard_support',
            password='TestPass123!',
            role='support',
            department=cls.department,
        )

        cls.other_support = User.objects.create_user(
            username='dashboard_other_support',
            password='TestPass123!',
            role='support',
            department=cls.other_department,
        )

        cls.no_department_support = User.objects.create_user(
            username='dashboard_no_department',
            password='TestPass123!',
            role='support',
        )

        cls.customer = User.objects.create_user(
            username='dashboard_customer',
            password='TestPass123!',
            role='customer',
        )

        cls.assigned_ticket = Ticket.objects.create(
            reporter=cls.customer,
            division='customer',
            department=cls.department,
            assigned_to=cls.support,
            title='Assigned dashboard issue',
            description='Assigned ticket for dashboard testing',
            status='in_progress',
        )

        cls.resolved_ticket = Ticket.objects.create(
            reporter=cls.customer,
            division='customer',
            department=cls.department,
            assigned_to=cls.support,
            title='Resolved dashboard issue',
            description='Resolved ticket for dashboard testing',
            status='resolved',
        )

        cls.unassigned_ticket = Ticket.objects.create(
            reporter=cls.customer,
            division='customer',
            department=cls.department,
            title='Unassigned dashboard issue',
            description='Unassigned ticket for dashboard testing',
            status='submitted',
        )

        cls.other_department_ticket = Ticket.objects.create(
            reporter=cls.customer,
            division='customer',
            department=cls.other_department,
            assigned_to=cls.other_support,
            title='Private other department issue',
            description='Must not appear in dashboard statistics',
            status='submitted',
        )

    def setUp(self):
        self.url = reverse('support_dashboard')

    def test_support_can_access_dashboard(self):
        self.client.force_login(self.support)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'role_dashboard.html'
        )

    def test_department_statistics(self):
        self.client.force_login(self.support)
        response = self.client.get(self.url)

        self.assertEqual(response.context['department_total'], 3)
        self.assertEqual(response.context['assigned_to_me'], 2)
        self.assertEqual(response.context['resolved_by_me'], 1)
        self.assertEqual(response.context['unassigned_count'], 1)

    def test_other_department_excluded(self):
        self.client.force_login(self.support)
        response = self.client.get(self.url)

        self.assertEqual(response.context['department_total'], 3)

        self.assertNotContains(
            response,
            'Private other department issue'
        )

    def test_status_chart_data(self):
        self.client.force_login(self.support)
        response = self.client.get(self.url)

        labels = response.context['status_chart_labels']
        counts = response.context['status_chart_counts']

        status_data = dict(zip(labels, counts))

        self.assertEqual(status_data['Submitted'], 1)
        self.assertEqual(status_data['In Progress'], 1)
        self.assertEqual(status_data['Resolved'], 1)

    def test_no_department_warning(self):
        self.client.force_login(self.no_department_support)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['department_missing'])

        self.assertContains(
            response,
            'no support department assigned'
        )

    def test_customer_cannot_access_support_dashboard(self):
        self.client.force_login(self.customer)
        response = self.client.get(self.url)

        self.assertNotEqual(response.status_code, 200)
