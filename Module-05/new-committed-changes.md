# Module 05 — Automatically detected new code

These additions were linked to the module by **explicit module numbers in Git commit messages**. The code below is from the currently committed project; verify its behavior rather than assuming an unfinished feature is complete.

### tickets/services/category_suggestions.py :: get_suggestion_candidates

Introduced or changed in [8ddf5a4945](https://github.com/Jyothy-p-anil/IssueInsight/commit/8ddf5a4945684003c31d54a3bc19af43a53799f3) — test(module-5): close employee submission checklist gaps.

#### `tickets/services/category_suggestions.py` → `get_suggestion_candidates`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/b5fac3135a3b92826b80454b47e933eda88b75f7/tickets/services/category_suggestions.py#L4-L17)

```python
def get_suggestion_candidates(division):
    """
    Return valid complaint categories for a division.

    Future AI classification can use these candidates.
    This function does not predict a category.
    """

    if division not in ('employee', 'customer'):
        return Category.objects.none()

    return Category.objects.filter(
        division=division
    ).order_by('name')
```

### tickets/tests.py :: EmployeeComplaintSubmissionTests

Introduced or changed in [8aa5fec6ff](https://github.com/Jyothy-p-anil/IssueInsight/commit/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a) — test(module-5): complete employee complaint submission review.

#### `tickets/tests.py` → `EmployeeComplaintSubmissionTests`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/b5fac3135a3b92826b80454b47e933eda88b75f7/tickets/tests.py#L1010-L1521)

```python
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
```

*Showing the first 150 of 512 lines. Open the source link for the remainder.*

