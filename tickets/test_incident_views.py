
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tickets.models import Department, Incident, Ticket

User = get_user_model()


class IncidentViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.facilities = Department.objects.create(name="Facilities")
        cls.it = Department.objects.create(name="IT")

        cls.support = User.objects.create_user(
            username="incident_view_support",
            password="TestPass123!",
            role="support",
            department=cls.facilities,
        )
        cls.other_support = User.objects.create_user(
            username="incident_view_other",
            password="TestPass123!",
            role="support",
            department=cls.it,
        )
        cls.employee = User.objects.create_user(
            username="incident_view_employee",
            password="TestPass123!",
            role="employee",
        )
        cls.ticket = Ticket.objects.create(
            reporter=cls.employee,
            division="employee",
            title="AC failure",
            description="Office AC not cooling.",
            department=cls.facilities,
        )
        cls.second_ticket = Ticket.objects.create(
            reporter=cls.employee,
            division="employee",
            title="Another AC failure",
            description="Second AC complaint.",
            department=cls.facilities,
        )

    def test_support_can_create_incident(self):
        self.client.force_login(self.support)

        response = self.client.post(
            reverse('support_create_incident', args=[self.ticket.pk]),
            {'title': 'AC outage', 'description': 'Shared AC issue'},
        )

        self.assertEqual(response.status_code, 302)
        incident = Incident.objects.get()
        self.assertEqual(incident.owner, self.support)
        self.assertTrue(incident.tickets.filter(pk=self.ticket.pk).exists())

    def test_employee_cannot_create_incident(self):
        self.client.force_login(self.employee)

        self.client.post(
            reverse('support_create_incident', args=[self.ticket.pk]),
            {'title': 'AC outage', 'description': 'Shared AC issue'},
        )

        self.assertFalse(Incident.objects.exists())

    def test_other_department_cannot_create_incident(self):
        self.client.force_login(self.other_support)

        self.client.post(
            reverse('support_create_incident', args=[self.ticket.pk]),
            {'title': 'AC outage', 'description': 'Shared AC issue'},
        )

        self.assertFalse(Incident.objects.exists())

    def test_department_incident_list_is_restricted(self):
        Incident.objects.create(
            title='IT incident',
            description='Network problem',
            department=self.it,
            owner=self.other_support,
        )
        self.client.force_login(self.support)

        response = self.client.get(reverse('support_incident_list'))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'IT incident')

    def test_support_can_link_second_ticket(self):
        incident = Incident.objects.create(
            title='AC outage',
            description='Shared AC issue',
            department=self.facilities,
            owner=self.support,
        )
        incident.tickets.add(self.ticket)
        self.client.force_login(self.support)

        response = self.client.post(
            reverse('support_link_incident_ticket', args=[incident.pk]),
            {'ticket_ids': [str(self.second_ticket.pk)]}
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(incident.tickets.count(), 2)

    def test_duplicate_incident_creation_is_rejected(self):
        incident = Incident.objects.create(
            title='Existing incident',
            description='Existing shared issue',
            department=self.facilities,
            owner=self.support,
        )
        incident.tickets.add(self.ticket)
        self.client.force_login(self.support)

        self.client.post(
            reverse('support_create_incident', args=[self.ticket.pk]),
            {'title': 'Duplicate', 'description': 'Duplicate issue'},
        )

        self.assertEqual(Incident.objects.count(), 1)

    def test_other_department_cannot_view_incident(self):
        incident = Incident.objects.create(
            title='IT incident',
            description='Network issue',
            department=self.it,
            owner=self.other_support,
        )
        self.client.force_login(self.support)

        response = self.client.get(
            reverse('support_incident_detail', args=[incident.pk])
        )

        self.assertEqual(response.status_code, 404)
