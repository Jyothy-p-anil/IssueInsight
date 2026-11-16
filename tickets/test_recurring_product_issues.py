
from unittest.mock import patch

import numpy as np
from django.contrib.auth import get_user_model
from django.test import TestCase

from tickets.models import Product, Ticket
from tickets.services.ai_embeddings import generate_complaint_embedding
from tickets.services.recurring_product_issues import (
    get_recurring_product_issues,
    get_recurring_issue_groups,
)

User = get_user_model()


class RecurringProductIssueTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.reporter = User.objects.create_user(
            username='recurring_reporter',
            password='TestPass123!',
            role='customer',
        )

        cls.product = Product.objects.create(
            name='Recurring Test Product'
        )
        cls.other_product = Product.objects.create(
            name='Unrelated Test Product'
        )

        cls.first = cls.create_ticket(
            cls.reporter,
            cls.product,
            'Reports crash',
            'reports_crash_1',
        )
        cls.second = cls.create_ticket(
            cls.reporter,
            cls.product,
            'Reports close',
            'reports_crash_2',
        )
        cls.third = cls.create_ticket(
            cls.reporter,
            cls.product,
            'Login fails',
            'login_failure',
        )
        cls.fourth = cls.create_ticket(
            cls.reporter,
            cls.product,
            'Reports freeze',
            'reports_crash_3',
        )
        cls.other = cls.create_ticket(
            cls.reporter,
            cls.other_product,
            'Reports crash elsewhere',
            'other_product_issue',
        )

    @staticmethod
    def create_ticket(reporter, product, title, description):
        return Ticket.objects.create(
            reporter=reporter,
            division='customer',
            product=product,
            title=title,
            description=description,
        )

    def mock_vectors(self):
        vectors = {
            'reports_crash_1': [1.0, 0.0],
            'reports_crash_2': [0.9, 0.43589],
            'login_failure': [0.0, 1.0],
            'reports_crash_3': [0.95, 0.31225],
            'other_product_issue': [1.0, 0.0],
        }

        def generate_mock_embedding(description):
            vector = np.array(
                vectors[description],
                dtype=float,
            )

            # Match the real embedding service:
            # return a unit-length vector.
            vector = vector / np.linalg.norm(vector)

            return vector, None

        return generate_mock_embedding

    def test_product_complaint_counts(self):
        results = get_recurring_product_issues()

        product_result = next(
            item for item in results
            if item['product_id'] == self.product.pk
        )

        self.assertEqual(
            product_result['complaint_count'],
            4,
        )

    @patch(
        'tickets.services.recurring_product_issues.'
        'generate_complaint_embedding'
    )
    def test_similar_issues_are_grouped(self, mock_embedding):
        mock_embedding.side_effect = self.mock_vectors()

        groups, error = get_recurring_issue_groups(
            self.product.pk
        )

        self.assertIsNone(error)
        self.assertEqual(len(groups), 1)
        self.assertEqual(groups[0]['complaint_count'], 3)

        self.assertEqual(
            set(groups[0]['ticket_ids']),
            {
                self.first.pk,
                self.second.pk,
                self.fourth.pk,
            },
        )

    @patch(
        'tickets.services.recurring_product_issues.'
        'generate_complaint_embedding'
    )
    def test_unrelated_issue_is_excluded(self, mock_embedding):
        mock_embedding.side_effect = self.mock_vectors()

        groups, error = get_recurring_issue_groups(
            self.product.pk
        )

        self.assertIsNone(error)
        self.assertEqual(len(groups), 1)

        self.assertNotIn(
            self.third.pk,
            groups[0]['ticket_ids'],
        )

    @patch(
        'tickets.services.recurring_product_issues.'
        'generate_complaint_embedding'
    )
    def test_other_product_is_excluded(self, mock_embedding):
        mock_embedding.side_effect = self.mock_vectors()

        groups, error = get_recurring_issue_groups(
            self.product.pk
        )

        self.assertIsNone(error)
        self.assertEqual(len(groups), 1)

        self.assertNotIn(
            self.other.pk,
            groups[0]['ticket_ids'],
        )

    @patch(
        'tickets.services.recurring_product_issues.'
        'generate_complaint_embedding'
    )
    def test_no_duplicate_group_members(self, mock_embedding):
        mock_embedding.side_effect = self.mock_vectors()

        groups, error = get_recurring_issue_groups(
            self.product.pk
        )

        self.assertIsNone(error)

        all_ids = [
            ticket_id
            for group in groups
            for ticket_id in group['ticket_ids']
        ]

        self.assertEqual(
            len(all_ids),
            len(set(all_ids)),
        )

    @patch(
        'tickets.services.recurring_product_issues.'
        'generate_complaint_embedding'
    )
    def test_higher_threshold_excludes_weaker_matches(
        self, mock_embedding
    ):
        mock_embedding.side_effect = self.mock_vectors()

        groups, error = get_recurring_issue_groups(
            self.product.pk,
            similarity_threshold=0.995,
        )

        self.assertIsNone(error)
        self.assertEqual(groups, [])

    def test_minimum_complaint_count(self):
        groups, error = get_recurring_issue_groups(
            self.other_product.pk,
            min_complaints=2,
        )

        self.assertIsNone(error)
        self.assertEqual(groups, [])

def get_recurring_other_product_issue_groups(
    product_name,
    min_complaints=2,
    similarity_threshold=0.70,
    department_id=None,
):
    """
    Group similar Customer complaints for a manually entered product.
    """

    product_name = (product_name or '').strip()

    if not product_name:
        return [], None

    tickets_query = Ticket.objects.filter(
        division='customer',
        product__isnull=True,
        other_product_name__iexact=product_name,
    )

    if department_id is not None:
        tickets_query = tickets_query.filter(
            department_id=department_id
        )

    tickets = list(
        tickets_query.order_by('created_at', 'pk')
    )

    if len(tickets) < min_complaints:
        return [], None

    vectors = []
    valid_tickets = []

    for ticket in tickets:
        vector, error = generate_complaint_embedding(
            ticket.description
        )

        if error:
            return None, error

        valid_tickets.append(ticket)
        vectors.append(vector)

    groups = []
    assigned_ids = set()

    for index, anchor in enumerate(valid_tickets):

        if anchor.pk in assigned_ids:
            continue

        members = [anchor]
        assigned_ids.add(anchor.pk)

        for other_index in range(index + 1, len(valid_tickets)):

            candidate = valid_tickets[other_index]

            if candidate.pk in assigned_ids:
                continue

            similarity = float(
                np.dot(vectors[index], vectors[other_index])
            )

            if similarity >= similarity_threshold:
                members.append(candidate)
                assigned_ids.add(candidate.pk)

        if len(members) >= min_complaints:
            groups.append({
                'summary': anchor.title,
                'complaint_count': len(members),
                'ticket_ids': [
                    ticket.pk for ticket in members
                ],
                'statuses': [
                    ticket.status for ticket in members
                ],
            })

    groups.sort(
        key=lambda group: -group['complaint_count']
    )

    return groups, None