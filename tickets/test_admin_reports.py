
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from tickets.models import Category, Department, Ticket


import csv
from io import StringIO

User = get_user_model()


class AdminReportsTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_user(
            username='reports_admin',
            password='TestPass123!',
            role='admin',
        )
        cls.employee = User.objects.create_user(
            username='reports_employee',
            password='TestPass123!',
            role='employee',
        )

        cls.department = Department.objects.create(
            name='Test Facilities'
        )
        cls.category = Category.objects.create(
            name='Test Maintenance',
            division='employee',
            department=cls.department,
        )

        cls.ticket1 = Ticket.objects.create(
            reporter=cls.employee,
            division='employee',
            department=cls.department,
            category=cls.category,
            title='AC Failure',
            description='Air conditioner not working',
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
            division='customer',
            title='Report Error',
            description='Software report failure',
            status='closed',
            urgency='low',
        )

        now = timezone.now()

        Ticket.objects.filter(pk=cls.ticket1.pk).update(
            created_at=now - timedelta(hours=10),
            first_response_at=now - timedelta(hours=8),
            resolved_at=now - timedelta(hours=4),
        )

        Ticket.objects.filter(pk=cls.ticket3.pk).update(
            created_at=now - timedelta(days=40),
            first_response_at=now - timedelta(days=40) + timedelta(hours=1),
            resolved_at=now - timedelta(days=40) + timedelta(hours=5),
        )

    def setUp(self):
        self.url = reverse('admin_reports')
        self.client.force_login(self.admin)

    def test_admin_can_access_reports(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'tickets/admin_reports.html'
        )

    def test_non_admin_cannot_access(self):
        self.client.force_login(self.employee)
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)

    def test_total_complaints(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context['total'], 3)

    def test_status_counts(self):
        response = self.client.get(self.url)
        counts = {
            item['label']: item['count']
            for item in response.context['status_report']
        }
        self.assertEqual(counts['Resolved'], 1)
        self.assertEqual(counts['Submitted'], 1)
        self.assertEqual(counts['Closed'], 1)

    def test_source_counts(self):
        response = self.client.get(self.url)
        counts = {
            item['label']: item['count']
            for item in response.context['source_report']
        }
        self.assertEqual(counts['Employee'], 2)
        self.assertEqual(counts['Customer'], 1)

    def test_category_counts(self):
        response = self.client.get(self.url)
        counts = {
            item['name']: item['count']
            for item in response.context['category_report']
        }
        self.assertEqual(counts['Test Maintenance'], 2)
        self.assertEqual(counts['Uncategorised'], 1)

    def test_urgency_counts(self):
        response = self.client.get(self.url)
        counts = {
            item['label']: item['count']
            for item in response.context['urgency_report']
        }
        self.assertEqual(counts['High'], 1)
        self.assertEqual(counts['Medium'], 1)
        self.assertEqual(counts['Low'], 1)

    def test_resolution_rate(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context['completed_count'], 2)
        self.assertAlmostEqual(
            response.context['resolution_rate'], 66.67
        )

    def test_average_durations(self):
        response = self.client.get(self.url)
        self.assertAlmostEqual(
            response.context['average_response_hours'], 1.5
        )
        self.assertAlmostEqual(
            response.context['average_resolution_hours'], 5.5
        )

    def test_last_30_days(self):
        response = self.client.get(
            self.url, {'period': 'last30'}
        )
        self.assertEqual(response.context['total'], 2)

    def test_custom_date_range(self):
        today = timezone.localdate().isoformat()

        response = self.client.get(self.url, {
            'period': 'custom',
            'date_from': today,
            'date_to': today,
        })
        self.assertEqual(response.context['total'], 1)

    def test_invalid_date_range(self):
        response = self.client.get(self.url, {
            'period': 'custom',
            'date_from': '2026-12-01',
            'date_to': '2026-11-01',
        })
        self.assertTrue(response.context['filter_error'])
        self.assertEqual(response.context['total'], 3)
    
    def read_csv_response(self, response):
        content = response.content.decode('utf-8-sig')
        return list(csv.reader(StringIO(content)))

    def test_csv_export_downloads(self):
        response = self.client.get(
            self.url, {'export': 'csv'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            'text/csv',
            response['Content-Type']
        )
        self.assertIn(
            'attachment',
            response['Content-Disposition']
        )

    def test_csv_export_contains_total(self):
        response = self.client.get(
            self.url, {'export': 'csv'}
        )
        rows = self.read_csv_response(response)

        self.assertIn(
            ['Total Complaints', '3'],
            rows
        )

    def test_csv_export_contains_statistics(self):
        response = self.client.get(
            self.url, {'export': 'csv'}
        )
        rows = self.read_csv_response(response)

        self.assertIn(['Resolved', '1'], rows)
        self.assertIn(['Submitted', '1'], rows)
        self.assertIn(['Test Maintenance', '2'], rows)
        self.assertIn(['Resolution Rate (%)', '66.67'], rows)

    def test_csv_export_respects_last_30_days(self):
        response = self.client.get(self.url, {
            'period': 'last30',
            'export': 'csv',
        })
        rows = self.read_csv_response(response)

        self.assertIn(
            ['Total Complaints', '2'],
            rows
        )

    def test_non_admin_cannot_export_csv(self):
        self.client.force_login(self.employee)

        response = self.client.get(
            self.url, {'export': 'csv'}
        )

        self.assertNotEqual(response.status_code, 200)
        self.assertNotIn(
            'text/csv',
            response.get('Content-Type', '')
        )

