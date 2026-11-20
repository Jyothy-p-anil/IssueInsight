
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tickets.models import Announcement

User = get_user_model()


class AnnouncementTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_user(
            username='announcement_admin',
            password='TestPass123!',
            role='admin',
        )

        cls.customer = User.objects.create_user(
            username='announcement_customer',
            password='TestPass123!',
            role='customer',
        )

        cls.published = Announcement.objects.create(
            title='Public Holiday Notice',
            content='Office closed for public holiday.',
            is_published=True,
        )

        cls.draft = Announcement.objects.create(
            title='Unpublished Draft Notice',
            content='Draft content.',
            is_published=False,
        )

    def test_anonymous_visitor_can_view_home(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)

    def test_published_announcement_visible(self):
        response = self.client.get(reverse('home'))

        self.assertContains(response, 'Public Holiday Notice')

    def test_draft_announcement_hidden(self):
        response = self.client.get(reverse('home'))

        self.assertNotContains(
            response, 'Unpublished Draft Notice'
        )

    def test_admin_can_access_management(self):
        self.client.force_login(self.admin)

        response = self.client.get(
            reverse('manage_announcements')
        )

        self.assertEqual(response.status_code, 200)

    def test_customer_cannot_access_management(self):
        self.client.force_login(self.customer)

        response = self.client.get(
            reverse('manage_announcements')
        )

        self.assertNotEqual(response.status_code, 200)

    def test_admin_can_create_announcement(self):
        self.client.force_login(self.admin)

        response = self.client.post(
            reverse('manage_announcements'),
            {
                'title': 'New Public Notice',
                'content': 'Public information.',
                'is_published': 'on',
            }
        )

        self.assertRedirects(
            response, reverse('manage_announcements')
        )

        self.assertTrue(
            Announcement.objects.filter(
                title='New Public Notice',
                is_published=True,
            ).exists()
        )

    def test_admin_can_edit_announcement(self):
        self.client.force_login(self.admin)

        response = self.client.post(
            reverse(
                'edit_announcement',
                args=[self.published.id]
            ),
            {
                'title': 'Updated Public Notice',
                'content': 'Updated information.',
                'is_published': 'on',
            }
        )

        self.assertRedirects(
            response, reverse('manage_announcements')
        )

        self.published.refresh_from_db()

        self.assertEqual(
            self.published.title,
            'Updated Public Notice'
        )

    def test_admin_can_delete_announcement(self):
        self.client.force_login(self.admin)

        response = self.client.post(
            reverse(
                'delete_announcement',
                args=[self.published.id]
            )
        )

        self.assertRedirects(
            response, reverse('manage_announcements')
        )

        self.assertFalse(
            Announcement.objects.filter(
                pk=self.published.id
            ).exists()
        )

    def test_delete_requires_post(self):
        self.client.force_login(self.admin)

        response = self.client.get(
            reverse(
                'delete_announcement',
                args=[self.published.id]
            )
        )

        self.assertEqual(response.status_code, 405)

        self.assertTrue(
            Announcement.objects.filter(
                pk=self.published.id
            ).exists()
        )
