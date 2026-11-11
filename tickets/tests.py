
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .forms import CustomerComplaintForm

from .models import Department, Category, Ticket, Product, TicketMessage

User = get_user_model()


from .services.category_suggestions import get_suggestion_candidates



from datetime import datetime, timedelta, timezone as dt_timezone
from django.utils import timezone

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


class CategoryManagementTests(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.admin = User.objects.create_user(
            username='category_admin',
            password='TestPass123!',
            role='admin'
        )

        cls.employee = User.objects.create_user(
            username='category_employee',
            password='TestPass123!',
            role='employee'
        )

        cls.facilities = Department.objects.create(
            name='Facilities Support'
        )

        cls.product_support = Department.objects.create(
            name='Product Support'
        )

    def test_only_admin_can_manage_categories(self):

        url = reverse('manage_categories')

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

    def test_admin_can_create_category(self):

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse('manage_categories'),
            {
                'name': 'Printer Issues',
                'division': 'employee',
                'department': self.facilities.pk,
            }
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Category.objects.filter(
                name='Printer Issues',
                division='employee',
                department=self.facilities
            ).exists()
        )

    def test_duplicate_category_rejected(self):

        Category.objects.create(
            name='IT Issues',
            division='employee',
            department=self.facilities
        )

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse('manage_categories'),
            {
                'name': 'it issues',
                'division': 'employee',
                'department': self.facilities.pk,
            }
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            Category.objects.filter(
                division='employee',
                name__iexact='IT Issues'
            ).count(),
            1
        )

        self.assertTrue(response.context['form'].errors)

    def test_same_name_allowed_for_different_divisions(self):

        Category.objects.create(
            name='Connection Issues',
            division='employee',
            department=self.facilities
        )

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse('manage_categories'),
            {
                'name': 'Connection Issues',
                'division': 'customer',
                'department': self.product_support.pk,
            }
        )

        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            Category.objects.filter(
                name='Connection Issues'
            ).count(),
            2
        )

    def test_other_category_has_manual_routing(self):

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse('manage_categories'),
            {
                'name': 'Other',
                'division': 'employee',
                'department': '',
            }
        )

        self.assertEqual(response.status_code, 302)

        category = Category.objects.get(
            name='Other',
            division='employee'
        )

        self.assertIsNone(category.department)

    def test_normal_category_requires_department(self):

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse('manage_categories'),
            {
                'name': 'Printer Issues',
                'division': 'employee',
                'department': '',
            }
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            Category.objects.filter(
                name='Printer Issues'
            ).exists()
        )

    def test_other_cannot_have_department(self):

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse('manage_categories'),
            {
                'name': 'Other',
                'division': 'customer',
                'department': self.product_support.pk,
            }
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            Category.objects.filter(
                name='Other',
                division='customer'
            ).exists()
        )



    def test_admin_can_edit_category(self):

        category = Category.objects.create(
            name='Printer Issues',
            division='employee',
            department=self.facilities
        )

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse('edit_category', args=[category.pk]),
            {
                'name': 'Office Printer Issues',
                'division': 'employee',
                'department': self.product_support.pk,
            }
        )

        self.assertEqual(response.status_code, 302)

        category.refresh_from_db()

        self.assertEqual(
            category.name,
            'Office Printer Issues'
        )
        self.assertEqual(
            category.department,
            self.product_support
        )

    def test_edit_rejects_duplicate_category(self):

        Category.objects.create(
            name='IT Issues',
            division='employee',
            department=self.facilities
        )

        category = Category.objects.create(
            name='Printer Issues',
            division='employee',
            department=self.facilities
        )

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse('edit_category', args=[category.pk]),
            {
                'name': 'it issues',
                'division': 'employee',
                'department': self.facilities.pk,
            }
        )

        self.assertEqual(response.status_code, 200)

        category.refresh_from_db()
        self.assertEqual(category.name, 'Printer Issues')

    def test_used_category_cannot_change_division(self):

        category = Category.objects.create(
            name='Printer Issues',
            division='employee',
            department=self.facilities
        )

        Ticket.objects.create(
            reporter=self.employee,
            division='employee',
            title='Printer not working',
            description='Office printer issue.',
            category=category,
            department=self.facilities
        )

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse('edit_category', args=[category.pk]),
            {
                'name': 'Printer Issues',
                'division': 'customer',
                'department': self.product_support.pk,
            }
        )

        self.assertEqual(response.status_code, 200)

        category.refresh_from_db()
        self.assertEqual(category.division, 'employee')
        self.assertTrue(response.context['form'].errors)

    def test_cannot_delete_used_category(self):

        category = Category.objects.create(
            name='IT Issues',
            division='employee',
            department=self.facilities
        )

        Ticket.objects.create(
            reporter=self.employee,
            division='employee',
            title='Computer issue',
            description='Computer is not working.',
            category=category,
            department=self.facilities
        )

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse('delete_category', args=[category.pk])
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Category.objects.filter(pk=category.pk).exists()
        )

    def test_admin_can_delete_unused_category(self):

        category = Category.objects.create(
            name='Temporary Category',
            division='employee',
            department=self.facilities
        )

        category_id = category.pk

        self.client.force_login(self.admin)

        url = reverse('delete_category', args=[category_id])

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            Category.objects.filter(pk=category_id).exists()
        )

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            Category.objects.filter(pk=category_id).exists()
        )

    def test_other_category_is_protected(self):

        category = Category.objects.create(
            name='Other',
            division='employee',
            department=None
        )

        self.client.force_login(self.admin)

        edit_response = self.client.post(
            reverse('edit_category', args=[category.pk]),
            {
                'name': 'Miscellaneous',
                'division': 'customer',
                'department': self.product_support.pk,
            }
        )

        self.assertEqual(edit_response.status_code, 200)

        category.refresh_from_db()
        self.assertEqual(category.name, 'Other')
        self.assertEqual(category.division, 'employee')

        delete_response = self.client.post(
            reverse('delete_category', args=[category.pk])
        )

        self.assertEqual(delete_response.status_code, 302)

        self.assertTrue(
            Category.objects.filter(pk=category.pk).exists()
        )

    def test_employee_cannot_edit_or_delete_category(self):

        category = Category.objects.create(
            name='Protected Category',
            division='employee',
            department=self.facilities
        )

        self.client.force_login(self.employee)

        edit_response = self.client.post(
            reverse('edit_category', args=[category.pk]),
            {
                'name': 'Unauthorized Change',
                'division': 'employee',
                'department': self.facilities.pk,
            }
        )

        delete_response = self.client.post(
            reverse('delete_category', args=[category.pk])
        )

        self.assertEqual(edit_response.status_code, 302)
        self.assertEqual(delete_response.status_code, 302)

        category.refresh_from_db()
        self.assertEqual(
            category.name,
            'Protected Category'
        )


class ProductManagementTests(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.admin = User.objects.create_user(
            username='product_admin',
            password='TestPass123!',
            role='admin'
        )

        cls.employee = User.objects.create_user(
            username='product_employee',
            password='TestPass123!',
            role='employee'
        )

    def test_only_admin_can_manage_products(self):

        url = reverse('manage_products')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)

        self.client.force_login(self.employee)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        response = self.client.post(
            url,
            {'name': 'Unauthorized Product'}
        )

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            Product.objects.filter(
                name='Unauthorized Product'
            ).exists()
        )

        self.client.force_login(self.admin)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_admin_can_create_active_product(self):

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse('manage_products'),
            {'name': 'DemoFlow'}
        )

        self.assertEqual(response.status_code, 302)

        product = Product.objects.get(name='DemoFlow')

        self.assertTrue(product.is_active)

    def test_duplicate_product_rejected(self):

        Product.objects.create(name='PayrollPro')

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse('manage_products'),
            {'name': 'payrollpro'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)

        self.assertEqual(Product.objects.count(), 1)

    def test_empty_product_name_rejected(self):

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse('manage_products'),
            {'name': '   '}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Product.objects.count(), 0)

    def test_only_active_products_are_selectable(self):

        active_product = Product.objects.create(
            name='ActiveDemo',
            is_active=True
        )

        inactive_product = Product.objects.create(
            name='InactiveDemo',
            is_active=False
        )

        form = CustomerComplaintForm()

        queryset = form.fields['product'].queryset

        self.assertIn(active_product, queryset)
        self.assertNotIn(inactive_product, queryset)


class ProductUpdateTests(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.admin = User.objects.create_user(
            username='product_update_admin',
            password='TestPass123!',
            role='admin'
        )

        cls.employee = User.objects.create_user(
            username='product_update_employee',
            password='TestPass123!',
            role='employee'
        )

    def test_admin_can_edit_product_name(self):

        product = Product.objects.create(
            name='DemoFlow',
            is_active=False
        )

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse('edit_product', args=[product.pk]),
            {'name': 'DemoFlow Suite'}
        )

        self.assertEqual(response.status_code, 302)

        product.refresh_from_db()

        self.assertEqual(
            product.name,
            'DemoFlow Suite'
        )
        self.assertFalse(product.is_active)

    def test_duplicate_product_rename_rejected(self):

        Product.objects.create(name='PayrollPro')

        product = Product.objects.create(
            name='DemoFlow'
        )

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse('edit_product', args=[product.pk]),
            {'name': 'payrollpro'}
        )

        self.assertEqual(response.status_code, 200)

        product.refresh_from_db()
        self.assertEqual(product.name, 'DemoFlow')
        self.assertTrue(response.context['form'].errors)

    def test_admin_can_deactivate_and_reactivate_product(self):

        product = Product.objects.create(
            name='DemoFlow'
        )

        self.client.force_login(self.admin)

        url = reverse(
            'toggle_product_status',
            args=[product.pk]
        )

        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)

        product.refresh_from_db()
        self.assertFalse(product.is_active)

        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)

        product.refresh_from_db()
        self.assertTrue(product.is_active)

    def test_inactive_product_preserves_existing_ticket(self):

        product = Product.objects.create(
            name='LegacyProduct'
        )

        customer = User.objects.create_user(
            username='product_history_customer',
            password='TestPass123!',
            role='customer'
        )

        ticket = Ticket.objects.create(
            reporter=customer,
            division='customer',
            title='Existing software issue',
            description='Historical complaint.',
            product=product
        )

        self.client.force_login(self.admin)

        self.client.post(
            reverse(
                'toggle_product_status',
                args=[product.pk]
            )
        )

        product.refresh_from_db()
        ticket.refresh_from_db()

        self.assertFalse(product.is_active)
        self.assertEqual(ticket.product, product)

        form = CustomerComplaintForm()

        self.assertNotIn(
            product,
            form.fields['product'].queryset
        )

    def test_employee_cannot_edit_or_toggle_product(self):

        product = Product.objects.create(
            name='ProtectedProduct'
        )

        self.client.force_login(self.employee)

        edit_response = self.client.post(
            reverse('edit_product', args=[product.pk]),
            {'name': 'Unauthorized Name'}
        )

        toggle_response = self.client.post(
            reverse(
                'toggle_product_status',
                args=[product.pk]
            )
        )

        self.assertEqual(edit_response.status_code, 302)
        self.assertEqual(toggle_response.status_code, 302)

        product.refresh_from_db()

        self.assertEqual(
            product.name,
            'ProtectedProduct'
        )
        self.assertTrue(product.is_active)

    def test_status_change_requires_post(self):

        product = Product.objects.create(
            name='DemoFlow'
        )

        self.client.force_login(self.admin)

        response = self.client.get(
            reverse(
                'toggle_product_status',
                args=[product.pk]
            )
        )

        self.assertEqual(response.status_code, 405)

        product.refresh_from_db()
        self.assertTrue(product.is_active)

    def test_product_deletion_disabled_in_django_admin(self):

        from django.contrib import admin
        from .admin import ProductAdmin

        product = Product.objects.create(
            name='ProtectedHistoryProduct'
        )

        product_admin = ProductAdmin(
            Product,
            admin.site
        )

        self.assertFalse(
            product_admin.has_delete_permission(
                None,
                obj=product
            )
        )


