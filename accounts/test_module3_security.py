
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from tickets.models import (
    Department,
    Category,
    Ticket,
    TicketMessage,
)


User = get_user_model()


class Module3SecurityTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.facilities = Department.objects.create(
            name='Facilities Support'
        )
        cls.product_support = Department.objects.create(
            name='Product Support'
        )

        cls.category = Category.objects.create(
            name='Facilities Issues',
            division='employee',
            department=cls.facilities
        )

        cls.employee = User.objects.create_user(
            username='security_employee',
            password='TestPass123!',
            role='employee'
        )
        cls.other_employee = User.objects.create_user(
            username='security_other_employee',
            password='TestPass123!',
            role='employee'
        )
        cls.customer = User.objects.create_user(
            username='security_customer',
            password='TestPass123!',
            role='customer'
        )
        cls.support = User.objects.create_user(
            username='security_support',
            password='TestPass123!',
            role='support',
            department=cls.facilities
        )
        cls.second_support = User.objects.create_user(
            username='security_second_support',
            password='TestPass123!',
            role='support',
            department=cls.facilities
        )
        cls.other_department_staff = User.objects.create_user(
            username='security_product_support',
            password='TestPass123!',
            role='support',
            department=cls.product_support
        )

        cls.ticket = Ticket.objects.create(
            reporter=cls.employee,
            division='employee',
            title='Office AC issue',
            description='The air conditioner is not working.',
            category=cls.category,
            department=cls.facilities,
            assigned_to=cls.support,
            status='in_progress'
        )

        cls.pending_ticket = Ticket.objects.create(
            reporter=cls.customer,
            division='customer',
            title='Unrouted software issue',
            description='The software is not working.',
            status='submitted'
        )

    def test_unauthorized_redirect_to_dashboard(self):
        self.client.force_login(self.employee)

        response = self.client.get(
            reverse('manage_users')
        )

        self.assertRedirects(
            response,
            reverse('dashboard_redirect'),
            fetch_redirect_response=False
        )

        response = self.client.get(
            reverse('manage_users'),
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'You do not have permission'
        )

    def test_employee_cannot_spoof_identity(self):
        self.client.force_login(self.employee)

        response = self.client.post(
            reverse('submit_employee_complaint'),
            {
                'title': 'New test complaint',
                'description': 'Testing identity protection.',
                'floor': 'Floor 2',
                'category': self.category.pk,
                'reporter': self.other_employee.pk,
                'division': 'customer',
                'department': self.product_support.pk,
                'assigned_to': self.support.pk,
                'status': 'closed',
            }
        )

        self.assertEqual(response.status_code, 302)

        ticket = Ticket.objects.get(
            title='New test complaint'
        )

        self.assertEqual(ticket.reporter, self.employee)
        self.assertEqual(ticket.division, 'employee')
        self.assertEqual(ticket.department, self.facilities)
        self.assertIsNone(ticket.assigned_to)
        self.assertEqual(ticket.status, 'submitted')

    def test_employee_cannot_edit_users_or_route_tickets(self):
        self.client.force_login(self.employee)

        edit_response = self.client.post(
            reverse(
                'edit_user',
                args=[self.other_employee.pk]
            ),
            {'username': 'hacked_username'}
        )

        self.assertEqual(edit_response.status_code, 302)

        self.other_employee.refresh_from_db()
        self.assertEqual(
            self.other_employee.username,
            'security_other_employee'
        )

        route_response = self.client.post(
            reverse(
                'admin_route_ticket',
                args=[self.pending_ticket.pk]
            ),
            {'department': self.facilities.pk}
        )

        self.assertEqual(route_response.status_code, 302)

        self.pending_ticket.refresh_from_db()
        self.assertIsNone(self.pending_ticket.department)

    def test_only_assigned_staff_can_send_messages(self):
        reply_url = reverse(
            'add_support_message',
            args=[self.ticket.pk]
        )

        self.client.force_login(self.second_support)

        response = self.client.post(
            reply_url,
            {'body': 'Unauthorized internal note',
             'is_internal': 'on'}
        )
        self.assertEqual(response.status_code, 404)

        self.client.force_login(self.other_department_staff)

        response = self.client.post(
            reply_url,
            {'body': 'Wrong department'}
        )
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            TicketMessage.objects.filter(
                ticket=self.ticket
            ).count(),
            0
        )

        self.client.force_login(self.support)

        response = self.client.post(
            reply_url,
            {'body': 'Authorized internal note',
             'is_internal': 'on'}
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            TicketMessage.objects.filter(
                ticket=self.ticket,
                author=self.support,
                is_internal=True
            ).exists()
        )

    def test_internal_notes_and_ticket_privacy(self):
        TicketMessage.objects.create(
            ticket=self.ticket,
            author=self.support,
            body='Private support information',
            is_internal=True
        )

        self.client.force_login(self.employee)

        response = self.client.get(
            reverse('ticket_detail', args=[self.ticket.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(
            response,
            'Private support information'
        )

        self.client.force_login(self.other_employee)

        response = self.client.post(
            reverse(
                'add_reporter_message',
                args=[self.ticket.pk]
            ),
            {'body': 'Unauthorized message'}
        )

        self.assertEqual(response.status_code, 404)

        self.assertFalse(
            TicketMessage.objects.filter(
                body='Unauthorized message'
            ).exists()
        )
