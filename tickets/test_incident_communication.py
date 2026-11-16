
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tickets.models import (
    Department,
    Incident,
    Notification,
    Ticket,
    TicketMessage,
)

User = get_user_model()


class IncidentCommunicationTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.department = Department.objects.create(
            name='Communication Test Facilities'
        )

        cls.owner = User.objects.create_user(
            username='incident_comm_owner',
            password='TestPass123!',
            role='support',
            department=cls.department,
        )

        cls.assignee = User.objects.create_user(
            username='incident_comm_assignee',
            password='TestPass123!',
            role='support',
            department=cls.department,
        )

        cls.reporter = User.objects.create_user(
            username='incident_comm_reporter',
            password='TestPass123!',
            role='employee',
        )

        cls.ticket1 = Ticket.objects.create(
            reporter=cls.reporter,
            division='employee',
            title='AC failure - Room 1',
            description='AC not cooling.',
            department=cls.department,
            assigned_to=cls.assignee,
            status='in_progress',
        )

        cls.ticket2 = Ticket.objects.create(
            reporter=cls.reporter,
            division='employee',
            title='AC failure - Room 2',
            description='AC not working.',
            department=cls.department,
            status='submitted',
        )

    def setUp(self):
        self.incident = Incident.objects.create(
            title='Building AC Failure',
            description='Shared AC problem',
            department=self.department,
            owner=self.owner,
            status='in_progress',
        )

        self.incident.tickets.add(
            self.ticket1,
            self.ticket2,
        )

        self.client.force_login(self.owner)

    def resolve_incident(self, summary='AC system repaired.'):
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

    def test_public_messages_created_for_all_linked_tickets(self):
        self.resolve_incident()

        for ticket in (self.ticket1, self.ticket2):
            message = TicketMessage.objects.get(ticket=ticket)

            self.assertFalse(message.is_internal)
            self.assertEqual(message.author, self.owner)
            self.assertIn('Building AC Failure', message.body)
            self.assertIn('AC system repaired.', message.body)

    def test_reporter_and_assignee_receive_notifications(self):
        self.resolve_incident()

        self.assertTrue(
            Notification.objects.filter(
                ticket=self.ticket1,
                recipient=self.reporter,
            ).exists()
        )
        self.assertTrue(
            Notification.objects.filter(
                ticket=self.ticket1,
                recipient=self.assignee,
            ).exists()
        )
        self.assertTrue(
            Notification.objects.filter(
                ticket=self.ticket2,
                recipient=self.reporter,
            ).exists()
        )

        self.assertEqual(Notification.objects.count(), 3)

    def test_ticket_statuses_and_assignments_unchanged(self):
        self.resolve_incident()

        self.ticket1.refresh_from_db()
        self.ticket2.refresh_from_db()

        self.assertEqual(self.ticket1.status, 'in_progress')
        self.assertEqual(self.ticket2.status, 'submitted')
        self.assertEqual(self.ticket1.assigned_to, self.assignee)
        self.assertIsNone(self.ticket2.assigned_to)

    def test_duplicate_resolution_does_not_duplicate_messages(self):
        self.resolve_incident()
        self.resolve_incident('Second resolution attempt.')

        self.incident.refresh_from_db()

        self.assertEqual(self.incident.status, 'resolved')
        self.assertEqual(
            self.incident.resolution_summary,
            'AC system repaired.',
        )
        self.assertEqual(TicketMessage.objects.count(), 2)
        self.assertEqual(Notification.objects.count(), 3)

    def test_invalid_summary_does_not_send_messages(self):
        self.resolve_incident('   ')

        self.incident.refresh_from_db()

        self.assertEqual(self.incident.status, 'in_progress')
        self.assertFalse(TicketMessage.objects.exists())
        self.assertFalse(Notification.objects.exists())

    def test_non_owner_cannot_trigger_communication(self):
        self.client.force_login(self.assignee)
        self.resolve_incident()

        self.incident.refresh_from_db()

        self.assertEqual(self.incident.status, 'in_progress')
        self.assertFalse(TicketMessage.objects.exists())
        self.assertFalse(Notification.objects.exists())
