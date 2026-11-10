# Module 03 — Role-Based Permissions and Account Access

## Automated security tests

### Before we begin

Permission rules must be verified for wrong roles, other people's records, wrong departments and unauthenticated requests.

### What we worked on

Django TestCase creates an isolated test database. The test client acts as different users and checks response codes, redirects and database effects.

### Picture it this way

Follow one real request or data change through the functions shown below. Notice which fields come from the user and which are set by the server.

### Important Django concepts

`TestCase`, `setUpTestData`, `force_login`, `assertEqual`, `assertRedirects`, `test client`.

### Actual code from the committed project

Source revision: [`9d0620abbb2d`](https://github.com/Jyothy-p-anil/IssueInsight/commit/9d0620abbb2df25ca00a4301a4a2318325521dbe) on `master`. The excerpts are current code, not invented historical versions.

#### `accounts/tests.py` → `RolePermissionTests`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/accounts/tests.py#L12-L273)

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

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/accounts/test_module3_security.py#L17-L257)

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

**Verified references in this chapter:** 2/2.

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

- Why is testing a forbidden URL important?
- What is the difference between a 302 redirect, a 403 and a 404 response?

### Connections

Back to [this module's chapter list](README.md), or view the [complete source module map](../MODULE_INDEX.md).
