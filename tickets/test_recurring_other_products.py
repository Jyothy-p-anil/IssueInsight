
from unittest.mock import patch

import numpy as np
from django.contrib.auth import get_user_model
from django.test import TestCase

from tickets.models import Department, Ticket
from tickets.services.recurring_product_issues import (
    get_recurring_other_product_issue_groups,
)

User = get_user_model()


class RecurringOtherProductTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.department = Department.objects.create(
            name='Other Product Support'
        )
        cls.other_department = Department.objects.create(
            name='Separate Product Support'
        )
        cls.customer = User.objects.create_user(
            username='other_product_customer',
            password='TestPass123!',
            role='customer',
        )

    def create_ticket(
        self, title, description,
        product_name='TodoApp', department=None
    ):
        return Ticket.objects.create(
            reporter=self.customer,
            division='customer',
            department=department or self.department,
            other_product_name=product_name,
            title=title,
            description=description,
        )

    @patch(
        'tickets.services.recurring_product_issues.'
        'generate_complaint_embedding'
    )
    def test_similar_other_product_complaints_grouped(
        self, mock_embedding
    ):
        self.create_ticket('Login failure', 'login_error_1')
        self.create_ticket('Cannot log in', 'login_error_2')

        mock_embedding.side_effect = [
            (np.array([1.0, 0.0]), None),
            (np.array([0.98, 0.20]) /
             np.linalg.norm([0.98, 0.20]), None),
        ]

        groups, error = get_recurring_other_product_issue_groups(
            'TodoApp',
            department_id=self.department.pk,
        )

        self.assertIsNone(error)
        self.assertEqual(len(groups), 1)
        self.assertEqual(groups[0]['complaint_count'], 2)

    @patch(
        'tickets.services.recurring_product_issues.'
        'generate_complaint_embedding'
    )
    def test_unrelated_complaints_not_grouped(
        self, mock_embedding
    ):
        self.create_ticket('Login failure', 'login_issue')
        self.create_ticket('Export failure', 'export_issue')

        mock_embedding.side_effect = [
            (np.array([1.0, 0.0]), None),
            (np.array([0.0, 1.0]), None),
        ]

        groups, error = get_recurring_other_product_issue_groups(
            'TodoApp',
            department_id=self.department.pk,
        )

        self.assertIsNone(error)
        self.assertEqual(groups, [])

    def test_different_product_excluded(self):
        self.create_ticket(
            'Login failure', 'login_issue',
            product_name='TodoApp'
        )
        self.create_ticket(
            'Login failure', 'login_issue',
            product_name='AnotherApp'
        )

        groups, error = get_recurring_other_product_issue_groups(
            'TodoApp',
            department_id=self.department.pk,
        )

        self.assertIsNone(error)
        self.assertEqual(groups, [])

    def test_other_department_excluded(self):
        self.create_ticket(
            'Login failure', 'login_issue',
            department=self.department
        )
        self.create_ticket(
            'Login failure', 'login_issue',
            department=self.other_department
        )

        groups, error = get_recurring_other_product_issue_groups(
            'TodoApp',
            department_id=self.department.pk,
        )

        self.assertIsNone(error)
        self.assertEqual(groups, [])

    def test_empty_product_name(self):
        groups, error = get_recurring_other_product_issue_groups(
            '   ',
            department_id=self.department.pk,
        )

        self.assertEqual(groups, [])
        self.assertIsNone(error)

    @patch(
        'tickets.services.recurring_product_issues.'
        'generate_complaint_embedding'
    )
    def test_embedding_error_returned(self, mock_embedding):
        self.create_ticket('Login failure', 'login_error_1')
        self.create_ticket('Login failure', 'login_error_2')

        mock_embedding.return_value = (
            None, 'Embedding unavailable'
        )

        groups, error = get_recurring_other_product_issue_groups(
            'TodoApp',
            department_id=self.department.pk,
        )

        self.assertIsNone(groups)
        self.assertEqual(error, 'Embedding unavailable')
