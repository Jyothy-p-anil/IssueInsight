
from django.test import TestCase
from django.urls import reverse


class PublicContactDirectoryTests(TestCase):

    def test_contact_directory_is_public(self):
        response = self.client.get(
            reverse("public_contact_directory")
        )
        self.assertEqual(response.status_code, 200)

    def test_contact_directory_uses_correct_template(self):
        response = self.client.get(
            reverse("public_contact_directory")
        )
        self.assertTemplateUsed(
            response,
            "tickets/public_contact_directory.html",
        )

    def test_contact_directory_displays_all_sections(self):
        response = self.client.get(
            reverse("public_contact_directory")
        )

        for section in [
            "General Enquiries",
            "Product Support",
            "Facilities Support",
            "IT Support",
        ]:
            self.assertContains(response, section)
