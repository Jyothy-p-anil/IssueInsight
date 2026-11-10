
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Department, Category, Ticket, Product
from .forms import CustomerComplaintForm

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
