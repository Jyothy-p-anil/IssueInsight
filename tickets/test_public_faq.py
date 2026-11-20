
from django.test import TestCase
from django.urls import reverse


class PublicFAQTests(TestCase):

    def test_faq_is_accessible_without_login(self):
        response = self.client.get(reverse("public_faq"))
        self.assertEqual(response.status_code, 200)

    def test_faq_uses_correct_template(self):
        response = self.client.get(reverse("public_faq"))
        self.assertTemplateUsed(
            response,
            "tickets/public_faq.html",
        )

    def test_faq_displays_all_questions(self):
        response = self.client.get(reverse("public_faq"))

        questions = [
            "What is IssueInsight?",
            "Who can submit a complaint?",
            "How can I track my complaint?",
            "Can I respond to Support Staff?",
            "What happens after my complaint is resolved?",
        ]

        for question in questions:
            self.assertContains(response, question)

    def test_faq_contains_accordion_components(self):
        response = self.client.get(reverse("public_faq"))

        self.assertContains(response, 'id="faqAccordion"')
        self.assertContains(response, 'data-bs-toggle="collapse"')
        self.assertContains(response, 'data-bs-target="#faq1"')
