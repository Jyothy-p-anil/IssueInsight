
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from tickets.models import Department, Ticket


User = get_user_model()


class RolePermissionTests(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.facilities = Department.objects.create(
            name='Facilities Support'
        )

        cls.product_support = Department.objects.create(
            name='Product Support'
        )

        cls.employee = User.objects.create_user(
            username='test_employee',
            password='TestPass123!',
            role='employee'
        )

        cls.other_employee = User.objects.create_user(
            username='other_employee',
            password='TestPass123!',
            role='employee'
        )

        cls.customer = User.objects.create_user(
            username='test_customer',
            password='TestPass123!',
            role='customer'
        )

        cls.support = User.objects.create_user(
            username='test_facilities_support',
            password='TestPass123!',
            role='support',
            department=cls.facilities
        )

        cls.product_staff = User.objects.create_user(
            username='test_product_support',
            password='TestPass123!',
            role='support',
            department=cls.product_support
        )

        cls.admin = User.objects.create_user(
            username='test_app_admin',
            password='TestPass123!',
            role='admin'
        )

        cls.employee_ticket = Ticket.objects.create(
            reporter=cls.employee,
            division='employee',
            title='AC not working',
            description='Air conditioner is not cooling.',
            department=cls.facilities
        )

        cls.other_ticket = Ticket.objects.create(
            reporter=cls.other_employee,
            division='employee',
            title='Different employee complaint',
            description='Private complaint.'
        )

        cls.customer_ticket = Ticket.objects.create(
            reporter=cls.customer,
            division='customer',
            title='Software login failure',
            description='Cannot access the product.',
            department=cls.product_support
        )

    # Test 1: Employee role permissions

    def test_employee_role_permissions(self):

        self.client.force_login(self.employee)

        self.assertEqual(
            self.client.get(
                reverse('employee_dashboard')
            ).status_code,
            200
        )

        for page in (
            'customer_dashboard',
            'support_dashboard',
            'admin_dashboard',
            'manage_users',
            'admin_pending_routing',
        ):
            response = self.client.get(reverse(page))
            self.assertEqual(response.status_code, 302)

    # Test 2: Customer role permissions

    def test_customer_role_permissions(self):

        self.client.force_login(self.customer)

        self.assertEqual(
            self.client.get(
                reverse('customer_dashboard')
            ).status_code,
            200
        )

        self.assertEqual(
            self.client.get(
                reverse('submit_employee_complaint')
            ).status_code,
            302
        )

        self.assertEqual(
            self.client.get(
                reverse('manage_users')
            ).status_code,
            302
        )

    # Test 3: Ticket privacy

    def test_ticket_privacy(self):

        self.client.force_login(self.employee)

        self.assertEqual(
            self.client.get(
                reverse(
                    'ticket_detail',
                    args=[self.employee_ticket.pk]
                )
            ).status_code,
            200
        )

        for ticket in (
            self.other_ticket,
            self.customer_ticket
        ):
            response = self.client.get(
                reverse(
                    'ticket_detail',
                    args=[ticket.pk]
                )
            )

            self.assertEqual(response.status_code, 404)

    # Test 4: Support Staff department isolation

    def test_support_department_isolation(self):

        self.client.force_login(self.support)

        response = self.client.get(
            reverse('support_department_queue')
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            list(response.context['tickets']),
            [self.employee_ticket]
        )

        response = self.client.get(
            reverse(
                'support_ticket_detail',
                args=[self.customer_ticket.pk]
            )
        )

        self.assertEqual(response.status_code, 404)

    # Test 5: Ticket claiming permissions

    def test_claim_permissions(self):

        claim_url = reverse(
            'claim_support_ticket',
            args=[self.employee_ticket.pk]
        )

        self.client.force_login(self.product_staff)

        self.assertEqual(
            self.client.post(claim_url).status_code,
            404
        )

        self.client.force_login(self.support)

        self.assertEqual(
            self.client.get(claim_url).status_code,
            405
        )

        self.assertEqual(
            self.client.post(claim_url).status_code,
            302
        )

        self.employee_ticket.refresh_from_db()

        self.assertEqual(
            self.employee_ticket.assigned_to,
            self.support
        )

    # Test 6: Admin-only account management

    def test_admin_only_account_changes(self):

        status_url = reverse(
            'change_user_status',
            args=[self.customer.pk]
        )

        self.client.force_login(self.employee)

        self.client.post(
            status_url,
            {'action': 'deactivate'}
        )

        self.customer.refresh_from_db()

        self.assertTrue(self.customer.is_active)

        self.client.force_login(self.admin)

        self.assertEqual(
            self.client.get(
                reverse('manage_users')
            ).status_code,
            200
        )

        self.assertEqual(
            self.client.get(status_url).status_code,
            405
        )

    # Test 7: Anonymous user access

    def test_anonymous_access(self):

        response = self.client.get(
            reverse('employee_dashboard')
        )

        self.assertEqual(response.status_code, 302)

        self.assertIn(
            'login',
            response.url
        )
