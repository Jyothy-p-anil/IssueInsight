
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tickets.models import Department, Product, Ticket

User = get_user_model()


class RecurringProductPageTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.department = Department.objects.create(
            name='Product Support'
        )
        cls.other_department = Department.objects.create(
            name='Other Recurring Support'
        )

        cls.support = User.objects.create_user(
            username='recurring_support',
            password='TestPass123!',
            role='support',
            department=cls.department,
        )

        cls.other_support = User.objects.create_user(
            username='recurring_other_support',
            password='TestPass123!',
            role='support',
            department=cls.other_department,
        )

        cls.customer = User.objects.create_user(
            username='recurring_customer',
            password='TestPass123!',
            role='customer',
        )

        cls.no_department_support = User.objects.create_user(
            username='recurring_no_department',
            password='TestPass123!',
            role='support',
        )

        cls.product = Product.objects.create(
            name='Recurring Page Product'
        )

        cls.other_product = Product.objects.create(
            name='Other Department Product'
        )

        for number in range(2):
            Ticket.objects.create(
                reporter=cls.customer,
                division='customer',
                department=cls.department,
                product=cls.product,
                title=f'Repeated issue {number}',
                description=f'repeated_issue_{number}',
            )

            Ticket.objects.create(
                reporter=cls.customer,
                division='customer',
                department=cls.other_department,
                product=cls.other_product,
                title=f'Private issue {number}',
                description=f'private_issue_{number}',
            )

    def setUp(self):
        self.url = reverse(
            'support_recurring_product_issues'
        )

    def test_support_can_open_page(self):
        self.client.force_login(self.support)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(
            response,
            'tickets/support_recurring_product_issues.html',
        )

    def test_other_department_products_are_hidden(self):
        self.client.force_login(self.support)

        response = self.client.get(self.url)

        self.assertContains(
            response,
            'Recurring Page Product',
        )

        self.assertNotContains(
            response,
            'Other Department Product',
        )

    def test_customer_cannot_access_page(self):
        self.client.force_login(self.customer)

        response = self.client.get(
            self.url,
            follow=True,
        )

        self.assertEqual(response.status_code, 200)

        self.assertRedirects(
            response,
            reverse('customer_dashboard'),
        )

    def test_anonymous_user_redirected_to_login(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_support_without_department_redirected(self):
        self.client.force_login(self.no_department_support)

        response = self.client.get(self.url)

        self.assertRedirects(
            response,
            reverse('support_dashboard'),
        )

    @patch('tickets.views.get_recurring_issue_groups')
    def test_selected_product_runs_department_scoped_analysis(
        self, mock_groups
    ):
        mock_groups.return_value = (
            [{
                'summary': 'Repeated issue',
                'complaint_count': 2,
                'ticket_ids': [],
                'statuses': [],
            }],
            None,
        )

        self.client.force_login(self.support)

        response = self.client.get(
            self.url,
            {'product_id': self.product.pk},
        )

        self.assertEqual(response.status_code, 200)

        mock_groups.assert_called_once_with(
            product_id=self.product.pk,
            department_id=self.department.pk,
        )

        self.assertContains(
            response,
            'Repeated issue',
        )

    @patch('tickets.views.get_recurring_issue_groups')
    def test_other_department_product_cannot_be_analyzed(
        self, mock_groups
    ):
        self.client.force_login(self.support)

        response = self.client.get(
            self.url,
            {'product_id': self.other_product.pk},
        )

        self.assertEqual(response.status_code, 200)

        self.assertIsNone(
            response.context['selected_product']
        )

        mock_groups.assert_not_called()

    @patch('tickets.views.get_recurring_issue_groups')
    def test_invalid_product_id_does_not_run_analysis(
        self, mock_groups
    ):
        self.client.force_login(self.support)

        response = self.client.get(
            self.url,
            {'product_id': 'invalid'},
        )

        self.assertEqual(response.status_code, 200)

        mock_groups.assert_not_called()

    def test_other_support_department_cannot_access_page(self):
        self.client.force_login(self.other_support)

        response = self.client.get(self.url)

        self.assertRedirects(
            response,
            reverse('support_dashboard'),
        )