# Step 57: Employee complaint submission tests

class EmployeeComplaintSubmissionTests(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.employee = User.objects.create_user(
            username='complaint_employee',
            password='TestPass123!',
            role='employee'
        )

        cls.other_employee = User.objects.create_user(
            username='another_employee',
            password='TestPass123!',
            role='employee'
        )

        cls.customer = User.objects.create_user(
            username='complaint_customer',
            password='TestPass123!',
            role='customer'
        )

        cls.department = Department.objects.create(
            name='Facilities Support'
        )

        cls.employee_category = Category.objects.create(
            name='Facilities Issues',
            division='employee',
            department=cls.department
        )

        cls.other_category = Category.objects.create(
            name='Other',
            division='employee',
            department=None
        )

        cls.customer_category = Category.objects.create(
            name='Login & Access',
            division='customer',
            department=cls.department
        )

    def complaint_data(self, **overrides):

        data = {
            'title': 'Office AC not working',
            'description': 'The AC is not cooling.',
            'floor': 'Floor 2',
            'category': self.employee_category.pk,
        }

        data.update(overrides)
        return data

    def test_guest_cannot_submit_complaint(self):

        url = reverse('submit_employee_complaint')

        get_response = self.client.get(url)

        post_response = self.client.post(
            url,
            self.complaint_data()
        )

        self.assertEqual(get_response.status_code, 302)
        self.assertEqual(post_response.status_code, 302)
        self.assertEqual(Ticket.objects.count(), 0)

    def test_customer_cannot_submit_employee_complaint(self):

        self.client.force_login(self.customer)

        response = self.client.post(
            reverse('submit_employee_complaint'),
            self.complaint_data()
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Ticket.objects.count(), 0)

    def test_form_shows_only_employee_categories(self):

        self.client.force_login(self.employee)

        response = self.client.get(
            reverse('submit_employee_complaint')
        )

        self.assertEqual(response.status_code, 200)

        categories = (
            response.context['form']
            .fields['category']
            .queryset
        )

        self.assertIn(self.employee_category, categories)
        self.assertIn(self.other_category, categories)
        self.assertNotIn(self.customer_category, categories)

    def test_submission_uses_server_controlled_fields(self):

        self.client.force_login(self.employee)

        data = self.complaint_data(
            reporter=self.other_employee.pk,
            division='customer',
            status='closed',
            department=99999,
            assigned_to=self.customer.pk
        )

        response = self.client.post(
            reverse('submit_employee_complaint'),
            data
        )

        self.assertRedirects(
            response,
            reverse('employee_my_tickets'),
            fetch_redirect_response=False
        )

        ticket = Ticket.objects.get()

        self.assertEqual(ticket.reporter, self.employee)
        self.assertEqual(ticket.division, 'employee')
        self.assertEqual(ticket.status, 'submitted')
        self.assertEqual(
            ticket.department,
            self.department
        )
        self.assertEqual(
            ticket.category,
            self.employee_category
        )
        self.assertEqual(ticket.floor, 'Floor 2')
        self.assertIsNone(ticket.assigned_to)

    def test_other_category_requires_manual_routing(self):

        self.client.force_login(self.employee)

        response = self.client.post(
            reverse('submit_employee_complaint'),
            self.complaint_data(
                category=self.other_category.pk
            )
        )

        self.assertEqual(response.status_code, 302)

        ticket = Ticket.objects.get()

        self.assertEqual(ticket.category, self.other_category)
        self.assertIsNone(ticket.department)
        self.assertEqual(ticket.status, 'submitted')

    def test_customer_category_is_rejected(self):

        self.client.force_login(self.employee)

        response = self.client.post(
            reverse('submit_employee_complaint'),
            self.complaint_data(
                category=self.customer_category.pk
            )
        )

        self.assertEqual(response.status_code, 200)

        self.assertIn(
            'category',
            response.context['form'].errors
        )

        self.assertEqual(Ticket.objects.count(), 0)

    def test_required_fields_are_validated(self):

        self.client.force_login(self.employee)

        for field_name in (
            'title',
            'description',
            'category'
        ):

            with self.subTest(field=field_name):

                response = self.client.post(
                    reverse('submit_employee_complaint'),
                    self.complaint_data(
                        **{field_name: ''}
                    )
                )

                self.assertEqual(
                    response.status_code,
                    200
                )

                self.assertIn(
                    field_name,
                    response.context['form'].errors
                )

        self.assertEqual(Ticket.objects.count(), 0)

    def test_floor_is_optional(self):

        self.client.force_login(self.employee)

        response = self.client.post(
            reverse('submit_employee_complaint'),
            self.complaint_data(floor='')
        )

        self.assertEqual(response.status_code, 302)

        ticket = Ticket.objects.get()

        self.assertEqual(ticket.floor, '')

    def test_employee_sees_only_own_complaints(self):

        own_ticket = Ticket.objects.create(
            reporter=self.employee,
            division='employee',
            title='My AC complaint',
            description='AC problem.',
            category=self.employee_category,
            department=self.department
        )

        Ticket.objects.create(
            reporter=self.other_employee,
            division='employee',
            title='Private employee complaint',
            description='Another issue.',
            category=self.employee_category,
            department=self.department
        )

        self.client.force_login(self.employee)

        response = self.client.get(
            reverse('employee_my_tickets')
        )

        self.assertEqual(response.status_code, 200)

        tickets = list(response.context['tickets'])

        self.assertEqual(tickets, [own_ticket])

        self.assertContains(
            response,
            'My AC complaint'
        )

        self.assertNotContains(
            response,
            'Private employee complaint'
        )

    def test_customer_cannot_view_employee_ticket_list(self):

        self.client.force_login(self.customer)

        response = self.client.get(
            reverse('employee_my_tickets')
        )

        self.assertEqual(response.status_code, 302)

        self.client.logout()

        guest_response = self.client.get(
            reverse('employee_my_tickets')
        )

        self.assertEqual(guest_response.status_code, 302)

    
    # Step 58: Floor/location validation

    def test_floor_extra_spaces_are_normalized(self):

        self.client.force_login(self.employee)

        response = self.client.post(
            reverse('submit_employee_complaint'),
            self.complaint_data(
                floor='  Floor    2 / West Wing  '
            )
        )

        self.assertEqual(response.status_code, 302)

        ticket = Ticket.objects.get()

        self.assertEqual(
            ticket.floor,
            'Floor 2 / West Wing'
        )

    def test_floor_exceeding_30_characters_is_rejected(self):

        self.client.force_login(self.employee)

        response = self.client.post(
            reverse('submit_employee_complaint'),
            self.complaint_data(
                floor='X' * 31
            )
        )

        self.assertEqual(response.status_code, 200)

        self.assertIn(
            'floor',
            response.context['form'].errors
        )

        self.assertEqual(Ticket.objects.count(), 0)

    def test_floor_accepts_maximum_allowed_length(self):

        self.client.force_login(self.employee)

        response = self.client.post(
            reverse('submit_employee_complaint'),
            self.complaint_data(
                floor='X' * 30
            )
        )

        self.assertEqual(response.status_code, 302)

        ticket = Ticket.objects.get()
        self.assertEqual(len(ticket.floor), 30)

    # Step 58: Invalid and unmapped categories

    def test_nonexistent_category_is_rejected(self):

        self.client.force_login(self.employee)

        response = self.client.post(
            reverse('submit_employee_complaint'),
            self.complaint_data(
                category=999999
            )
        )

        self.assertEqual(response.status_code, 200)

        self.assertIn(
            'category',
            response.context['form'].errors
        )

        self.assertEqual(Ticket.objects.count(), 0)

    def test_unmapped_category_enters_admin_routing_queue(self):

        legacy_category = Category.objects.create(
            name='Legacy Unmapped Issue',
            division='employee',
            department=None
        )

        self.client.force_login(self.employee)

        response = self.client.post(
            reverse('submit_employee_complaint'),
            self.complaint_data(
                category=legacy_category.pk
            )
        )

        self.assertEqual(response.status_code, 302)

        ticket = Ticket.objects.get()

        self.assertIsNone(ticket.department)
        self.assertEqual(ticket.status, 'submitted')

        admin_user = User.objects.create_user(
            username='routing_review_admin',
            password='TestPass123!',
            role='admin'
        )

        self.client.force_login(admin_user)

        response = self.client.get(
            reverse('admin_pending_routing')
        )

        self.assertEqual(response.status_code, 200)

        self.assertIn(
            ticket,
            list(response.context['tickets'])
        )

    # Step 58: Real workplace scenarios

    def test_shared_facilities_complaint_routes_correctly(self):

        self.client.force_login(self.employee)

        response = self.client.post(
            reverse('submit_employee_complaint'),
            self.complaint_data(
                title='Shared office AC issue',
                description='The common office AC is broken.',
                category=self.employee_category.pk
            )
        )

        self.assertEqual(response.status_code, 302)

        ticket = Ticket.objects.get()

        self.assertEqual(
            ticket.department,
            self.department
        )

        self.assertEqual(
            ticket.category.name,
            'Facilities Issues'
        )

    def test_personal_device_complaint_routes_to_it(self):

        it_department = Department.objects.create(
            name='Internal IT Support'
        )

        it_category = Category.objects.create(
            name='IT Issues',
            division='employee',
            department=it_department
        )

        self.client.force_login(self.employee)

        response = self.client.post(
            reverse('submit_employee_complaint'),
            self.complaint_data(
                title='My assigned laptop is not charging',
                description='My laptop charger is not working.',
                category=it_category.pk
            )
        )

        self.assertEqual(response.status_code, 302)

        ticket = Ticket.objects.get()

        self.assertEqual(
            ticket.department,
            it_department
        )

        self.assertEqual(ticket.category, it_category)

    # Step 58: Future category suggestion integration

    def test_suggestion_candidates_respect_division(self):

        employee_candidates = list(
            get_suggestion_candidates('employee')
        )

        customer_candidates = list(
            get_suggestion_candidates('customer')
        )

        invalid_candidates = list(
            get_suggestion_candidates('invalid')
        )

        self.assertIn(
            self.employee_category,
            employee_candidates
        )

        self.assertNotIn(
            self.customer_category,
            employee_candidates
        )

        self.assertIn(
            self.customer_category,
            customer_candidates
        )

        self.assertNotIn(
            self.employee_category,
            customer_candidates
        )

        self.assertEqual(invalid_candidates, [])


class CustomerComplaintSubmissionTests(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.customer = User.objects.create_user(
            username='module6_customer',
            password='TestPass123!',
            role='customer'
        )

        cls.employee = User.objects.create_user(
            username='module6_employee',
            password='TestPass123!',
            role='employee'
        )

        cls.department = Department.objects.create(
            name='Product Support'
        )

        cls.customer_category = Category.objects.create(
            name='Software Errors',
            division='customer',
            department=cls.department
        )

        cls.other_category = Category.objects.create(
            name='Other',
            division='customer',
            department=None
        )

        cls.employee_category = Category.objects.create(
            name='IT Issues',
            division='employee',
            department=cls.department
        )

        cls.active_product = Product.objects.create(
            name='Module6 Active App',
            is_active=True
        )

        cls.inactive_product = Product.objects.create(
            name='Module6 Retired App',
            is_active=False
        )

    def complaint_data(self, **overrides):

        data = {
            'title': 'Software login problem',
            'description': 'The application displays an error.',
            'product': self.active_product.pk,
            'other_product_name': '',
            'category': self.customer_category.pk,
        }

        data.update(overrides)
        return data

    def test_guest_cannot_submit_customer_complaint(self):

        url = reverse('submit_customer_complaint')

        self.assertEqual(self.client.get(url).status_code, 302)

        response = self.client.post(
            url,
            self.complaint_data()
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Ticket.objects.count(), 0)

    def test_employee_cannot_submit_customer_complaint(self):

        self.client.force_login(self.employee)

        response = self.client.post(
            reverse('submit_customer_complaint'),
            self.complaint_data()
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Ticket.objects.count(), 0)

    def test_form_filters_products_and_categories(self):

        self.client.force_login(self.customer)

        response = self.client.get(
            reverse('submit_customer_complaint')
        )

        self.assertEqual(response.status_code, 200)

        form = response.context['form']

        products = list(form.fields['product'].queryset)
        categories = list(form.fields['category'].queryset)

        self.assertIn(self.active_product, products)
        self.assertNotIn(self.inactive_product, products)

        self.assertIn(self.customer_category, categories)
        self.assertIn(self.other_category, categories)
        self.assertNotIn(self.employee_category, categories)

    def test_known_product_complaint_is_saved(self):

        self.client.force_login(self.customer)

        response = self.client.post(
            reverse('submit_customer_complaint'),
            self.complaint_data()
        )

        self.assertRedirects(
            response,
            reverse('customer_my_tickets'),
            fetch_redirect_response=False
        )

        ticket = Ticket.objects.get()

        self.assertEqual(ticket.reporter, self.customer)
        self.assertEqual(ticket.division, 'customer')
        self.assertEqual(ticket.product, self.active_product)
        self.assertEqual(ticket.other_product_name, '')
        self.assertEqual(ticket.category, self.customer_category)
        self.assertEqual(ticket.department, self.department)
        self.assertEqual(ticket.status, 'submitted')

    def test_unlisted_product_complaint_is_saved(self):

        self.client.force_login(self.customer)

        response = self.client.post(
            reverse('submit_customer_complaint'),
            self.complaint_data(
                product='',
                other_product_name='Custom Software'
            )
        )

        self.assertEqual(response.status_code, 302)

        ticket = Ticket.objects.get()

        self.assertIsNone(ticket.product)
        self.assertEqual(
            ticket.other_product_name,
            'Custom Software'
        )

    def test_both_product_choices_are_rejected(self):

        self.client.force_login(self.customer)

        response = self.client.post(
            reverse('submit_customer_complaint'),
            self.complaint_data(
                other_product_name='Another Product'
            )
        )

        self.assertEqual(response.status_code, 200)

        self.assertIn(
            'other_product_name',
            response.context['form'].errors
        )

        self.assertEqual(Ticket.objects.count(), 0)

    def test_missing_product_choice_is_rejected(self):

        self.client.force_login(self.customer)

        response = self.client.post(
            reverse('submit_customer_complaint'),
            self.complaint_data(
                product='',
                other_product_name=''
            )
        )

        self.assertEqual(response.status_code, 200)

        self.assertIn(
            'other_product_name',
            response.context['form'].errors
        )

        self.assertEqual(Ticket.objects.count(), 0)

    def test_required_customer_fields_are_validated(self):

        self.client.force_login(self.customer)

        for field_name in ('title', 'description', 'category'):

            with self.subTest(field=field_name):

                response = self.client.post(
                    reverse('submit_customer_complaint'),
                    self.complaint_data(
                        **{field_name: ''}
                    )
                )

                self.assertEqual(response.status_code, 200)

                self.assertIn(
                    field_name,
                    response.context['form'].errors
                )

        self.assertEqual(Ticket.objects.count(), 0)

    def test_employee_category_is_rejected(self):

        self.client.force_login(self.customer)

        response = self.client.post(
            reverse('submit_customer_complaint'),
            self.complaint_data(
                category=self.employee_category.pk
            )
        )

        self.assertEqual(response.status_code, 200)

        self.assertIn(
            'category',
            response.context['form'].errors
        )

        self.assertEqual(Ticket.objects.count(), 0)


    # Step 61: Protect server-controlled ticket fields

    def test_forged_server_fields_are_ignored(self):

        another_customer = User.objects.create_user(
            username='module6_other_customer',
            password='TestPass123!',
            role='customer'
        )

        self.client.force_login(self.customer)

        response = self.client.post(
            reverse('submit_customer_complaint'),
            self.complaint_data(
                reporter=another_customer.pk,
                division='employee',
                status='closed',
                department=999999,
                assigned_to=another_customer.pk,
                floor='Floor 20'
            )
        )

        self.assertEqual(response.status_code, 302)

        ticket = Ticket.objects.get()

        self.assertEqual(ticket.reporter, self.customer)
        self.assertEqual(ticket.division, 'customer')
        self.assertEqual(ticket.status, 'submitted')
        self.assertEqual(ticket.department, self.department)
        self.assertEqual(ticket.product, self.active_product)
        self.assertIsNone(ticket.assigned_to)
        self.assertEqual(ticket.floor, '')

    # Step 61: Reject invalid software products

    def test_inactive_product_submission_is_rejected(self):

        self.client.force_login(self.customer)

        response = self.client.post(
            reverse('submit_customer_complaint'),
            self.complaint_data(
                product=self.inactive_product.pk
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            'product',
            response.context['form'].errors
        )
        self.assertEqual(Ticket.objects.count(), 0)

    def test_nonexistent_product_id_is_rejected(self):

        self.client.force_login(self.customer)

        response = self.client.post(
            reverse('submit_customer_complaint'),
            self.complaint_data(product=999999)
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            'product',
            response.context['form'].errors
        )
        self.assertEqual(Ticket.objects.count(), 0)

    # Step 61: Invalid and unmapped categories

    def test_nonexistent_customer_category_is_rejected(self):

        self.client.force_login(self.customer)

        response = self.client.post(
            reverse('submit_customer_complaint'),
            self.complaint_data(category=999999)
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            'category',
            response.context['form'].errors
        )
        self.assertEqual(Ticket.objects.count(), 0)

    def test_customer_other_category_goes_to_admin_routing(self):

        self.client.force_login(self.customer)

        response = self.client.post(
            reverse('submit_customer_complaint'),
            self.complaint_data(
                category=self.other_category.pk
            )
        )

        self.assertEqual(response.status_code, 302)

        ticket = Ticket.objects.get()

        self.assertEqual(ticket.category, self.other_category)
        self.assertIsNone(ticket.department)
        self.assertEqual(ticket.status, 'submitted')

        admin = User.objects.create_user(
            username='module6_routing_admin',
            password='TestPass123!',
            role='admin'
        )

        self.client.force_login(admin)

        response = self.client.get(
            reverse('admin_pending_routing')
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(ticket, list(response.context['tickets']))

    def test_unmapped_customer_category_goes_to_admin_routing(self):

        unmapped_category = Category.objects.create(
            name='Legacy Customer Issue',
            division='customer',
            department=None
        )

        self.client.force_login(self.customer)

        response = self.client.post(
            reverse('submit_customer_complaint'),
            self.complaint_data(
                category=unmapped_category.pk
            )
        )

        self.assertEqual(response.status_code, 302)

        ticket = Ticket.objects.get()

        self.assertIsNone(ticket.department)
        self.assertEqual(ticket.status, 'submitted')

        admin = User.objects.create_user(
            username='module6_legacy_admin',
            password='TestPass123!',
            role='admin'
        )

        self.client.force_login(admin)

        response = self.client.get(
            reverse('admin_pending_routing')
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(ticket, list(response.context['tickets']))

    # Step 61: Submission confirmation and ticket reference

    def test_submission_confirmation_displays_ticket_reference(self):

        self.client.force_login(self.customer)

        response = self.client.post(
            reverse('submit_customer_complaint'),
            self.complaint_data(),
            follow=True
        )

        ticket = Ticket.objects.get()

        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response,
            f'Complaint #{ticket.pk} submitted successfully.'
        )

        self.assertContains(
            response,
            f'#{ticket.pk}'
        )

    # Step 61: Customer complaint privacy

    def test_customer_my_tickets_is_private(self):

        another_customer = User.objects.create_user(
            username='module6_private_customer',
            password='TestPass123!',
            role='customer'
        )

        own_ticket = Ticket.objects.create(
            reporter=self.customer,
            division='customer',
            title='My software complaint',
            description='My application has an error.',
            product=self.active_product,
            category=self.customer_category,
            department=self.department
        )

        Ticket.objects.create(
            reporter=another_customer,
            division='customer',
            title='Private other customer issue',
            description='Another customer has an error.',
            product=self.active_product,
            category=self.customer_category,
            department=self.department
        )

        self.client.force_login(self.customer)

        response = self.client.get(
            reverse('customer_my_tickets')
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context['tickets']),
            [own_ticket]
        )

        self.assertContains(response, 'My software complaint')
        self.assertNotContains(
            response,
            'Private other customer issue'
        )

    def test_customer_cannot_open_another_customer_ticket(self):

        another_customer = User.objects.create_user(
            username='module6_detail_customer',
            password='TestPass123!',
            role='customer'
        )

        ticket = Ticket.objects.create(
            reporter=another_customer,
            division='customer',
            title='Another customer complaint',
            description='Private complaint information.',
            product=self.active_product,
            category=self.customer_category,
            department=self.department
        )

        self.client.force_login(self.customer)

        response = self.client.get(
            reverse('ticket_detail', args=[ticket.pk])
        )

        self.assertEqual(response.status_code, 404)

    def test_guest_and_employee_cannot_view_customer_ticket_list(self):

        url = reverse('customer_my_tickets')

        guest_response = self.client.get(url)
        self.assertEqual(guest_response.status_code, 302)

        self.client.force_login(self.employee)

        employee_response = self.client.get(url)
        self.assertEqual(employee_response.status_code, 302)


class ReporterTicketDetailTests(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.employee = User.objects.create_user(
            username='module7_employee',
            password='TestPass123!',
            role='employee'
        )

        cls.other_employee = User.objects.create_user(
            username='module7_other_employee',
            password='TestPass123!',
            role='employee'
        )

        cls.customer = User.objects.create_user(
            username='module7_customer',
            password='TestPass123!',
            role='customer'
        )

        cls.facilities = Department.objects.create(
            name='Module7 Facilities'
        )

        cls.product_support = Department.objects.create(
            name='Module7 Product Support'
        )

        cls.facilities_category = Category.objects.create(
            name='Module7 Facilities Issues',
            division='employee',
            department=cls.facilities
        )

        cls.software_category = Category.objects.create(
            name='Module7 Software Errors',
            division='customer',
            department=cls.product_support
        )

        cls.product = Product.objects.create(
            name='Module7 PayrollPro'
        )

        cls.support = User.objects.create_user(
            username='module7_support',
            password='TestPass123!',
            role='support',
            department=cls.product_support
        )

        cls.employee_ticket = Ticket.objects.create(
            reporter=cls.employee,
            division='employee',
            title='Office AC not working',
            description='The office AC is not cooling.',
            floor='Floor 2',
            category=cls.facilities_category,
            department=cls.facilities,
            status='submitted'
        )

        cls.customer_ticket = Ticket.objects.create(
            reporter=cls.customer,
            division='customer',
            title='Payroll software error',
            description='The software displays an error.',
            product=cls.product,
            category=cls.software_category,
            department=cls.product_support,
            assigned_to=cls.support,
            status='in_progress'
        )

    def test_employee_detail_displays_workplace_information(self):

        self.client.force_login(self.employee)

        response = self.client.get(
            reverse('ticket_detail', args=[self.employee_ticket.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Office AC not working')
        self.assertContains(response, 'Floor 2')
        self.assertContains(response, 'Module7 Facilities Issues')
        self.assertContains(response, 'Module7 Facilities')
        self.assertContains(response, 'Submitted On')
        self.assertContains(response, 'The office AC is not cooling.')

    def test_customer_detail_displays_product_and_assignment(self):

        self.client.force_login(self.customer)

        response = self.client.get(
            reverse('ticket_detail', args=[self.customer_ticket.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Module7 PayrollPro')
        self.assertContains(response, 'Module7 Product Support')
        self.assertContains(response, 'module7_support')
        self.assertContains(response, 'In Progress')
        self.assertContains(response, 'Send Message')

    def test_unlisted_customer_product_is_displayed(self):

        ticket = Ticket.objects.create(
            reporter=self.customer,
            division='customer',
            title='Custom portal problem',
            description='The portal is unavailable.',
            other_product_name='Custom Client Portal',
            category=self.software_category,
            department=self.product_support
        )

        self.client.force_login(self.customer)

        response = self.client.get(
            reverse('ticket_detail', args=[ticket.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Custom Client Portal')

    def test_reporter_sees_public_messages_not_internal_notes(self):

        TicketMessage.objects.create(
            ticket=self.customer_ticket,
            author=self.support,
            body='Public support update',
            is_internal=False
        )

        TicketMessage.objects.create(
            ticket=self.customer_ticket,
            author=self.support,
            body='Private internal investigation',
            is_internal=True
        )

        self.client.force_login(self.customer)

        response = self.client.get(
            reverse('ticket_detail', args=[self.customer_ticket.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Public support update')
        self.assertNotContains(
            response,
            'Private internal investigation'
        )

    def test_other_employee_cannot_open_private_ticket(self):

        self.client.force_login(self.other_employee)

        response = self.client.get(
            reverse('ticket_detail', args=[self.employee_ticket.pk])
        )

        self.assertEqual(response.status_code, 404)

    def test_closed_ticket_does_not_show_reply_form(self):

        self.customer_ticket.status = 'closed'
        self.customer_ticket.save(update_fields=['status'])

        self.client.force_login(self.customer)

        response = self.client.get(
            reverse('ticket_detail', args=[self.customer_ticket.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'Replies are unavailable'
        )
        self.assertNotContains(response, 'Send Message')

class ReporterTicketListFilterTests(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.employee = User.objects.create_user(
            username='module7_filter_employee',
            password='TestPass123!',
            role='employee'
        )

        cls.other_employee = User.objects.create_user(
            username='module7_filter_other_employee',
            password='TestPass123!',
            role='employee'
        )

        cls.customer = User.objects.create_user(
            username='module7_filter_customer',
            password='TestPass123!',
            role='customer'
        )

        cls.other_customer = User.objects.create_user(
            username='module7_filter_other_customer',
            password='TestPass123!',
            role='customer'
        )

        cls.department = Department.objects.create(
            name='Module7 Filter Support'
        )

        cls.employee_category = Category.objects.create(
            name='Module7 Filter Facilities',
            division='employee',
            department=cls.department
        )

        cls.customer_category = Category.objects.create(
            name='Module7 Filter Software',
            division='customer',
            department=cls.department
        )

        cls.employee_submitted = Ticket.objects.create(
            reporter=cls.employee,
            division='employee',
            title='My submitted AC issue',
            description='AC needs repair.',
            category=cls.employee_category,
            department=cls.department,
            status='submitted'
        )

        cls.employee_resolved = Ticket.objects.create(
            reporter=cls.employee,
            division='employee',
            title='My resolved lighting issue',
            description='Lights have been repaired.',
            category=cls.employee_category,
            department=cls.department,
            status='resolved'
        )

        cls.customer_submitted = Ticket.objects.create(
            reporter=cls.customer,
            division='customer',
            title='My submitted software issue',
            description='Software has an error.',
            category=cls.customer_category,
            department=cls.department,
            status='submitted'
        )

        cls.customer_in_progress = Ticket.objects.create(
            reporter=cls.customer,
            division='customer',
            title='My ongoing software issue',
            description='Support is investigating.',
            category=cls.customer_category,
            department=cls.department,
            status='in_progress'
        )

        Ticket.objects.create(
            reporter=cls.other_employee,
            division='employee',
            title='Private employee resolved issue',
            description='Private workplace complaint.',
            category=cls.employee_category,
            department=cls.department,
            status='resolved'
        )

        Ticket.objects.create(
            reporter=cls.other_customer,
            division='customer',
            title='Private customer ongoing issue',
            description='Private software complaint.',
            category=cls.customer_category,
            department=cls.department,
            status='in_progress'
        )

    def test_employee_filter_returns_only_own_matching_tickets(self):

        self.client.force_login(self.employee)

        response = self.client.get(
            reverse('employee_my_tickets'),
            {'status': 'resolved'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context['tickets']),
            [self.employee_resolved]
        )
        self.assertEqual(
            response.context['selected_status'],
            'resolved'
        )
        self.assertNotContains(
            response, 'Private employee resolved issue'
        )

    def test_customer_filter_returns_only_own_matching_tickets(self):

        self.client.force_login(self.customer)

        response = self.client.get(
            reverse('customer_my_tickets'),
            {'status': 'in_progress'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context['tickets']),
            [self.customer_in_progress]
        )
        self.assertNotContains(
            response, 'Private customer ongoing issue'
        )

    def test_unfiltered_lists_show_all_own_tickets(self):

        scenarios = [
            (
                self.employee,
                'employee_my_tickets',
                {self.employee_submitted, self.employee_resolved}
            ),
            (
                self.customer,
                'customer_my_tickets',
                {self.customer_submitted, self.customer_in_progress}
            ),
        ]

        for user, url_name, expected in scenarios:
            with self.subTest(role=user.role):

                self.client.force_login(user)

                response = self.client.get(reverse(url_name))

                self.assertEqual(response.status_code, 200)
                self.assertEqual(
                    set(response.context['tickets']),
                    expected
                )

    def test_invalid_status_filter_defaults_to_all(self):

        for user, url_name in (
            (self.employee, 'employee_my_tickets'),
            (self.customer, 'customer_my_tickets'),
        ):
            with self.subTest(role=user.role):

                self.client.force_login(user)

                response = self.client.get(
                    reverse(url_name),
                    {'status': 'not-a-valid-status'}
                )

                self.assertEqual(response.status_code, 200)
                self.assertEqual(
                    response.context['selected_status'],
                    ''
                )
                self.assertEqual(
                    len(list(response.context['tickets'])),
                    2
                )

    def test_empty_filtered_lists_show_correct_message(self):

        for user, url_name in (
            (self.employee, 'employee_my_tickets'),
            (self.customer, 'customer_my_tickets'),
        ):
            with self.subTest(role=user.role):

                self.client.force_login(user)

                response = self.client.get(
                    reverse(url_name),
                    {'status': 'closed'}
                )

                self.assertEqual(response.status_code, 200)
                self.assertEqual(
                    list(response.context['tickets']),
                    []
                )
                self.assertContains(
                    response,
                    'No complaints found with this status.'
                )

    def test_empty_unfiltered_lists_show_original_message(self):

        new_employee = User.objects.create_user(
            username='module7_no_ticket_employee',
            password='TestPass123!',
            role='employee'
        )

        new_customer = User.objects.create_user(
            username='module7_no_ticket_customer',
            password='TestPass123!',
            role='customer'
        )

        for user, url_name, expected_message in (
            (
                new_employee,
                'employee_my_tickets',
                'You have not submitted any complaints yet.'
            ),
            (
                new_customer,
                'customer_my_tickets',
                'No complaints submitted yet.'
            ),
        ):
            with self.subTest(role=user.role):

                self.client.force_login(user)

                response = self.client.get(reverse(url_name))

                self.assertEqual(response.status_code, 200)
                self.assertContains(response, expected_message)

    def test_both_pages_display_status_filter_options(self):

        for user, url_name in (
            (self.employee, 'employee_my_tickets'),
            (self.customer, 'customer_my_tickets'),
        ):
            with self.subTest(role=user.role):

                self.client.force_login(user)

                response = self.client.get(reverse(url_name))

                self.assertEqual(response.status_code, 200)
                self.assertContains(response, 'name="status"')
                self.assertContains(response, 'All Statuses')
                self.assertContains(response, 'value="reopened"')
                self.assertContains(response, 'table-responsive')

class ReporterTicketSearchDateUpdateTests(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.employee = User.objects.create_user(
            username='module7_search_employee',
            password='TestPass123!',
            role='employee'
        )

        cls.other_employee = User.objects.create_user(
            username='module7_search_other_employee',
            password='TestPass123!',
            role='employee'
        )

        cls.customer = User.objects.create_user(
            username='module7_search_customer',
            password='TestPass123!',
            role='customer'
        )

        cls.support = User.objects.create_user(
            username='module7_search_support',
            password='TestPass123!',
            role='support'
        )

        cls.department = Department.objects.create(
            name='Module7 Search Support'
        )

        cls.support.department = cls.department
        cls.support.save(update_fields=['department'])

        cls.employee_category = Category.objects.create(
            name='Module7 Printer Issues',
            division='employee',
            department=cls.department
        )

        cls.customer_category = Category.objects.create(
            name='Module7 Report Issues',
            division='customer',
            department=cls.department
        )

        cls.employee_old = Ticket.objects.create(
            reporter=cls.employee,
            division='employee',
            title='Printer unavailable',
            description='The office printer is unavailable.',
            category=cls.employee_category,
            department=cls.department,
            status='submitted'
        )

        cls.employee_recent = Ticket.objects.create(
            reporter=cls.employee,
            division='employee',
            title='Laptop freezing',
            description='The assigned laptop freezes.',
            category=cls.employee_category,
            department=cls.department,
            status='in_progress'
        )

        cls.customer_old = Ticket.objects.create(
            reporter=cls.customer,
            division='customer',
            title='Invoice download fails',
            description='Invoices cannot be downloaded.',
            category=cls.customer_category,
            department=cls.department,
            status='submitted'
        )

        cls.customer_recent = Ticket.objects.create(
            reporter=cls.customer,
            division='customer',
            title='Report export error',
            description='Exporting a report fails.',
            category=cls.customer_category,
            department=cls.department,
            status='in_progress'
        )

        cls.private_ticket = Ticket.objects.create(
            reporter=cls.other_employee,
            division='employee',
            title='Private Printer issue',
            description='This is not the first employee complaint.',
            category=cls.employee_category,
            department=cls.department,
            status='submitted'
        )

        for ticket, day in (
            (cls.employee_old, 1),
            (cls.employee_recent, 3),
            (cls.customer_old, 2),
            (cls.customer_recent, 4),
            (cls.private_ticket, 1),
        ):
            Ticket.objects.filter(pk=ticket.pk).update(
                created_at=datetime(
                    2025, 6, day, 12, 0,
                    tzinfo=dt_timezone.utc
                )
            )

    def test_employee_title_search_preserves_privacy(self):

        self.client.force_login(self.employee)

        response = self.client.get(
            reverse('employee_my_tickets'),
            {'q': 'Printer'}
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            list(response.context['tickets']),
            [self.employee_old]
        )

        self.assertNotContains(
            response,
            'Private Printer issue'
        )

    def test_customer_can_search_by_ticket_reference(self):

        self.client.force_login(self.customer)

        response = self.client.get(
            reverse('customer_my_tickets'),
            {'q': f'#{self.customer_recent.pk}'}
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            list(response.context['tickets']),
            [self.customer_recent]
        )

    def test_date_filter_is_inclusive(self):

        self.client.force_login(self.customer)

        response = self.client.get(
            reverse('customer_my_tickets'),
            {
                'date_from': '2025-06-02',
                'date_to': '2025-06-02'
            }
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            list(response.context['tickets']),
            [self.customer_old]
        )

    def test_search_status_and_date_work_together(self):

        self.client.force_login(self.employee)

        response = self.client.get(
            reverse('employee_my_tickets'),
            {
                'q': 'Printer',
                'status': 'submitted',
                'date_from': '2025-06-01',
                'date_to': '2025-06-01',
            }
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            list(response.context['tickets']),
            [self.employee_old]
        )

    def test_invalid_dates_do_not_crash_or_filter(self):

        self.client.force_login(self.employee)

        response = self.client.get(
            reverse('employee_my_tickets'),
            {
                'date_from': '2025-99-99',
                'date_to': 'invalid'
            }
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            len(list(response.context['tickets'])),
            2
        )

        self.assertEqual(
            response.context['date_from'],
            ''
        )

        self.assertEqual(
            response.context['date_to'],
            ''
        )

    def test_search_no_results_has_helpful_message(self):

        self.client.force_login(self.customer)

        response = self.client.get(
            reverse('customer_my_tickets'),
            {'q': 'NonexistentComplaintXYZ'}
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            list(response.context['tickets']),
            []
        )

        self.assertContains(
            response,
            'No complaints match your search or filters.'
        )

    def test_claiming_ticket_updates_latest_timestamp(self):

        previous_update = timezone.now() - timedelta(days=1)

        Ticket.objects.filter(
            pk=self.employee_old.pk
        ).update(updated_at=previous_update)

        self.client.force_login(self.support)

        response = self.client.post(
            reverse(
                'claim_support_ticket',
                args=[self.employee_old.pk]
            )
        )

        self.assertEqual(response.status_code, 302)

        ticket = Ticket.objects.get(pk=self.employee_old.pk)

        self.assertEqual(ticket.status, 'in_progress')
        self.assertEqual(ticket.assigned_to, self.support)
        self.assertGreater(ticket.updated_at, previous_update)

    def test_public_message_updates_timestamp_and_history(self):

        previous_update = timezone.now() - timedelta(days=1)

        Ticket.objects.filter(
            pk=self.customer_old.pk
        ).update(updated_at=previous_update)

        self.client.force_login(self.customer)

        response = self.client.post(
            reverse(
                'add_reporter_message',
                args=[self.customer_old.pk]
            ),
            {'body': 'Public message for timeline'}
        )

        self.assertEqual(response.status_code, 302)

        ticket = Ticket.objects.get(pk=self.customer_old.pk)

        message = TicketMessage.objects.get(
            ticket=ticket,
            body='Public message for timeline'
        )

        self.assertEqual(
            ticket.updated_at,
            message.created_at
        )

        detail_response = self.client.get(
            reverse('ticket_detail', args=[ticket.pk])
        )

        self.assertContains(detail_response, 'Latest Update')
        self.assertContains(detail_response, 'Complaint Submitted')
        self.assertContains(
            detail_response,
            'Public message for timeline'
        )

    def test_manual_routing_updates_latest_timestamp(self):

        other_category = Category.objects.create(
            name='Other',
            division='customer',
            department=None
        )

        pending_ticket = Ticket.objects.create(
            reporter=self.customer,
            division='customer',
            title='Unmapped customer complaint',
            description='Admin routing is required.',
            category=other_category,
            status='submitted'
        )

        previous_update = timezone.now() - timedelta(days=1)

        Ticket.objects.filter(
            pk=pending_ticket.pk
        ).update(updated_at=previous_update)

        admin = User.objects.create_user(
            username='module7_search_admin',
            password='TestPass123!',
            role='admin'
        )

        self.client.force_login(admin)

        response = self.client.post(
            reverse(
                'admin_route_ticket',
                args=[pending_ticket.pk]
            ),
            {'department': self.department.pk}
        )

        self.assertEqual(response.status_code, 302)

        pending_ticket.refresh_from_db()

        self.assertEqual(
            pending_ticket.department,
            self.department
        )

        self.assertGreater(
            pending_ticket.updated_at,
            previous_update
        )

    def test_long_text_uses_responsive_layout(self):

        long_title = 'LaptopIssue' * 15
        long_description = 'DetailedProblem' * 40

        Ticket.objects.filter(
            pk=self.employee_old.pk
        ).update(
            title=long_title,
            description=long_description
        )

        self.client.force_login(self.employee)

        list_response = self.client.get(
            reverse('employee_my_tickets')
        )

        self.assertEqual(list_response.status_code, 200)
        self.assertContains(list_response, long_title)
        self.assertContains(list_response, 'table-responsive')
        self.assertContains(list_response, 'text-break')

        detail_response = self.client.get(
            reverse(
                'ticket_detail',
                args=[self.employee_old.pk]
            )
        )

        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, long_description)
        self.assertContains(detail_response, 'text-break')

    def test_both_roles_have_search_and_date_controls(self):

        for user, url_name in (
            (self.employee, 'employee_my_tickets'),
            (self.customer, 'customer_my_tickets'),
        ):
            with self.subTest(role=user.role):

                self.client.force_login(user)

                response = self.client.get(reverse(url_name))

                self.assertEqual(response.status_code, 200)

                self.assertContains(response, 'name="q"')
                self.assertContains(response, 'name="date_from"')
                self.assertContains(response, 'name="date_to"')
                self.assertContains(response, 'name="status"')



class AdminAllComplaintsTests(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.admin = User.objects.create_user(
            username='module8_admin',
            password='TestPass123!',
            role='admin'
        )

        cls.employee = User.objects.create_user(
            username='module8_employee',
            password='TestPass123!',
            role='employee'
        )

        cls.customer = User.objects.create_user(
            username='module8_customer',
            password='TestPass123!',
            role='customer'
        )

        cls.department = Department.objects.create(
            name='Module8 Product Support'
        )

        cls.support = User.objects.create_user(
            username='module8_support',
            password='TestPass123!',
            role='support',
            department=cls.department
        )

        cls.employee_category = Category.objects.create(
            name='Module8 Other',
            division='employee',
            department=None
        )

        cls.customer_category = Category.objects.create(
            name='Module8 Software Issues',
            division='customer',
            department=cls.department
        )

        cls.employee_ticket = Ticket.objects.create(
            reporter=cls.employee,
            division='employee',
            title='Module8 Office AC problem',
            description='Office air conditioning not working.',
            category=cls.employee_category,
            status='submitted'
        )

        cls.customer_ticket = Ticket.objects.create(
            reporter=cls.customer,
            division='customer',
            title='Module8 Payroll error',
            description='Software shows an error.',
            category=cls.customer_category,
            department=cls.department,
            assigned_to=cls.support,
            status='in_progress'
        )

    def test_guest_cannot_view_all_complaints(self):

        response = self.client.get(
            reverse('admin_all_complaints')
        )

        self.assertEqual(response.status_code, 302)

    def test_non_admin_roles_cannot_view_all_complaints(self):

        for user in (
            self.employee,
            self.customer,
            self.support
        ):
            with self.subTest(role=user.role):

                self.client.force_login(user)

                response = self.client.get(
                    reverse('admin_all_complaints')
                )

                self.assertEqual(response.status_code, 302)

    def test_admin_can_view_both_complaint_sources(self):

        self.client.force_login(self.admin)

        response = self.client.get(
            reverse('admin_all_complaints')
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response, 'Module8 Office AC problem'
        )

        self.assertContains(
            response, 'Module8 Payroll error'
        )

        self.assertEqual(
            set(response.context['tickets']),
            {self.employee_ticket, self.customer_ticket}
        )

    def test_admin_sees_routing_and_assignment(self):

        self.client.force_login(self.admin)

        response = self.client.get(
            reverse('admin_all_complaints')
        )

        self.assertContains(response, 'Pending routing')
        self.assertContains(response, 'Module8 Product Support')
        self.assertContains(response, 'module8_support')
        self.assertContains(response, 'In Progress')

    def test_superuser_can_view_all_complaints(self):

        superuser = User.objects.create_superuser(
            username='module8_superuser',
            password='TestPass123!'
        )

        self.client.force_login(superuser)

        response = self.client.get(
            reverse('admin_all_complaints')
        )

        self.assertEqual(response.status_code, 200)

    def test_viewing_does_not_change_complaint_data(self):

        self.client.force_login(self.admin)

        self.client.get(reverse('admin_all_complaints'))

        self.employee_ticket.refresh_from_db()
        self.customer_ticket.refresh_from_db()

        self.assertEqual(
            self.employee_ticket.status, 'submitted'
        )

        self.assertIsNone(
            self.employee_ticket.department
        )

        self.assertEqual(
            self.customer_ticket.status, 'in_progress'
        )

        self.assertEqual(
            self.customer_ticket.assigned_to, self.support
        )

    def test_empty_page_has_helpful_message(self):

        Ticket.objects.all().delete()

        self.client.force_login(self.admin)

        response = self.client.get(
            reverse('admin_all_complaints')
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response,
            'No complaints have been submitted yet.'
        )



# Step 72: Module 8 - Support queues and safe claiming

class SupportQueueAndClaimTests(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.facilities = Department.objects.create(
            name='Module8 Queue Facilities'
        )

        cls.product_support = Department.objects.create(
            name='Module8 Queue Product Support'
        )

        cls.employee = User.objects.create_user(
            username='m8_queue_employee',
            password='TestPass123!',
            role='employee'
        )

        cls.customer = User.objects.create_user(
            username='m8_queue_customer',
            password='TestPass123!',
            role='customer'
        )

        cls.admin = User.objects.create_user(
            username='m8_queue_admin',
            password='TestPass123!',
            role='admin'
        )

        cls.staff_a = User.objects.create_user(
            username='m8_queue_staff_a',
            password='TestPass123!',
            role='support',
            department=cls.facilities
        )

        cls.staff_b = User.objects.create_user(
            username='m8_queue_staff_b',
            password='TestPass123!',
            role='support',
            department=cls.facilities
        )

        cls.other_staff = User.objects.create_user(
            username='m8_queue_other_staff',
            password='TestPass123!',
            role='support',
            department=cls.product_support
        )

        cls.no_department_staff = User.objects.create_user(
            username='m8_queue_no_department',
            password='TestPass123!',
            role='support'
        )

        cls.facilities_category = Category.objects.create(
            name='Module8 Queue AC Issues',
            division='employee',
            department=cls.facilities
        )

        cls.customer_category = Category.objects.create(
            name='Module8 Queue Customer Issues',
            division='customer',
            department=cls.facilities
        )

        cls.product_category = Category.objects.create(
            name='Module8 Queue Software Issues',
            division='customer',
            department=cls.product_support
        )

        cls.submitted_ticket = Ticket.objects.create(
            reporter=cls.employee,
            division='employee',
            title='Office AC repair required',
            description='AC not cooling.',
            category=cls.facilities_category,
            department=cls.facilities,
            status='submitted'
        )

        cls.reopened_ticket = Ticket.objects.create(
            reporter=cls.customer,
            division='customer',
            title='Customer follow-up issue',
            description='An issue needs another review.',
            category=cls.customer_category,
            department=cls.facilities,
            status='reopened'
        )

        cls.assigned_a = Ticket.objects.create(
            reporter=cls.employee,
            division='employee',
            title='Assigned to staff A',
            description='Existing assigned complaint.',
            category=cls.facilities_category,
            department=cls.facilities,
            assigned_to=cls.staff_a,
            status='in_progress'
        )

        cls.assigned_b = Ticket.objects.create(
            reporter=cls.employee,
            division='employee',
            title='Assigned to staff B',
            description='Another assigned complaint.',
            category=cls.facilities_category,
            department=cls.facilities,
            assigned_to=cls.staff_b,
            status='in_progress'
        )

        cls.resolved_ticket = Ticket.objects.create(
            reporter=cls.employee,
            division='employee',
            title='Already resolved complaint',
            description='Work has finished.',
            category=cls.facilities_category,
            department=cls.facilities,
            status='resolved'
        )

        cls.other_department_ticket = Ticket.objects.create(
            reporter=cls.customer,
            division='customer',
            title='Product support complaint',
            description='Software issue.',
            category=cls.product_category,
            department=cls.product_support,
            status='submitted'
        )

        cls.unmapped_ticket = Ticket.objects.create(
            reporter=cls.employee,
            division='employee',
            title='Complaint awaiting routing',
            description='Department is not yet known.',
            category=cls.facilities_category,
            department=None,
            status='submitted'
        )

    def test_non_support_roles_cannot_access_support_lists(self):

        for url_name in (
            'support_department_queue',
            'support_assigned_tickets'
        ):
            with self.subTest(url=url_name):

                url = reverse(url_name)

                self.assertEqual(
                    self.client.get(url).status_code,
                    302
                )

                for user in (
                    self.employee,
                    self.customer,
                    self.admin
                ):
                    self.client.force_login(user)

                    response = self.client.get(url)

                    self.assertEqual(response.status_code, 302)

                    self.client.logout()

    def test_queue_contains_only_eligible_department_tickets(self):

        self.client.force_login(self.staff_a)

        response = self.client.get(
            reverse('support_department_queue')
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            set(response.context['tickets']),
            {
                self.submitted_ticket,
                self.reopened_ticket
            }
        )

        self.assertNotContains(
            response,
            'Product support complaint'
        )

        self.assertNotContains(
            response,
            'Complaint awaiting routing'
        )

    def test_assigned_list_shows_only_own_tickets(self):

        self.client.force_login(self.staff_a)

        response = self.client.get(
            reverse('support_assigned_tickets')
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            list(response.context['tickets']),
            [self.assigned_a]
        )

        self.assertNotContains(
            response,
            'Assigned to staff B'
        )

    def test_support_detail_requires_matching_department(self):

        self.client.force_login(self.staff_a)

        own_response = self.client.get(
            reverse(
                'support_ticket_detail',
                args=[self.submitted_ticket.pk]
            )
        )

        other_response = self.client.get(
            reverse(
                'support_ticket_detail',
                args=[self.other_department_ticket.pk]
            )
        )

        self.assertEqual(own_response.status_code, 200)
        self.assertEqual(other_response.status_code, 404)

    def test_claim_button_only_for_eligible_ticket(self):

        self.client.force_login(self.staff_a)

        available_response = self.client.get(
            reverse(
                'support_ticket_detail',
                args=[self.submitted_ticket.pk]
            )
        )

        assigned_response = self.client.get(
            reverse(
                'support_ticket_detail',
                args=[self.assigned_b.pk]
            )
        )

        self.assertTrue(
            available_response.context['can_claim']
        )

        self.assertFalse(
            assigned_response.context['can_claim']
        )

        self.assertFalse(
            assigned_response.context['can_reply']
        )

    def test_claim_requires_post(self):

        self.client.force_login(self.staff_a)

        response = self.client.get(
            reverse(
                'claim_support_ticket',
                args=[self.submitted_ticket.pk]
            )
        )

        self.assertEqual(response.status_code, 405)

        self.submitted_ticket.refresh_from_db()

        self.assertIsNone(
            self.submitted_ticket.assigned_to
        )

        self.assertEqual(
            self.submitted_ticket.status,
            'submitted'
        )

    def test_successful_claim_updates_owner_status_and_time(self):

        self.client.force_login(self.staff_a)

        response = self.client.post(
            reverse(
                'claim_support_ticket',
                args=[self.submitted_ticket.pk]
            )
        )

        self.assertEqual(response.status_code, 302)

        self.submitted_ticket.refresh_from_db()

        self.assertEqual(
            self.submitted_ticket.assigned_to,
            self.staff_a
        )

        self.assertEqual(
            self.submitted_ticket.status,
            'in_progress'
        )

        self.assertIsNotNone(
            self.submitted_ticket.updated_at
        )

        self.assertRedirects(
            response,
            reverse(
                'support_ticket_detail',
                args=[self.submitted_ticket.pk]
            ),
            fetch_redirect_response=False
        )

    def test_second_staff_cannot_take_claimed_ticket(self):

        url = reverse(
            'claim_support_ticket',
            args=[self.submitted_ticket.pk]
        )

        self.client.force_login(self.staff_a)
        first_response = self.client.post(url)

        self.assertEqual(first_response.status_code, 302)

        self.client.force_login(self.staff_b)
        second_response = self.client.post(url)

        self.assertEqual(second_response.status_code, 302)

        self.submitted_ticket.refresh_from_db()

        self.assertEqual(
            self.submitted_ticket.assigned_to,
            self.staff_a
        )

        self.assertEqual(
            self.submitted_ticket.status,
            'in_progress'
        )

    def test_other_department_cannot_claim_ticket(self):

        self.client.force_login(self.other_staff)

        response = self.client.post(
            reverse(
                'claim_support_ticket',
                args=[self.submitted_ticket.pk]
            )
        )

        self.assertEqual(response.status_code, 404)

        self.submitted_ticket.refresh_from_db()

        self.assertIsNone(
            self.submitted_ticket.assigned_to
        )

    def test_ineligible_ticket_cannot_be_claimed(self):

        self.client.force_login(self.staff_a)

        response = self.client.post(
            reverse(
                'claim_support_ticket',
                args=[self.resolved_ticket.pk]
            )
        )

        self.assertEqual(response.status_code, 302)

        self.resolved_ticket.refresh_from_db()

        self.assertIsNone(
            self.resolved_ticket.assigned_to
        )

        self.assertEqual(
            self.resolved_ticket.status,
            'resolved'
        )

    def test_staff_without_department_cannot_work_tickets(self):

        self.client.force_login(self.no_department_staff)

        for url_name in (
            'support_department_queue',
            'support_assigned_tickets'
        ):
            response = self.client.get(reverse(url_name))

            self.assertEqual(response.status_code, 302)

        detail_response = self.client.get(
            reverse(
                'support_ticket_detail',
                args=[self.submitted_ticket.pk]
            )
        )

        claim_response = self.client.post(
            reverse(
                'claim_support_ticket',
                args=[self.submitted_ticket.pk]
            )
        )

        self.assertEqual(detail_response.status_code, 302)
        self.assertEqual(claim_response.status_code, 302)

        self.submitted_ticket.refresh_from_db()

        self.assertIsNone(
            self.submitted_ticket.assigned_to
        )

    def test_reporter_cannot_claim_support_ticket(self):

        self.client.force_login(self.employee)

        response = self.client.post(
            reverse(
                'claim_support_ticket',
                args=[self.submitted_ticket.pk]
            )
        )

        self.assertEqual(response.status_code, 302)

        self.submitted_ticket.refresh_from_db()

        self.assertIsNone(
            self.submitted_ticket.assigned_to
        )


# Step 73: Module 8 - Admin manual routing security

class AdminManualRoutingTests(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.facilities = Department.objects.create(
            name='Module8 Routing Facilities'
        )

        cls.product_support = Department.objects.create(
            name='Module8 Routing Product Support'
        )

        cls.admin = User.objects.create_user(
            username='m8_route_admin',
            password='TestPass123!',
            role='admin'
        )

        cls.employee = User.objects.create_user(
            username='m8_route_employee',
            password='TestPass123!',
            role='employee'
        )

        cls.customer = User.objects.create_user(
            username='m8_route_customer',
            password='TestPass123!',
            role='customer'
        )

        cls.support = User.objects.create_user(
            username='m8_route_support',
            password='TestPass123!',
            role='support',
            department=cls.product_support
        )

        cls.employee_other = Category.objects.create(
            name='Other',
            division='employee',
            department=None
        )

        cls.customer_other = Category.objects.create(
            name='Other',
            division='customer',
            department=None
        )

        cls.legacy_category = Category.objects.create(
            name='Module8 Legacy Unmapped',
            division='employee',
            department=None
        )

        cls.mapped_category = Category.objects.create(
            name='Module8 Mapped Software',
            division='customer',
            department=cls.product_support
        )

        cls.employee_pending = Ticket.objects.create(
            reporter=cls.employee,
            division='employee',
            title='Unknown workplace problem',
            description='Admin must identify the team.',
            category=cls.employee_other,
            status='submitted'
        )

        cls.customer_pending = Ticket.objects.create(
            reporter=cls.customer,
            division='customer',
            title='Unknown software issue',
            description='The software is not responding.',
            other_product_name='Custom Portal',
            category=cls.customer_other,
            status='submitted'
        )

        cls.reopened_pending = Ticket.objects.create(
            reporter=cls.employee,
            division='employee',
            title='Unmapped reopened issue',
            description='Needs manual routing.',
            category=cls.legacy_category,
            status='reopened'
        )

        cls.already_routed = Ticket.objects.create(
            reporter=cls.customer,
            division='customer',
            title='Already assigned to department',
            description='Department is already known.',
            category=cls.mapped_category,
            department=cls.product_support,
            status='submitted'
        )

        cls.assigned_without_department = Ticket.objects.create(
            reporter=cls.employee,
            division='employee',
            title='Legacy assigned complaint',
            description='Existing assignment must be protected.',
            category=cls.employee_other,
            assigned_to=cls.support,
            status='submitted'
        )

        cls.resolved_pending = Ticket.objects.create(
            reporter=cls.employee,
            division='employee',
            title='Resolved legacy complaint',
            description='Not eligible for routing.',
            category=cls.legacy_category,
            status='resolved'
        )

        cls.in_progress_pending = Ticket.objects.create(
            reporter=cls.employee,
            division='employee',
            title='In progress legacy complaint',
            description='Not eligible for routing.',
            category=cls.legacy_category,
            status='in_progress'
        )

    def test_guest_cannot_access_manual_routing(self):

        list_response = self.client.get(
            reverse('admin_pending_routing')
        )

        detail_response = self.client.get(
            reverse(
                'admin_route_ticket',
                args=[self.employee_pending.pk]
            )
        )

        self.assertEqual(list_response.status_code, 302)
        self.assertEqual(detail_response.status_code, 302)

    def test_non_admin_roles_cannot_route(self):

        route_url = reverse(
            'admin_route_ticket',
            args=[self.employee_pending.pk]
        )

        for user in (
            self.employee,
            self.customer,
            self.support
        ):
            with self.subTest(role=user.role):

                self.client.force_login(user)

                self.assertEqual(
                    self.client.get(
                        reverse('admin_pending_routing')
                    ).status_code,
                    302
                )

                self.assertEqual(
                    self.client.get(route_url).status_code,
                    302
                )

                self.assertEqual(
                    self.client.post(
                        route_url,
                        {'department': self.facilities.pk}
                    ).status_code,
                    302
                )

        self.employee_pending.refresh_from_db()

        self.assertIsNone(self.employee_pending.department)

    def test_pending_list_contains_only_eligible_tickets(self):

        self.client.force_login(self.admin)

        response = self.client.get(
            reverse('admin_pending_routing')
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            set(response.context['tickets']),
            {
                self.employee_pending,
                self.customer_pending,
                self.reopened_pending
            }
        )

    def test_admin_can_review_routing_form(self):

        self.client.force_login(self.admin)

        response = self.client.get(
            reverse(
                'admin_route_ticket',
                args=[self.customer_pending.pk]
            )
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Unknown software issue')
        self.assertContains(response, 'm8_route_customer')
        self.assertContains(response, 'Custom Portal')
        self.assertContains(response, 'Assign Department')

        form = response.context['form']

        self.assertIn(
            self.facilities,
            form.fields['department'].queryset
        )

        self.assertIn(
            self.product_support,
            form.fields['department'].queryset
        )

    def test_get_request_does_not_route_ticket(self):

        self.client.force_login(self.admin)

        self.client.get(
            reverse(
                'admin_route_ticket',
                args=[self.employee_pending.pk]
            )
        )

        self.employee_pending.refresh_from_db()

        self.assertIsNone(self.employee_pending.department)
        self.assertEqual(
            self.employee_pending.status,
            'submitted'
        )

    def test_admin_routes_employee_ticket_to_department(self):

        previous_update = timezone.now() - timedelta(days=1)

        Ticket.objects.filter(
            pk=self.employee_pending.pk
        ).update(updated_at=previous_update)

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse(
                'admin_route_ticket',
                args=[self.employee_pending.pk]
            ),
            {'department': self.facilities.pk}
        )

        self.assertRedirects(
            response,
            reverse('admin_pending_routing'),
            fetch_redirect_response=False
        )

        self.employee_pending.refresh_from_db()

        self.assertEqual(
            self.employee_pending.department,
            self.facilities
        )

        self.assertEqual(
            self.employee_pending.status,
            'submitted'
        )

        self.assertIsNone(
            self.employee_pending.assigned_to
        )

        self.assertGreater(
            self.employee_pending.updated_at,
            previous_update
        )

    def test_customer_routing_enters_support_queue(self):

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse(
                'admin_route_ticket',
                args=[self.customer_pending.pk]
            ),
            {'department': self.product_support.pk}
        )

        self.assertEqual(response.status_code, 302)

        self.customer_pending.refresh_from_db()

        self.assertEqual(
            self.customer_pending.department,
            self.product_support
        )

        self.assertEqual(
            self.customer_pending.status,
            'submitted'
        )

        self.client.force_login(self.support)

        queue_response = self.client.get(
            reverse('support_department_queue')
        )

        self.assertEqual(queue_response.status_code, 200)

        self.assertIn(
            self.customer_pending,
            list(queue_response.context['tickets'])
        )

    def test_admin_can_route_eligible_reopened_ticket(self):

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse(
                'admin_route_ticket',
                args=[self.reopened_pending.pk]
            ),
            {'department': self.facilities.pk}
        )

        self.assertEqual(response.status_code, 302)

        self.reopened_pending.refresh_from_db()

        self.assertEqual(
            self.reopened_pending.department,
            self.facilities
        )

        self.assertEqual(
            self.reopened_pending.status,
            'reopened'
        )

    def test_missing_department_is_rejected(self):

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse(
                'admin_route_ticket',
                args=[self.employee_pending.pk]
            ),
            {'department': ''}
        )

        self.assertEqual(response.status_code, 200)

        self.assertIn(
            'department',
            response.context['form'].errors
        )

        self.employee_pending.refresh_from_db()

        self.assertIsNone(self.employee_pending.department)

    def test_nonexistent_department_is_rejected(self):

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse(
                'admin_route_ticket',
                args=[self.employee_pending.pk]
            ),
            {'department': 999999}
        )

        self.assertEqual(response.status_code, 200)

        self.assertIn(
            'department',
            response.context['form'].errors
        )

        self.employee_pending.refresh_from_db()

        self.assertIsNone(self.employee_pending.department)

    def test_forged_ticket_fields_are_ignored(self):

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse(
                'admin_route_ticket',
                args=[self.employee_pending.pk]
            ),
            {
                'department': self.facilities.pk,
                'reporter': self.customer.pk,
                'division': 'customer',
                'status': 'closed',
                'assigned_to': self.support.pk,
                'category': self.customer_other.pk,
            }
        )

        self.assertEqual(response.status_code, 302)

        self.employee_pending.refresh_from_db()

        self.assertEqual(
            self.employee_pending.reporter,
            self.employee
        )

        self.assertEqual(
            self.employee_pending.division,
            'employee'
        )

        self.assertEqual(
            self.employee_pending.status,
            'submitted'
        )

        self.assertEqual(
            self.employee_pending.category,
            self.employee_other
        )

        self.assertEqual(
            self.employee_pending.department,
            self.facilities
        )

        self.assertIsNone(
            self.employee_pending.assigned_to
        )

    def test_ineligible_tickets_cannot_be_routed(self):

        self.client.force_login(self.admin)

        for ticket in (
            self.already_routed,
            self.assigned_without_department,
            self.resolved_pending,
            self.in_progress_pending
        ):
            with self.subTest(ticket=ticket.pk):

                url = reverse(
                    'admin_route_ticket',
                    args=[ticket.pk]
                )

                self.assertEqual(
                    self.client.get(url).status_code,
                    404
                )

                self.assertEqual(
                    self.client.post(
                        url,
                        {'department': self.facilities.pk}
                    ).status_code,
                    404
                )

    def test_ticket_cannot_be_routed_twice(self):

        self.client.force_login(self.admin)

        url = reverse(
            'admin_route_ticket',
            args=[self.employee_pending.pk]
        )

        first_response = self.client.post(
            url,
            {'department': self.facilities.pk}
        )

        second_response = self.client.post(
            url,
            {'department': self.product_support.pk}
        )

        self.assertEqual(first_response.status_code, 302)
        self.assertEqual(second_response.status_code, 404)

        self.employee_pending.refresh_from_db()

        self.assertEqual(
            self.employee_pending.department,
            self.facilities
        )

# Step 74: Module 8 - First human acknowledgement

class FirstPublicAcknowledgementTests(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.facilities = Department.objects.create(
            name='Module8 Acknowledgement Facilities'
        )

        cls.other_department = Department.objects.create(
            name='Module8 Acknowledgement Other'
        )

        cls.employee = User.objects.create_user(
            username='m8_ack_employee',
            password='TestPass123!',
            role='employee'
        )

        cls.staff = User.objects.create_user(
            username='m8_ack_staff',
            password='TestPass123!',
            role='support',
            department=cls.facilities
        )

        cls.second_staff = User.objects.create_user(
            username='m8_ack_second_staff',
            password='TestPass123!',
            role='support',
            department=cls.facilities
        )

        cls.other_staff = User.objects.create_user(
            username='m8_ack_other_staff',
            password='TestPass123!',
            role='support',
            department=cls.other_department
        )

        cls.category = Category.objects.create(
            name='Module8 Acknowledgement AC',
            division='employee',
            department=cls.facilities
        )

        cls.ticket = Ticket.objects.create(
            reporter=cls.employee,
            division='employee',
            title='Office AC needs repair',
            description='AC is not working.',
            category=cls.category,
            department=cls.facilities,
            assigned_to=cls.staff,
            status='in_progress'
        )

        cls.unclaimed_ticket = Ticket.objects.create(
            reporter=cls.employee,
            division='employee',
            title='Unclaimed acknowledgement test',
            description='Waiting for staff.',
            category=cls.category,
            department=cls.facilities,
            status='submitted'
        )

        cls.resolved_ticket = Ticket.objects.create(
            reporter=cls.employee,
            division='employee',
            title='Resolved acknowledgement test',
            description='Already marked resolved.',
            category=cls.category,
            department=cls.facilities,
            assigned_to=cls.staff,
            status='resolved'
        )

    def support_reply(self, body, internal=False):

        return self.client.post(
            reverse(
                'add_support_message',
                args=[self.ticket.pk]
            ),
            {
                'body': body,
                'is_internal': 'on' if internal else ''
            }
        )

    def test_first_public_reply_records_acknowledgement(self):

        self.client.force_login(self.staff)

        response = self.support_reply(
            'We are investigating the AC issue.'
        )

        self.assertEqual(response.status_code, 302)

        message = TicketMessage.objects.get(
            ticket=self.ticket
        )

        self.ticket.refresh_from_db()

        self.assertFalse(message.is_internal)

        self.assertEqual(
            self.ticket.first_response_at,
            message.created_at
        )

        self.assertEqual(
            self.ticket.updated_at,
            message.created_at
        )

    def test_internal_note_does_not_acknowledge(self):

        previous_update = timezone.now() - timedelta(days=1)

        Ticket.objects.filter(
            pk=self.ticket.pk
        ).update(updated_at=previous_update)

        self.client.force_login(self.staff)

        response = self.support_reply(
            'Staff-only investigation note.',
            internal=True
        )

        self.assertEqual(response.status_code, 302)

        self.ticket.refresh_from_db()

        message = TicketMessage.objects.get(
            ticket=self.ticket
        )

        self.assertTrue(message.is_internal)
        self.assertIsNone(self.ticket.first_response_at)

        self.assertEqual(
            self.ticket.updated_at,
            previous_update
        )

    def test_internal_note_after_acknowledgement(self):

        self.client.force_login(self.staff)

        self.support_reply('First public acknowledgement.')

        self.ticket.refresh_from_db()

        first_time = self.ticket.first_response_at
        public_update = self.ticket.updated_at

        self.support_reply(
            'Internal staff investigation.',
            internal=True
        )

        self.ticket.refresh_from_db()

        self.assertEqual(
            self.ticket.first_response_at,
            first_time
        )

        self.assertEqual(
            self.ticket.updated_at,
            public_update
        )

    def test_later_public_reply_preserves_first_response(self):

        self.client.force_login(self.staff)

        self.support_reply('First public reply.')

        self.ticket.refresh_from_db()

        first_time = self.ticket.first_response_at

        self.support_reply('Second public update.')

        self.ticket.refresh_from_db()

        self.assertEqual(
            self.ticket.first_response_at,
            first_time
        )

        self.assertEqual(
            TicketMessage.objects.filter(
                ticket=self.ticket,
                is_internal=False
            ).count(),
            2
        )

    def test_reporter_reply_is_not_support_acknowledgement(self):

        self.client.force_login(self.employee)

        response = self.client.post(
            reverse(
                'add_reporter_message',
                args=[self.ticket.pk]
            ),
            {'body': 'Can you provide an update?'}
        )

        self.assertEqual(response.status_code, 302)

        self.ticket.refresh_from_db()

        self.assertIsNone(self.ticket.first_response_at)

        self.assertEqual(
            TicketMessage.objects.filter(
                ticket=self.ticket
            ).count(),
            1
        )

    def test_other_staff_in_same_department_cannot_reply(self):

        self.client.force_login(self.second_staff)

        response = self.support_reply(
            'Unauthorized acknowledgement.'
        )

        self.assertEqual(response.status_code, 404)

        self.ticket.refresh_from_db()

        self.assertIsNone(self.ticket.first_response_at)

        self.assertFalse(
            TicketMessage.objects.filter(
                ticket=self.ticket
            ).exists()
        )

    def test_other_department_cannot_acknowledge(self):

        self.client.force_login(self.other_staff)

        response = self.support_reply(
            'Wrong department acknowledgement.'
        )

        self.assertEqual(response.status_code, 404)

        self.ticket.refresh_from_db()

        self.assertIsNone(self.ticket.first_response_at)

    def test_unclaimed_and_resolved_tickets_reject_replies(self):

        self.client.force_login(self.staff)

        unclaimed_response = self.client.post(
            reverse(
                'add_support_message',
                args=[self.unclaimed_ticket.pk]
            ),
            {'body': 'Should not be accepted.'}
        )

        resolved_response = self.client.post(
            reverse(
                'add_support_message',
                args=[self.resolved_ticket.pk]
            ),
            {'body': 'Should also be rejected.'}
        )

        self.assertEqual(
            unclaimed_response.status_code,
            404
        )

        self.assertEqual(
            resolved_response.status_code,
            302
        )

        for ticket in (
            self.unclaimed_ticket,
            self.resolved_ticket
        ):
            ticket.refresh_from_db()

            self.assertIsNone(ticket.first_response_at)

            self.assertFalse(
                TicketMessage.objects.filter(
                    ticket=ticket
                ).exists()
            )

    def test_blank_reply_does_not_acknowledge(self):

        self.client.force_login(self.staff)

        response = self.support_reply('')

        self.assertEqual(response.status_code, 302)

        self.ticket.refresh_from_db()

        self.assertIsNone(self.ticket.first_response_at)

        self.assertFalse(
            TicketMessage.objects.filter(
                ticket=self.ticket
            ).exists()
        )



# Step 75: Support Staff complaint resolution

class SupportTicketResolutionTests(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.department = Department.objects.create(
            name='Resolution Test Facilities'
        )

        cls.other_department = Department.objects.create(
            name='Resolution Test IT'
        )

        cls.employee = User.objects.create_user(
            username='resolution_employee',
            password='TestPass123!',
            role='employee'
        )

        cls.staff = User.objects.create_user(
            username='resolution_staff',
            password='TestPass123!',
            role='support',
            department=cls.department
        )

        cls.other_staff = User.objects.create_user(
            username='resolution_other_staff',
            password='TestPass123!',
            role='support',
            department=cls.department
        )

        cls.wrong_department_staff = User.objects.create_user(
            username='resolution_wrong_department',
            password='TestPass123!',
            role='support',
            department=cls.other_department
        )

        cls.ticket = Ticket.objects.create(
            reporter=cls.employee,
            division='employee',
            title='Office AC not cooling',
            description='AC needs repair.',
            department=cls.department,
            assigned_to=cls.staff,
            status='in_progress'
        )

    def resolve(self, summary):
        return self.client.post(
            reverse(
                'resolve_support_ticket',
                args=[self.ticket.pk]
            ),
            {'resolution_summary': summary}
        )

    def test_assigned_staff_can_resolve(self):

        self.client.force_login(self.staff)

        response = self.resolve(
            'Faulty capacitor replaced and AC tested.'
        )

        self.assertEqual(response.status_code, 302)

        self.ticket.refresh_from_db()

        self.assertEqual(self.ticket.status, 'resolved')
        self.assertEqual(
            self.ticket.resolution_summary,
            'Faulty capacitor replaced and AC tested.'
        )
        self.assertIsNotNone(self.ticket.resolved_at)
        self.assertEqual(
            self.ticket.updated_at,
            self.ticket.resolved_at
        )

    def test_blank_summary_is_rejected(self):

        self.client.force_login(self.staff)

        for summary in ('', '   '):
            with self.subTest(summary=repr(summary)):
                self.resolve(summary)

                self.ticket.refresh_from_db()

                self.assertEqual(
                    self.ticket.status,
                    'in_progress'
                )
                self.assertEqual(
                    self.ticket.resolution_summary,
                    ''
                )
                self.assertIsNone(self.ticket.resolved_at)

    def test_other_staff_cannot_resolve(self):

        self.client.force_login(self.other_staff)

        response = self.resolve('Unauthorized resolution.')

        self.assertEqual(response.status_code, 404)

        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, 'in_progress')

    def test_wrong_department_cannot_resolve(self):

        self.client.force_login(
            self.wrong_department_staff
        )

        response = self.resolve('Wrong department.')

        self.assertEqual(response.status_code, 404)

        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, 'in_progress')

    def test_reporter_cannot_resolve(self):

        self.client.force_login(self.employee)

        response = self.resolve('Reporter resolution.')

        self.assertEqual(response.status_code, 302)

        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, 'in_progress')

    def test_duplicate_resolution_is_rejected(self):

        self.client.force_login(self.staff)

        self.resolve('AC repaired successfully.')

        self.ticket.refresh_from_db()
        original_time = self.ticket.resolved_at

        response = self.resolve('Second resolution attempt.')

        self.assertEqual(response.status_code, 404)

        self.ticket.refresh_from_db()

        self.assertEqual(self.ticket.status, 'resolved')
        self.assertEqual(
            self.ticket.resolution_summary,
            'AC repaired successfully.'
        )
        self.assertEqual(
            self.ticket.resolved_at,
            original_time
        )

    def test_reporter_can_view_resolution(self):

        self.client.force_login(self.staff)
        self.resolve('AC repaired and tested.')

        self.client.force_login(self.employee)

        response = self.client.get(
            reverse('ticket_detail', args=[self.ticket.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'AC repaired and tested.'
        )
