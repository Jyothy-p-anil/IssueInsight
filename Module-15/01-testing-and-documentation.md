# Module 15 — Integration Testing, Final Delivery and Documentation

## Current automated tests and documentation

### Before we begin

An academic project should be explainable and verifiable, with clear boundaries between passing tests and remaining features.

### What we worked on

The test runner finds TestCase methods named test_ and checks the implemented access rules. NOTES.md records chronological development decisions.

### Picture it this way

Follow one real request or data change through the functions shown below. Notice which fields come from the user and which are set by the server.

### Important Django concepts

`test discovery`, `TestCase`, `test database`, `documentation`, `regression testing`.

### Actual code from the committed project

Source revision: [`a9a40f739d52`](https://github.com/Jyothy-p-anil/IssueInsight/commit/a9a40f739d52f68c0d05b37955d53ea1baacecf8) on `master`. The excerpts are current code, not invented historical versions.

#### `accounts/tests.py` → `RolePermissionTests`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/a9a40f739d52f68c0d05b37955d53ea1baacecf8/accounts/tests.py#L12-L273)

```python
class RolePermissionTests(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.facilities = Department.objects.create(
            name='Facilities Support'
        )

        cls.product_support = Department.objects.create(
            name='Product Support'
        )

        cls.employee = User.objects.create_user(
            username='test_employee',
            password='TestPass123!',
            role='employee'
        )

        cls.other_employee = User.objects.create_user(
            username='other_employee',
            password='TestPass123!',
            role='employee'
        )

        cls.customer = User.objects.create_user(
            username='test_customer',
            password='TestPass123!',
            role='customer'
        )

        cls.support = User.objects.create_user(
            username='test_facilities_support',
            password='TestPass123!',
            role='support',
            department=cls.facilities
        )

        cls.product_staff = User.objects.create_user(
            username='test_product_support',
            password='TestPass123!',
            role='support',
            department=cls.product_support
        )

        cls.admin = User.objects.create_user(
            username='test_app_admin',
            password='TestPass123!',
            role='admin'
        )

        cls.employee_ticket = Ticket.objects.create(
            reporter=cls.employee,
            division='employee',
            title='AC not working',
            description='Air conditioner is not cooling.',
            department=cls.facilities
        )

        cls.other_ticket = Ticket.objects.create(
            reporter=cls.other_employee,
            division='employee',
            title='Different employee complaint',
            description='Private complaint.'
        )

        cls.customer_ticket = Ticket.objects.create(
            reporter=cls.customer,
            division='customer',
            title='Software login failure',
            description='Cannot access the product.',
            department=cls.product_support
        )

    # Test 1: Employee role permissions

    def test_employee_role_permissions(self):

        self.client.force_login(self.employee)

        self.assertEqual(
            self.client.get(
                reverse('employee_dashboard')
            ).status_code,
            200
        )

        for page in (
            'customer_dashboard',
            'support_dashboard',
            'admin_dashboard',
            'manage_users',
            'admin_pending_routing',
        ):
            response = self.client.get(reverse(page))
            self.assertEqual(response.status_code, 302)

    # Test 2: Customer role permissions

    def test_customer_role_permissions(self):

        self.client.force_login(self.customer)

        self.assertEqual(
            self.client.get(
                reverse('customer_dashboard')
            ).status_code,
            200
        )

        self.assertEqual(
            self.client.get(
                reverse('submit_employee_complaint')
            ).status_code,
            302
        )

        self.assertEqual(
            self.client.get(
                reverse('manage_users')
            ).status_code,
            302
        )

    # Test 3: Ticket privacy

    def test_ticket_privacy(self):

        self.client.force_login(self.employee)

        self.assertEqual(
            self.client.get(
                reverse(
                    'ticket_detail',
                    args=[self.employee_ticket.pk]
                )
            ).status_code,
            200
        )

        for ticket in (
            self.other_ticket,
            self.customer_ticket
        ):
            response = self.client.get(
                reverse(
                    'ticket_detail',
                    args=[ticket.pk]
                )
            )
```

*Showing the first 150 of 262 lines. Open the source link for the remainder.*

#### `accounts/test_module3_security.py` → `Module3SecurityTests`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/a9a40f739d52f68c0d05b37955d53ea1baacecf8/accounts/test_module3_security.py#L17-L257)

```python
class Module3SecurityTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.facilities = Department.objects.create(
            name='Facilities Support'
        )
        cls.product_support = Department.objects.create(
            name='Product Support'
        )

        cls.category = Category.objects.create(
            name='Facilities Issues',
            division='employee',
            department=cls.facilities
        )

        cls.employee = User.objects.create_user(
            username='security_employee',
            password='TestPass123!',
            role='employee'
        )
        cls.other_employee = User.objects.create_user(
            username='security_other_employee',
            password='TestPass123!',
            role='employee'
        )
        cls.customer = User.objects.create_user(
            username='security_customer',
            password='TestPass123!',
            role='customer'
        )
        cls.support = User.objects.create_user(
            username='security_support',
            password='TestPass123!',
            role='support',
            department=cls.facilities
        )
        cls.second_support = User.objects.create_user(
            username='security_second_support',
            password='TestPass123!',
            role='support',
            department=cls.facilities
        )
        cls.other_department_staff = User.objects.create_user(
            username='security_product_support',
            password='TestPass123!',
            role='support',
            department=cls.product_support
        )

        cls.ticket = Ticket.objects.create(
            reporter=cls.employee,
            division='employee',
            title='Office AC issue',
            description='The air conditioner is not working.',
            category=cls.category,
            department=cls.facilities,
            assigned_to=cls.support,
            status='in_progress'
        )

        cls.pending_ticket = Ticket.objects.create(
            reporter=cls.customer,
            division='customer',
            title='Unrouted software issue',
            description='The software is not working.',
            status='submitted'
        )

    def test_unauthorized_redirect_to_dashboard(self):
        self.client.force_login(self.employee)

        response = self.client.get(
            reverse('manage_users')
        )

        self.assertRedirects(
            response,
            reverse('dashboard_redirect'),
            fetch_redirect_response=False
        )

        response = self.client.get(
            reverse('manage_users'),
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'You do not have permission'
        )

    def test_employee_cannot_spoof_identity(self):
        self.client.force_login(self.employee)

        response = self.client.post(
            reverse('submit_employee_complaint'),
            {
                'title': 'New test complaint',
                'description': 'Testing identity protection.',
                'floor': 'Floor 2',
                'category': self.category.pk,
                'reporter': self.other_employee.pk,
                'division': 'customer',
                'department': self.product_support.pk,
                'assigned_to': self.support.pk,
                'status': 'closed',
            }
        )

        self.assertEqual(response.status_code, 302)

        ticket = Ticket.objects.get(
            title='New test complaint'
        )

        self.assertEqual(ticket.reporter, self.employee)
        self.assertEqual(ticket.division, 'employee')
        self.assertEqual(ticket.department, self.facilities)
        self.assertIsNone(ticket.assigned_to)
        self.assertEqual(ticket.status, 'submitted')

    def test_employee_cannot_edit_users_or_route_tickets(self):
        self.client.force_login(self.employee)

        edit_response = self.client.post(
            reverse(
                'edit_user',
                args=[self.other_employee.pk]
            ),
            {'username': 'hacked_username'}
        )

        self.assertEqual(edit_response.status_code, 302)

        self.other_employee.refresh_from_db()
        self.assertEqual(
            self.other_employee.username,
            'security_other_employee'
        )

        route_response = self.client.post(
            reverse(
                'admin_route_ticket',
                args=[self.pending_ticket.pk]
            ),
            {'department': self.facilities.pk}
        )
```

*Showing the first 150 of 241 lines. Open the source link for the remainder.*

#### `tickets/tests.py`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/a9a40f739d52f68c0d05b37955d53ea1baacecf8/tickets/tests.py#L1-L2040)

```python

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Department, Category, Ticket, Product
from .forms import CustomerComplaintForm

User = get_user_model()


from .services.category_suggestions import get_suggestion_candidates

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
```

*Showing the first 150 of 2040 lines. Open the source link for the remainder.*

**Verified references in this chapter:** 3/3.

### Related development commits

- [6885ea66b8](https://github.com/Jyothy-p-anil/IssueInsight/commit/6885ea66b8d30c3d5bf80cd622269134bf4d8665) — test: complete module 3 permission verification (2026-11-08)
- [ea64b763d1](https://github.com/Jyothy-p-anil/IssueInsight/commit/ea64b763d1c0e69bc4ef3b3645cc32fc87f12549) — test: finalize module 3 permissions (2026-11-08)

*These links show historical changes. A commit may touch several modules; inspect its diff before attributing every edit to this chapter.*

### How we checked it

The source code and test definitions were inspected from Git. **This journal generator does not run Django tests** and cannot prove that every workflow works.

To test locally: `python manage.py test accounts -v 2`. Record the actual output separately.

### Explain it independently

1. What existed before this feature?
2. Which file handles the incoming request or data?
3. Which checks protect the operation?
4. How do the results reach the next page or database record?

### Teacher / interview questions

- What is the difference between having tests and executing them?
- Which end-to-end workflows still need tests?

### Connections

Back to [this module's chapter list](README.md), or view the [complete source module map](../MODULE_INDEX.md).
