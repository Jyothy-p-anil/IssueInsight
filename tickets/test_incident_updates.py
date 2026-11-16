
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tickets.models import Department, Incident, IncidentUpdate, Ticket

User = get_user_model()


class IncidentInvestigationUpdateTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.facilities = Department.objects.create(name='Facilities Test')
        cls.it = Department.objects.create(name='IT Test')

        cls.owner = User.objects.create_user(
            username='update_owner',
            password='TestPass123!',
            role='support',
            department=cls.facilities,
        )
        cls.colleague = User.objects.create_user(
            username='update_colleague',
            password='TestPass123!',
            role='support',
            department=cls.facilities,
        )
        cls.other_department = User.objects.create_user(
            username='update_it_staff',
            password='TestPass123!',
            role='support',
            department=cls.it,
        )
        cls.employee = User.objects.create_user(
            username='update_employee',
            password='TestPass123!',
            role='employee',
        )

        cls.ticket = Ticket.objects.create(
            reporter=cls.employee,
            division='employee',
            title='Water dispenser failure',
            description='Water dispenser not working.',
            department=cls.facilities,
            status='submitted',
        )

        cls.incident = Incident.objects.create(
            title='Water dispenser incident',
            description='Shared workplace issue',
            department=cls.facilities,
            owner=cls.owner,
        )
        cls.incident.tickets.add(cls.ticket)

    def update_url(self):
        return reverse(
            'support_add_incident_update',
            args=[self.incident.pk],
        )

    def test_owner_can_add_update(self):
        self.client.force_login(self.owner)

        response = self.client.post(
            self.update_url(),
            {'body': 'Maintenance inspected the dispenser.'},
        )

        self.assertEqual(response.status_code, 302)
        update = IncidentUpdate.objects.get()
        self.assertEqual(update.author, self.owner)
        self.assertEqual(update.incident, self.incident)

    def test_other_support_cannot_add_update(self):
        self.client.force_login(self.colleague)

        self.client.post(
            self.update_url(),
            {'body': 'Unauthorized update'},
        )

        self.assertFalse(IncidentUpdate.objects.exists())

    def test_other_department_cannot_access_incident(self):
        self.client.force_login(self.other_department)

        response = self.client.post(
            self.update_url(),
            {'body': 'Unauthorized update'},
        )

        self.assertEqual(response.status_code, 404)
        self.assertFalse(IncidentUpdate.objects.exists())

    def test_empty_update_is_rejected(self):
        self.client.force_login(self.owner)

        self.client.post(
            self.update_url(),
            {'body': '   '},
        )

        self.assertFalse(IncidentUpdate.objects.exists())

    def test_resolved_incident_rejects_updates(self):
        self.incident.status = 'resolved'
        self.incident.save(update_fields=['status'])

        self.client.force_login(self.owner)

        self.client.post(
            self.update_url(),
            {'body': 'Late investigation update'},
        )

        self.assertFalse(IncidentUpdate.objects.exists())

    def test_update_does_not_change_ticket_status(self):
        self.client.force_login(self.owner)

        self.client.post(
            self.update_url(),
            {'body': 'Repair investigation started.'},
        )

        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, 'submitted')
        self.assertEqual(IncidentUpdate.objects.count(), 1)
