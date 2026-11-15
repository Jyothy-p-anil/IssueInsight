
from django.test import SimpleTestCase

from tickets.services.ai_urgency_detection import (
    detect_complaint_urgency,
)


class AIUrgencyDetectionTests(SimpleTestCase):

    def test_high_urgency(self):
        result = detect_complaint_urgency(
            "The server is down."
        )
        self.assertEqual(result["urgency"], "high")

    def test_medium_urgency(self):
        result = detect_complaint_urgency(
            "The application keeps crashing."
        )
        self.assertEqual(result["urgency"], "medium")

    def test_low_urgency(self):
        result = detect_complaint_urgency(
            "Please install a new mouse."
        )
        self.assertEqual(result["urgency"], "low")

    def test_high_overrides_medium(self):
        result = detect_complaint_urgency(
            "The server is down and the application is crashing."
        )
        self.assertEqual(result["urgency"], "high")

    def test_case_insensitive(self):
        result = detect_complaint_urgency(
            "SECURITY BREACH detected."
        )
        self.assertEqual(result["urgency"], "high")

    def test_empty_description(self):
        result = detect_complaint_urgency("")
        self.assertEqual(result["urgency"], "low")

    def test_keyword_inside_word_not_matched(self):
        result = detect_complaint_urgency(
            "We are discussing firewall improvements."
        )
        self.assertEqual(result["urgency"], "low")
