
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tickets.models import Category


User = get_user_model()


class AICategorySuggestionTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.employee = User.objects.create_user(
            username="ai_test_employee",
            password="TestPass123!",
            role="employee",
        )

        cls.customer = User.objects.create_user(
            username="ai_test_customer",
            password="TestPass123!",
            role="customer",
        )

        cls.category = Category.objects.create(
            name="Printer Issue",
            division="employee",
        )

    def setUp(self):
        self.url = reverse("suggest_ticket_category")

    def test_login_required(self):
        response = self.client.post(
            self.url,
            {"description": "My office printer is not working."},
        )
        self.assertEqual(response.status_code, 302)

    def test_get_not_allowed(self):
        self.client.force_login(self.employee)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 405)

    def test_invalid_description(self):
        self.client.force_login(self.employee)

        response = self.client.post(
            self.url,
            {"description": "AC"},
        )

        self.assertEqual(response.status_code, 400)

    @patch("tickets.views.suggest_complaint_category")
    def test_successful_employee_suggestion(self, mock_predict):
        mock_predict.return_value = (
            {
                "suggested_category": "Printer Issue",
                "similarity_score": 0.75,
                "alternatives": [],
            },
            None,
        )

        self.client.force_login(self.employee)

        response = self.client.post(
            self.url,
            {"description": "My office printer is not working."},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["category_name"],
            "Printer Issue",
        )
        self.assertEqual(
            response.json()["category_id"],
            self.category.pk,
        )
