
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from tickets.models import Department, Incident, Ticket
from tickets.services.incident_management import (
    create_incident,
    link_ticket_to_incident,
)

User = get_user_model()


class IncidentCreationTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.facilities = Department.objects.create(
            name="Facilities"
        )
        cls.it = Department.objects.create(
            name="IT"
        )

        cls.support = User.objects.create_user(
            username="incident_support",
            password="TestPass123!",
            role="support",
            department=cls.facilities,
        )

        cls.other_support = User.objects.create_user(
            username="incident_other_support",
            password="TestPass123!",
            role="support",
            department=cls.it,
        )

        cls.employee = User.objects.create_user(
            username="incident_employee",
            password="TestPass123!",
            role="employee",
        )

        cls.ticket = Ticket.objects.create(
            reporter=cls.employee,
            division="employee",
            title="AC not cooling",
            description="Office AC is not cooling on Floor 2.",
            department=cls.facilities,
        )

    def test_creator_becomes_incident_owner(self):
        incident = create_incident(
            user=self.support,
            title="Floor 2 AC failure",
            description="Multiple AC complaints on Floor 2.",
            ticket=self.ticket,
        )

        self.assertEqual(incident.owner, self.support)
        self.assertEqual(incident.department, self.facilities)
        self.assertEqual(incident.status, "open")
        self.assertTrue(
            incident.tickets.filter(pk=self.ticket.pk).exists()
        )

    def test_other_department_cannot_create_incident(self):
        with self.assertRaises(ValidationError):
            create_incident(
                user=self.other_support,
                title="Floor 2 AC failure",
                description="AC problem.",
                ticket=self.ticket,
            )

        self.assertEqual(Incident.objects.count(), 0)

    def test_employee_cannot_create_incident(self):
        with self.assertRaises(ValidationError):
            create_incident(
                user=self.employee,
                title="Floor 2 AC failure",
                description="AC problem.",
                ticket=self.ticket,
            )

        self.assertEqual(Incident.objects.count(), 0)

    def test_ticket_assignment_remains_unchanged(self):
        self.ticket.assigned_to = self.support
        self.ticket.status = "in_progress"
        self.ticket.save()

        create_incident(
            user=self.support,
            title="Floor 2 AC failure",
            description="AC problem.",
            ticket=self.ticket,
        )

        self.ticket.refresh_from_db()

        self.assertEqual(self.ticket.assigned_to, self.support)
        self.assertEqual(self.ticket.status, "in_progress")

    def test_cannot_create_second_incident_for_same_ticket(self):
        create_incident(
            user=self.support,
            title="Floor 2 AC failure",
            description="First incident.",
            ticket=self.ticket,
        )

        with self.assertRaises(ValidationError):
            create_incident(
                user=self.support,
                title="Another AC incident",
                description="Duplicate incident.",
                ticket=self.ticket,
            )

        self.assertEqual(Incident.objects.count(), 1)
        self.assertEqual(self.ticket.incidents.count(), 1)

    def test_link_tickets_assigned_to_different_support_staff(self):
        second_support = User.objects.create_user(
            username="incident_second_support",
            password="TestPass123!",
            role="support",
            department=self.facilities,
        )

        second_ticket = Ticket.objects.create(
            reporter=self.employee,
            division="employee",
            title="AC not working on Floor 2",
            description="The second floor AC has stopped cooling.",
            department=self.facilities,
            assigned_to=second_support,
            status="in_progress",
        )

        self.ticket.assigned_to = self.support
        self.ticket.status = "in_progress"
        self.ticket.save()

        incident = create_incident(
            user=self.support,
            title="Floor 2 AC failure",
            description="Multiple employees reported the same AC issue.",
            ticket=self.ticket,
        )

        link_ticket_to_incident(
            user=second_support,
            incident=incident,
            ticket=second_ticket,
        )

        self.ticket.refresh_from_db()
        second_ticket.refresh_from_db()
        incident.refresh_from_db()

        self.assertEqual(incident.owner, self.support)
        self.assertEqual(incident.tickets.count(), 2)

        self.assertEqual(self.ticket.assigned_to, self.support)
        self.assertEqual(second_ticket.assigned_to, second_support)

        self.assertEqual(self.ticket.status, "in_progress")
        self.assertEqual(second_ticket.status, "in_progress")

    
    def test_cannot_link_ticket_from_another_department(self):
        incident = create_incident(
            user=self.support,
            title="Floor 2 AC failure",
            description="Shared AC issue.",
            ticket=self.ticket,
        )

        other_ticket = Ticket.objects.create(
            reporter=self.employee,
            division="employee",
            title="IT network issue",
            description="Office network is unavailable.",
            department=self.it,
        )

        with self.assertRaises(ValidationError):
            link_ticket_to_incident(
                user=self.support,
                incident=incident,
                ticket=other_ticket,
            )

        self.assertEqual(incident.tickets.count(), 1)

    def test_cannot_link_ticket_to_two_incidents(self):
        second_ticket = Ticket.objects.create(
            reporter=self.employee,
            division="employee",
            title="Another AC complaint",
            description="AC is not cooling.",
            department=self.facilities,
        )

        first_incident = create_incident(
            user=self.support,
            title="First AC incident",
            description="First shared issue.",
            ticket=self.ticket,
        )

        second_incident = create_incident(
            user=self.support,
            title="Second AC incident",
            description="Another shared issue.",
            ticket=second_ticket,
        )

        with self.assertRaises(ValidationError):
            link_ticket_to_incident(
                user=self.support,
                incident=second_incident,
                ticket=self.ticket,
            )

        self.assertEqual(self.ticket.incidents.count(), 1)
        self.assertTrue(
            first_incident.tickets.filter(pk=self.ticket.pk).exists()
        )

    def test_employee_cannot_link_ticket_to_incident(self):
        incident = create_incident(
            user=self.support,
            title="Floor 2 AC failure",
            description="Shared AC issue.",
            ticket=self.ticket,
        )

        second_ticket = Ticket.objects.create(
            reporter=self.employee,
            division="employee",
            title="Another AC complaint",
            description="AC not working.",
            department=self.facilities,
        )

        with self.assertRaises(ValidationError):
            link_ticket_to_incident(
                user=self.employee,
                incident=incident,
                ticket=second_ticket,
            )

        self.assertEqual(incident.tickets.count(), 1)

    def test_other_department_support_cannot_link_ticket(self):
        incident = create_incident(
            user=self.support,
            title="Floor 2 AC failure",
            description="Shared AC issue.",
            ticket=self.ticket,
        )

        second_ticket = Ticket.objects.create(
            reporter=self.employee,
            division="employee",
            title="Another AC complaint",
            description="AC not working.",
            department=self.facilities,
        )

        with self.assertRaises(ValidationError):
            link_ticket_to_incident(
                user=self.other_support,
                incident=incident,
                ticket=second_ticket,
            )

        self.assertEqual(incident.tickets.count(), 1)

#       
    
    def test_database_prevents_ticket_in_two_incidents(self):
        from django.db import IntegrityError, transaction
        from tickets.models import IncidentTicket

        first = create_incident(
            user=self.support,
            title="First incident",
            description="First shared issue",
            ticket=self.ticket,
        )

        second = Incident.objects.create(
            title="Second incident",
            description="Another shared issue",
            department=self.facilities,
            owner=self.support,
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                IncidentTicket.objects.create(
                    incident=second,
                    ticket=self.ticket,
                )

        self.assertEqual(
            IncidentTicket.objects.filter(
                ticket=self.ticket
            ).count(),
            1,
        )
