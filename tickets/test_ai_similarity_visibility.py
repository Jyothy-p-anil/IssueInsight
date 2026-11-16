from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tickets.models import Ticket

User = get_user_model()


class SimilarityVisibilityTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.support = User.objects.create_user(
            username="similarity_support",
            password="TestPass123!",
            role="support",
        )

        cls.reporter = User.objects.create_user(
            username="similarity_employee",
            password="TestPass123!",
            role="employee",
        )

    def test_employee_cannot_access_support_ticket_detail(self):
        ticket = Ticket.objects.create(
            reporter=self.reporter,
            division="employee",
            title="Office AC issue",
            description="Office air conditioner is not cooling.",
        )

        self.client.force_login(self.reporter)

        response = self.client.get(
            reverse("support_ticket_detail", args=[ticket.pk])
        )

        self.assertNotEqual(response.status_code, 200)

    @patch("tickets.views.find_similar_complaints")
    def test_support_without_department_cannot_view_suggestions(
        self, mock_similarity
    ):
        ticket = Ticket.objects.create(
            reporter=self.reporter,
            division="employee",
            title="Office AC issue",
            description="Office air conditioner is not cooling.",
        )

        self.client.force_login(self.support)

        response = self.client.get(
            reverse("support_ticket_detail", args=[ticket.pk])
        )

        self.assertEqual(response.status_code, 302)
        mock_similarity.assert_not_called()