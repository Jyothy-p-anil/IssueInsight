from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tickets.models import Department, Incident, Ticket


from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from tickets.models import Department, Incident



User = get_user_model()


class IncidentProgressTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.department = Department.objects.create(
            name='Progress Facilities'
        )
        cls.other_department = Department.objects.create(
            name='Progress IT'
        )

        cls.owner = User.objects.create_user(
            username='progress_owner',
            password='TestPass123!',
            role='support',
            department=cls.department,
        )

        cls.other_support = User.objects.create_user(
            username='progress_other_support',
            password='TestPass123!',
            role='support',
            department=cls.department,
        )

        cls.it_support = User.objects.create_user(
            username='progress_it_support',
            password='TestPass123!',
            role='support',
            department=cls.other_department,
        )

        cls.employee = User.objects.create_user(
            username='progress_employee',
            password='TestPass123!',
            role='employee',
        )

        cls.ticket = Ticket.objects.create(
            reporter=cls.employee,
            division='employee',
            title='AC not cooling',
            description='Office AC failure',
            department=cls.department,
            status='submitted',
        )

    def setUp(self):
        self.incident = Incident.objects.create(
            title='AC failure',
            description='Shared cooling issue',
            department=self.department,
            owner=self.owner,
        )
        self.incident.tickets.add(self.ticket)

        self.url = reverse(
            'support_update_incident_status',
            args=[self.incident.pk],
        )

    def test_owner_starts_investigation(self):
        self.client.force_login(self.owner)

        response = self.client.post(
            self.url,
            {'status': 'in_progress'},
        )

        self.incident.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.incident.status, 'in_progress')

    def test_owner_resolves_incident(self):
        self.incident.status = 'in_progress'
        self.incident.save()

        self.client.force_login(self.owner)

        self.client.post(
            self.url,
            {'status': 'resolved',
            'resolution_summary': 'The issue was investigated and repaired successfully.',
            }
        )

        self.incident.refresh_from_db()
        self.assertEqual(self.incident.status, 'resolved')

    def test_cannot_skip_investigation(self):
        self.client.force_login(self.owner)

        self.client.post(
            self.url,
            {'status': 'resolved'},
        )

        self.incident.refresh_from_db()
        self.assertEqual(self.incident.status, 'open')

    def test_other_support_cannot_update(self):
        self.client.force_login(self.other_support)

        self.client.post(
            self.url,
            {'status': 'in_progress'},
        )

        self.incident.refresh_from_db()
        self.assertEqual(self.incident.status, 'open')

    def test_other_department_cannot_update(self):
        self.client.force_login(self.it_support)

        response = self.client.post(
            self.url,
            {'status': 'in_progress'},
        )

        self.incident.refresh_from_db()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(self.incident.status, 'open')

    def test_employee_cannot_update(self):
        self.client.force_login(self.employee)

        self.client.post(
            self.url,
            {'status': 'in_progress'},
        )

        self.incident.refresh_from_db()
        self.assertEqual(self.incident.status, 'open')

    def test_get_request_does_not_update(self):
        self.client.force_login(self.owner)

        response = self.client.get(self.url)

        self.incident.refresh_from_db()
        self.assertEqual(response.status_code, 405)
        self.assertEqual(self.incident.status, 'open')

    def test_resolving_incident_preserves_ticket_status(self):
        self.incident.status = 'in_progress'
        self.incident.save()

        self.client.force_login(self.owner)

        self.client.post(
            self.url,
            {'status': 'resolved'},
        )

        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, 'submitted')

    def test_resolved_incident_cannot_be_reopened(self):
        self.incident.status = 'resolved'
        self.incident.save()

        self.client.force_login(self.owner)

        self.client.post(
            self.url,
            {'status': 'open'},
        )

        self.incident.refresh_from_db()
        self.assertEqual(self.incident.status, 'resolved')




class IncidentResolutionSummaryTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.department = Department.objects.create(
            name='Resolution Test Department'
        )
        cls.owner = get_user_model().objects.create_user(
            username='resolution_owner',
            password='TestPass123!',
            role='support',
            department=cls.department,
        )
        cls.other_staff = get_user_model().objects.create_user(
            username='resolution_other',
            password='TestPass123!',
            role='support',
            department=cls.department,
        )
        cls.incident = Incident.objects.create(
            title='Test resolution',
            description='Testing mandatory summary',
            department=cls.department,
            owner=cls.owner,
            status='in_progress',
        )

    def resolve(self, summary):
        return self.client.post(
            reverse(
                'support_update_incident_status',
                args=[self.incident.pk],
            ),
            {
                'status': 'resolved',
                'resolution_summary': summary,
            },
        )

    def test_owner_can_resolve_with_summary(self):
        self.client.force_login(self.owner)
        self.resolve('Water connection repaired.')

        self.incident.refresh_from_db()
        self.assertEqual(self.incident.status, 'resolved')
        self.assertEqual(
            self.incident.resolution_summary,
            'Water connection repaired.',
        )

    def test_empty_summary_is_rejected(self):
        self.client.force_login(self.owner)
        self.resolve('   ')

        self.incident.refresh_from_db()
        self.assertEqual(self.incident.status, 'in_progress')

    def test_other_staff_cannot_resolve(self):
        self.client.force_login(self.other_staff)
        self.resolve('Unauthorized resolution.')

        self.incident.refresh_from_db()
        self.assertEqual(self.incident.status, 'in_progress')

    def test_summary_length_limit(self):
        self.client.force_login(self.owner)
        self.resolve('A' * 2001)

        self.incident.refresh_from_db()
        self.assertEqual(self.incident.status, 'in_progress')

    def test_resolved_incident_cannot_be_resolved_again(self):
        self.client.force_login(self.owner)
        self.resolve('First resolution.')
        self.resolve('Second resolution.')

        self.incident.refresh_from_db()
        self.assertEqual(
            self.incident.resolution_summary,
            'First resolution.',
        )
