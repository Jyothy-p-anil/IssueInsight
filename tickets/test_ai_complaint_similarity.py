
from unittest.mock import patch

import numpy as np
from django.test import TestCase
from django.contrib.auth import get_user_model

from tickets.models import Ticket
from tickets.services.ai_complaint_similarity import (
    find_similar_complaints,
)


from tickets.models import Department

User = get_user_model()


class ComplaintSimilarityTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.reporter = User.objects.create_user(
            username="similarity_reporter",
            password="TestPass123!",
            role="employee",
        )

        cls.current = Ticket.objects.create(
            reporter=cls.reporter,
            division="employee",
            title="Current complaint",
            description="The office AC is not cooling.",
        )

        cls.similar = Ticket.objects.create(
            reporter=cls.reporter,
            division="employee",
            title="Similar complaint",
            description="The air conditioner is broken.",
        )

        cls.unrelated = Ticket.objects.create(
            reporter=cls.reporter,
            division="employee",
            title="Unrelated complaint",
            description="The office printer needs paper.",
        )

        cls.customer_ticket = Ticket.objects.create(
            reporter=cls.reporter,
            division="customer",
            title="Customer complaint",
            description="The air conditioner is broken.",
        )

    @patch(
        "tickets.services.ai_complaint_similarity."
        "generate_complaint_embedding"
    )
    def test_matching_ranking_and_division_isolation(self, mock_embedding):
        vectors = {
            self.current.description: [1.0, 0.0],
            self.similar.description: [0.9, 0.43589],
            self.unrelated.description: [0.0, 1.0],
            self.customer_ticket.description: [0.9, 0.43589],
        }

        mock_embedding.side_effect = lambda description: (
            np.array(vectors[description]),
            None,
        )

        matches, error = find_similar_complaints(
            self.current,
            min_similarity=0.60,
        )

        self.assertIsNone(error)
        self.assertEqual(len(matches), 1)
        self.assertEqual(
            matches[0]["ticket_id"],
            self.similar.pk,
        )
        self.assertGreaterEqual(
            matches[0]["similarity_score"],
            0.60,
        )

    def test_invalid_division(self):
        self.current.division = "invalid"

        matches, error = find_similar_complaints(self.current)

        self.assertIsNone(matches)
        self.assertEqual(
            error,
            "Invalid complaint division.",
        )

    @patch(
        "tickets.services.ai_complaint_similarity."
        "generate_complaint_embedding"
    )
    def test_invalid_description(self, mock_embedding):
        mock_embedding.return_value = (
            None,
            "Invalid description.",
        )

        matches, error = find_similar_complaints(self.current)

        self.assertIsNone(matches)
        self.assertEqual(error, "Invalid description.")

    @patch(
        "tickets.services.ai_complaint_similarity."
        "generate_complaint_embedding"  
)
    def test_database_similarity_retrieval(self, mock_embedding):
        vectors = {
            self.current.description: [1.0, 0.0],
            self.similar.description: [0.9, 0.43589],
            self.unrelated.description: [0.0, 1.0],
    }

        mock_embedding.side_effect = lambda description: (
        np.array(vectors[description]),
        None,
    )

        matches, error = find_similar_complaints(
        self.current,
        limit=5,
        min_similarity=0.60,    
    )

        self.assertIsNone(error)
        self.assertEqual(len(matches), 1)

        match = matches[0]

        self.assertEqual(match["ticket_id"], self.similar.pk)
        self.assertEqual(match["title"], self.similar.title)
        self.assertEqual(match["status"], self.similar.status)
        self.assertGreaterEqual(match["similarity_score"], 0.60)


    @patch(
        "tickets.services.ai_complaint_similarity."
        "generate_complaint_embedding"
    )
    def test_department_filter_excludes_other_departments(
        self, mock_embedding
    ):
        from unittest.mock import Mock

        department_a = Mock(pk=101)
        department_b = Mock(pk=102)

        vectors = {
            self.current.description: [1.0, 0.0],
            self.similar.description: [0.9, 0.43589],
            self.unrelated.description: [0.0, 1.0],
        }

        mock_embedding.side_effect = lambda description: (
            np.array(vectors[description]),
            None,
        )

        self.current.department_id = department_a.pk

        # Existing test tickets have no department assigned.
        matches, error = find_similar_complaints(
            self.current,
            department_id=department_a.pk,
        )

        self.assertIsNone(error)
        self.assertEqual(matches, [])


    @patch(
        "tickets.services.ai_complaint_similarity."
        "generate_complaint_embedding"
    )
    def test_similarity_with_real_departments(self, mock_embedding):
        from tickets.models import Department

        department_a = Department.objects.create(
            name="Similarity Facilities A"
        )
        department_b = Department.objects.create(
            name="Similarity Facilities B"
        )

        self.current.department = department_a
        self.current.save(update_fields=["department"])

        self.similar.department = department_a
        self.similar.save(update_fields=["department"])

        self.customer_ticket.department = department_b
        self.customer_ticket.save(update_fields=["department"])

        vectors = {
            self.current.description: [1.0, 0.0],
            self.similar.description: [0.9, 0.43589],
            self.unrelated.description: [0.0, 1.0],
        }

        mock_embedding.side_effect = lambda description: (
            np.array(vectors[description]),
            None,
        )

        matches, error = find_similar_complaints(
            self.current,
            department_id=department_a.pk,
            min_similarity=0.60,
        )

        self.assertIsNone(error)
        self.assertEqual(len(matches), 1)
        self.assertEqual(
            matches[0]["ticket_id"],
            self.similar.pk,
        )