
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from tickets.models import Category, Department, Ticket


User = get_user_model()


class SupportReportsTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.department = Department.objects.create(
            name='Facilities Test'
        )
        cls.other_department = Department.objects.create(
            name='IT Test'
        )

        cls.support = User.objects.create_user(
            username='reports_support',
            password='TestPass123!',
            role='support',
            department=cls.department,
        )
        cls.other_support = User.objects.create_user(
            username='reports_other_support',
            password='TestPass123!',
            role='support',
            department=cls.other_department,
        )
        cls.employee = User.objects.create_user(
            username='reports_employee_support',
            password='TestPass123!',
            role='employee',
        )
        cls.admin = User.objects.create_user(
            username='reports_admin_support',
            password='TestPass123!',
            role='admin',
        )

        cls.category = Category.objects.create(
            name='AC Maintenance Test',
            division='employee',
            department=cls.department,
        )

        cls.ticket1 = Ticket.objects.create(
            reporter=cls.employee,
            division='employee',
            department=cls.department,
            category=cls.category,
            assigned_to=cls.support,
            title='AC Not Working',
            description='AC failure in office',
            status='resolved',
            urgency='high',
        )

        cls.ticket2 = Ticket.objects.create(
            reporter=cls.employee,
            division='employee',
            department=cls.department,
            category=cls.category,
            title='Water Leakage',
            description='Water leakage in office',
            status='submitted',
            urgency='medium',
        )

        cls.ticket3 = Ticket.objects.create(
            reporter=cls.employee,
            division='employee',
            department=cls.other_department,
            assigned_to=cls.other_support,
            title='Laptop Issue',
            description='Laptop is not working',
            status='closed',
            urgency='low',
        )

        now = timezone.now()

        Ticket.objects.filter(pk=cls.ticket1.pk).update(
            created_at=now - timedelta(hours=10),
            first_response_at=now - timedelta(hours=8),
            resolved_at=now - timedelta(hours=4),
        )

        Ticket.objects.filter(pk=cls.ticket2.pk).update(
            created_at=now - timedelta(days=40),
        )

    def setUp(self):
        self.url = reverse('support_reports')
        self.client.force_login(self.support)

    def test_support_can_access_reports(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'tickets/support_reports.html'
        )

    def test_employee_cannot_access_reports(self):
        self.client.force_login(self.employee)

        response = self.client.get(self.url)

        self.assertNotEqual(response.status_code, 200)

    def test_admin_cannot_access_support_reports(self):
        self.client.force_login(self.admin)

        response = self.client.get(self.url)

        self.assertNotEqual(response.status_code, 200)

    def test_department_isolation(self):
        response = self.client.get(self.url)

        self.assertEqual(response.context['total'], 2)
        self.assertEqual(
            response.context['department_name'],
            'Facilities Test'
        )

        self.client.force_login(self.other_support)
        response = self.client.get(self.url)

        self.assertEqual(response.context['total'], 1)
        self.assertEqual(
            response.context['department_name'],
            'IT Test'
        )

    def test_status_and_urgency_counts(self):
        response = self.client.get(self.url)

        status_counts = {
            item['label']: item['count']
            for item in response.context['status_report']
        }

        urgency_counts = {
            item['label']: item['count']
            for item in response.context['urgency_report']
        }

        self.assertEqual(status_counts['Resolved'], 1)
        self.assertEqual(status_counts['Submitted'], 1)
        self.assertEqual(urgency_counts['High'], 1)
        self.assertEqual(urgency_counts['Medium'], 1)

    def test_assignment_counts(self):
        response = self.client.get(self.url)

        self.assertEqual(response.context['assigned_count'], 1)
        self.assertEqual(response.context['unassigned_count'], 1)
        self.assertEqual(response.context['completed_count'], 1)

    def test_category_and_resolution_performance(self):
        response = self.client.get(self.url)

        categories = {
            item['name']: item['count']
            for item in response.context['category_report']
        }

        self.assertEqual(categories['AC Maintenance Test'], 2)
        self.assertAlmostEqual(
            response.context['resolution_rate'], 50.0
        )
        self.assertAlmostEqual(
            response.context['average_response_hours'], 2.0
        )
        self.assertAlmostEqual(
            response.context['average_resolution_hours'], 6.0
        )

    
    def test_corrected_department_category_count(self):
        other_category = Category.objects.create(
            name='IT Hardware Test',
            division='employee',
            department=self.other_department,
        )

        Ticket.objects.filter(
            pk=self.ticket2.pk
        ).update(
            category=other_category
        )

        response = self.client.get(self.url)

        categories = {
            item['name']: item['count']
            for item in response.context['category_report']
        }

        self.assertEqual(
            categories['AC Maintenance Test'], 1
        )
        self.assertEqual(
            categories['IT Hardware Test'], 1
        )
        self.assertEqual(
            sum(categories.values()), 2
        )


    def test_last_30_days(self):
        response = self.client.get(
            self.url, {'period': 'last30'}
        )

        self.assertEqual(response.context['total'], 1)
        self.assertEqual(
            response.context['completed_count'], 1
        )

    
    
    def test_custom_date_range(self):
        ticket = Ticket.objects.get(pk=self.ticket1.pk)

        ticket_date = timezone.localtime(
            ticket.created_at
        ).date().isoformat()

        response = self.client.get(self.url, {
            'period': 'custom',
            'date_from': ticket_date,
            'date_to': ticket_date,
        })

        self.assertEqual(response.context['total'], 1)



    def test_invalid_date_range(self):
        response = self.client.get(self.url, {
            'period': 'custom',
            'date_from': '2026-12-01',
            'date_to': '2026-11-01',
        })

        self.assertTrue(response.context['filter_error'])
        self.assertEqual(response.context['total'], 2)
