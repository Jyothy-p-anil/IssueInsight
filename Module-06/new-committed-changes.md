# Module 06 — Automatically detected new code

These additions were linked to the module by **explicit module numbers in Git commit messages**. The code below is from the currently committed project; verify its behavior rather than assuming an unfinished feature is complete.

### tickets/tests.py :: CustomerComplaintSubmissionTests

Introduced or changed in [e92989cc68](https://github.com/Jyothy-p-anil/IssueInsight/commit/e92989cc689bd476f15dd2dcddd18fdfe37825b8) — test(module-6): review customer complaint form and product selection.

#### `tickets/tests.py` → `CustomerComplaintSubmissionTests`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/tickets/tests.py#L1530-L2046)

```python
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
```

*Showing the first 150 of 517 lines. Open the source link for the remainder.*

