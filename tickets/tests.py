
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Department


User = get_user_model()


class DepartmentManagementTests(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.admin = User.objects.create_user(
            username='department_admin',
            password='TestPass123!',
            role='admin'
        )

        cls.employee = User.objects.create_user(
            username='department_employee',
            password='TestPass123!',
            role='employee'
        )

    def test_only_admin_can_access_departments(self):

        url = reverse('manage_departments')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)

        self.client.force_login(self.employee)

        response = self.client.get(url)
        self.assertRedirects(
            response,
            reverse('dashboard_redirect'),
            fetch_redirect_response=False
        )

        self.client.force_login(self.admin)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_admin_can_create_department(self):

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse('manage_departments'),
            {'name': 'Quality Assurance Support'}
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Department.objects.filter(
                name='Quality Assurance Support'
            ).exists()
        )

    def test_duplicate_department_rejected(self):

        Department.objects.create(
            name='Facilities Support'
        )

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse('manage_departments'),
            {'name': 'FACILITIES SUPPORT'}
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            Department.objects.filter(
                name__iexact='Facilities Support'
            ).count(),
            1
        )

        self.assertTrue(
            response.context['form'].errors
        )

    def test_empty_department_name_rejected(self):

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse('manage_departments'),
            {'name': '   '}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Department.objects.count(), 0)
