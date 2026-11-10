
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Department, Category, Ticket

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

        
    def test_admin_can_edit_department(self):

        department = Department.objects.create(
            name='Testing Department'
        )

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse('edit_department', args=[department.pk]),
            {'name': 'Updated Department'}
        )

        self.assertEqual(response.status_code, 302)

        department.refresh_from_db()
        self.assertEqual(
            department.name,
            'Updated Department'
        )

    def test_edit_rejects_duplicate_name(self):

        Department.objects.create(
            name='Internal IT Support'
        )

        department = Department.objects.create(
            name='Testing Department'
        )

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse('edit_department', args=[department.pk]),
            {'name': 'internal it support'}
        )

        self.assertEqual(response.status_code, 200)

        department.refresh_from_db()
        self.assertEqual(
            department.name,
            'Testing Department'
        )

        self.assertTrue(response.context['form'].errors)

    def test_employee_cannot_edit_or_delete_departments(self):

        department = Department.objects.create(
            name='Protected Department'
        )

        self.client.force_login(self.employee)

        edit_response = self.client.post(
            reverse('edit_department', args=[department.pk]),
            {'name': 'Unauthorized Name'}
        )

        delete_response = self.client.post(
            reverse('delete_department', args=[department.pk])
        )

        self.assertEqual(edit_response.status_code, 302)
        self.assertEqual(delete_response.status_code, 302)

        department.refresh_from_db()
        self.assertEqual(
            department.name,
            'Protected Department'
        )

    def test_cannot_delete_department_with_dependencies(self):

        staff_department = Department.objects.create(
            name='Department With Staff'
        )

        category_department = Department.objects.create(
            name='Department With Category'
        )

        ticket_department = Department.objects.create(
            name='Department With Ticket'
        )

        User.objects.create_user(
            username='linked_support_staff',
            password='TestPass123!',
            role='support',
            department=staff_department
        )

        Category.objects.create(
            name='Linked Category',
            division='employee',
            department=category_department
        )

        Ticket.objects.create(
            reporter=self.employee,
            division='employee',
            title='Linked Ticket',
            description='Test complaint.',
            department=ticket_department
        )

        self.client.force_login(self.admin)

        for department in (
            staff_department,
            category_department,
            ticket_department
        ):
            response = self.client.post(
                reverse(
                    'delete_department',
                    args=[department.pk]
                )
            )

            self.assertEqual(response.status_code, 302)

            self.assertTrue(
                Department.objects.filter(
                    pk=department.pk
                ).exists()
            )

    def test_admin_can_delete_unused_department(self):

        department = Department.objects.create(
            name='Temporary Department'
        )

        department_id = department.pk

        self.client.force_login(self.admin)

        url = reverse(
            'delete_department',
            args=[department_id]
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Department.objects.filter(
                pk=department_id
            ).exists()
        )

        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            Department.objects.filter(
                pk=department_id
            ).exists()
        )

