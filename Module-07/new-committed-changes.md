# Module 07 — Automatically detected new code

These additions were linked to the module by **explicit module numbers in Git commit messages**. The code below is from the currently committed project; verify its behavior rather than assuming an unfinished feature is complete.

### templates/tickets/customer_my_tickets.html

Introduced or changed in [4c179f64e1](https://github.com/Jyothy-p-anil/IssueInsight/commit/4c179f64e177a16ce2f536aa4b8c025639566ab9) — feat(module-7): add reporter ticket status filtering.

#### `templates/tickets/customer_my_tickets.html`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/4c179f64e177a16ce2f536aa4b8c025639566ab9/templates/tickets/customer_my_tickets.html#L1-L124)

```html

{% extends 'base.html' %}

{% block title %}My Tickets | IssueInsight{% endblock %}

{% block content %}

<div class="d-flex justify-content-between align-items-center mb-3">
    <h2>My Tickets</h2>

    <a href="{% url 'submit_customer_complaint' %}"
       class="btn btn-primary">
        + New Complaint
    </a>
</div>

<div class="card shadow-sm">
    
<form method="get" class="row g-2 align-items-end mb-3">

    <div class="col-12 col-sm-5 col-md-4">
        <label for="customer-status-filter" class="form-label">
            Filter by Status
        </label>

        <select name="status"
                id="customer-status-filter"
                class="form-select">

            <option value="">All Statuses</option>

            {% for value, label in status_choices %}
                <option value="{{ value }}"
                    {% if selected_status == value %}selected{% endif %}>
                    {{ label }}
                </option>
            {% endfor %}

        </select>
    </div>

    <div class="col-12 col-sm-auto">
        <button type="submit" class="btn btn-primary">
            Apply Filter
        </button>
    </div>

    {% if selected_status %}
        <div class="col-12 col-sm-auto">
            <a href="{% url 'customer_my_tickets' %}"
               class="btn btn-outline-secondary">
                Show All
            </a>
        </div>
    {% endif %}

</form>

    <div class="card-body table-responsive">

        <table class="table table-striped align-middle">
            <thead>
                <tr>
                    <th>Ticket</th>
                    <th>Title</th>
                    <th>Product</th>
                    <th>Category</th>
                    <th>Department</th>
                    <th>Status</th>
                    <th>Submitted</th>
                    <th>Actions</th>
                </tr>
            </thead>

            <tbody>
                {% for ticket in tickets %}
                    <tr>
                        <td>#{{ ticket.id }}</td>
                        <td>{{ ticket.title }}</td>

                        <td>
                            {% if ticket.product %}
                                {{ ticket.product.name }}
                            {% else %}
                                {{ ticket.other_product_name }}
                            {% endif %}
                        </td>

                        <td>{{ ticket.category|default:"—" }}</td>

                        <td>
                            {{ ticket.department|default:"Pending routing" }}
                        </td>

                        <td>{{ ticket.get_status_display }}</td>

                        <td>
                            {{ ticket.created_at|date:"d M Y, h:i A" }}
                        </td>
                        <td>
                        <a href="{% url 'ticket_detail' ticket.id %}"
                        class="btn btn-outline-primary btn-sm">
                            View Details
                        </a>
                    </td>
                    </tr>
                {% empty %}
                    <tr>
                        <td colspan="8" class="text-center">
                           {% if selected_status %}
                                No complaints found with this status.
                            {% else %}
                                No complaints submitted yet.
                            {% endif %}
                        </td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>

    </div>
</div>

{% endblock %}
```

### templates/tickets/employee_my_tickets.html

Introduced or changed in [4c179f64e1](https://github.com/Jyothy-p-anil/IssueInsight/commit/4c179f64e177a16ce2f536aa4b8c025639566ab9) — feat(module-7): add reporter ticket status filtering.

#### `templates/tickets/employee_my_tickets.html`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/4c179f64e177a16ce2f536aa4b8c025639566ab9/templates/tickets/employee_my_tickets.html#L1-L116)

```html

{% extends 'base.html' %}

{% block title %}My Tickets | IssueInsight{% endblock %}

{% block content %}

<div class="d-flex justify-content-between align-items-center mb-3">
    <h2>My Tickets</h2>

    <a href="{% url 'submit_employee_complaint' %}"
       class="btn btn-primary">
        + New Complaint
    </a>
</div>

<div class="card shadow-sm">
    
<form method="get" class="row g-2 align-items-end mb-3">

    <div class="col-12 col-sm-5 col-md-4">
        <label for="employee-status-filter" class="form-label">
            Filter by Status
        </label>

        <select name="status"
                id="employee-status-filter"
                class="form-select">

            <option value="">All Statuses</option>

            {% for value, label in status_choices %}
                <option value="{{ value }}"
                    {% if selected_status == value %}selected{% endif %}>
                    {{ label }}
                </option>
            {% endfor %}

        </select>
    </div>

    <div class="col-12 col-sm-auto">
        <button type="submit" class="btn btn-primary">
            Apply Filter
        </button>
    </div>

    {% if selected_status %}
        <div class="col-12 col-sm-auto">
            <a href="{% url 'employee_my_tickets' %}"
               class="btn btn-outline-secondary">
                Show All
            </a>
        </div>
    {% endif %}

</form>

    <div class="card-body table-responsive">

        <table class="table table-striped align-middle">
            <thead>
                <tr>
                    <th>Ticket</th>
                    <th>Title</th>
                    <th>Category</th>
                    <th>Department</th>
                    <th>Status</th>
                    <th>Submitted</th>
                    <th>Actions</th>
                </tr>
            </thead>

            <tbody>
                {% for ticket in tickets %}
                    
                    <tr>
                        <td>#{{ ticket.id }}</td>
                        <td>{{ ticket.title }}</td>
                        <td>{{ ticket.category|default:"—" }}</td>

                        <td>
                            {{ ticket.department|default:"Pending routing" }}
                        </td>

                        <td>{{ ticket.get_status_display }}</td>

                        <td>{{ ticket.created_at|date:"d M Y, h:i A" }}</td>

                        <td>
                            <a href="{% url 'ticket_detail' ticket.id %}"
                            class="btn btn-outline-primary btn-sm">
                                View Details
                            </a>
                        </td>
                    </tr>

                    
                {% empty %}
                    <tr>
                        <td colspan="7" class="text-center">
                            {% if selected_status %}
                                    No complaints found with this status.
                                {% else %}
                                    You have not submitted any complaints yet.
                                {% endif %}
                        </td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>

    </div>
</div>

{% endblock %}
```

### tickets/tests.py :: ReporterTicketDetailTests

Introduced or changed in [312193a651](https://github.com/Jyothy-p-anil/IssueInsight/commit/312193a6518f46d65a9905656917c8fc99ceca6c) — test(module-7): review reporter complaint details and privacy.

#### `tickets/tests.py` → `ReporterTicketDetailTests`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/4c179f64e177a16ce2f536aa4b8c025639566ab9/tickets/tests.py#L2044-L2228)

```python
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
```

*Showing the first 150 of 185 lines. Open the source link for the remainder.*

### tickets/tests.py :: ReporterTicketListFilterTests

Introduced or changed in [4c179f64e1](https://github.com/Jyothy-p-anil/IssueInsight/commit/4c179f64e177a16ce2f536aa4b8c025639566ab9) — feat(module-7): add reporter ticket status filtering.

#### `tickets/tests.py` → `ReporterTicketListFilterTests`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/4c179f64e177a16ce2f536aa4b8c025639566ab9/tickets/tests.py#L2230-L2504)

```python
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
```

*Showing the first 150 of 275 lines. Open the source link for the remainder.*

