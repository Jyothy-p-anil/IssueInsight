# Module 07 — Automatically detected new code

These additions were linked to the module by **explicit module numbers in Git commit messages**. The code below is from the currently committed project; verify its behavior rather than assuming an unfinished feature is complete.

### templates/tickets/_reporter_ticket_filters.html

Introduced or changed in [0f32b2d705](https://github.com/Jyothy-p-anil/IssueInsight/commit/0f32b2d705ebbe252fa5f9726861428f5bb85900) — test(module-7): finalize all reporter ticket requirements.

#### `templates/tickets/_reporter_ticket_filters.html`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/templates/tickets/_reporter_ticket_filters.html#L1-L75)

```html



<form method="get" class="row g-2 align-items-end mb-3">

    <div class="col-12 col-md-4">
        <label for="ticket-search" class="form-label">
            Search Complaints
        </label>
        <input type="search"
               id="ticket-search"
               name="q"
               value="{{ search_query }}"
               class="form-control"
               placeholder="Title or ticket #">
    </div>

    <div class="col-12 col-sm-6 col-md-2">
        <label for="date-from" class="form-label">
            From Date
        </label>
        <input type="date"
               id="date-from"
               name="date_from"
               value="{{ date_from }}"
               class="form-control">
    </div>

    <div class="col-12 col-sm-6 col-md-2">
        <label for="date-to" class="form-label">
            To Date
        </label>
        <input type="date"
               id="date-to"
               name="date_to"
               value="{{ date_to }}"
               class="form-control">
    </div>

    <div class="col-12 col-md-3">
        <label for="ticket-status" class="form-label">
            Status
        </label>

        <select name="status"
                id="ticket-status"
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

    <div class="col-12 col-md-auto">
        <button type="submit" class="btn btn-primary">
            Apply Filter
        </button>
    </div>

    {% if filters_applied %}
        <div class="col-12 col-md-auto">
            <a href="{% url reset_url %}"
               class="btn btn-outline-secondary">
                Show All
            </a>
        </div>
    {% endif %}

</form>
```

### templates/tickets/customer_my_tickets.html

Introduced or changed in [0f32b2d705](https://github.com/Jyothy-p-anil/IssueInsight/commit/0f32b2d705ebbe252fa5f9726861428f5bb85900) — test(module-7): finalize all reporter ticket requirements.

#### `templates/tickets/customer_my_tickets.html`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/templates/tickets/customer_my_tickets.html#L1-L92)

```html

{% extends 'base.html' %}

{% block title %}My Tickets | IssueInsight{% endblock %}

{% block content %}

{% include 'tickets/_reporter_ticket_filters.html' %}

<div class="d-flex justify-content-between align-items-center mb-3">
    <h2>My Tickets</h2>

    <a href="{% url 'submit_customer_complaint' %}"
       class="btn btn-primary">
        + New Complaint
    </a>
</div>


    <div class="card shadow-sm">
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
                        <td class="text-break" style="min-width: 180px; max-width: 360px;">
                          {{ ticket.title }}
                        </td>

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
                            {% if filters_applied %}
                            {% if selected_status and not search_query and not date_from and not date_to %}
                                No complaints found with this status.
                            {% else %}
                                No complaints match your search or filters.
                            {% endif %}
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

Introduced or changed in [0f32b2d705](https://github.com/Jyothy-p-anil/IssueInsight/commit/0f32b2d705ebbe252fa5f9726861428f5bb85900) — test(module-7): finalize all reporter ticket requirements.

#### `templates/tickets/employee_my_tickets.html`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/templates/tickets/employee_my_tickets.html#L1-L86)

```html

{% extends 'base.html' %}

{% block title %}My Tickets | IssueInsight{% endblock %}

{% block content %}


{% include 'tickets/_reporter_ticket_filters.html' %}


<div class="d-flex justify-content-between align-items-center mb-3">
    <h2>My Tickets</h2>

    <a href="{% url 'submit_employee_complaint' %}"
       class="btn btn-primary">
        + New Complaint
    </a>
</div>


<div class="card shadow-sm">
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
                        <td class="text-break" style="min-width: 180px; max-width: 360px;">
                        {{ ticket.title }}
                         </td>
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
                                {% if filters_applied %}
                                {% if selected_status and not search_query and not date_from and not date_to %}
                                    No complaints found with this status.
                                {% else %}
                                    No complaints match your search or filters.
                                {% endif %}
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

### tickets/migrations/0006_ticket_updated_at.py :: Migration

Introduced or changed in [0f32b2d705](https://github.com/Jyothy-p-anil/IssueInsight/commit/0f32b2d705ebbe252fa5f9726861428f5bb85900) — test(module-7): finalize all reporter ticket requirements.

#### `tickets/migrations/0006_ticket_updated_at.py` → `Migration`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/tickets/migrations/0006_ticket_updated_at.py#L6-L18)

```python
class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0005_ticket_first_response_at_ticketmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
```

### tickets/tests.py :: ReporterTicketDetailTests

Introduced or changed in [312193a651](https://github.com/Jyothy-p-anil/IssueInsight/commit/312193a6518f46d65a9905656917c8fc99ceca6c) — test(module-7): review reporter complaint details and privacy.

#### `tickets/tests.py` → `ReporterTicketDetailTests`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/tickets/tests.py#L2049-L2233)

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

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/tickets/tests.py#L2235-L2509)

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

### tickets/tests.py :: ReporterTicketSearchDateUpdateTests

Introduced or changed in [0f32b2d705](https://github.com/Jyothy-p-anil/IssueInsight/commit/0f32b2d705ebbe252fa5f9726861428f5bb85900) — test(module-7): finalize all reporter ticket requirements.

#### `tickets/tests.py` → `ReporterTicketSearchDateUpdateTests`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/tickets/tests.py#L2511-L2922)

```python
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
```

*Showing the first 150 of 412 lines. Open the source link for the remainder.*

### tickets/views.py :: apply_reporter_ticket_filters

Introduced or changed in [0f32b2d705](https://github.com/Jyothy-p-anil/IssueInsight/commit/0f32b2d705ebbe252fa5f9726861428f5bb85900) — test(module-7): finalize all reporter ticket requirements.

#### `tickets/views.py` → `apply_reporter_ticket_filters`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/tickets/views.py#L114-L193)

```python
def apply_reporter_ticket_filters(request, tickets):

    search_query = request.GET.get('q', '').strip()
    selected_status = request.GET.get('status', '')

    valid_statuses = {
        value for value, label in Ticket.STATUS_CHOICES
    }

    if selected_status not in valid_statuses:
        selected_status = ''

    def valid_date(value):
        try:
            parsed = date.fromisoformat(value)
            if parsed.isoformat() == value:
                return parsed
        except (TypeError, ValueError):
            pass
        return None

    from_date = valid_date(request.GET.get('date_from', ''))
    to_date = valid_date(request.GET.get('date_to', ''))

    if search_query:
        candidate = (
            search_query[1:]
            if search_query.startswith('#')
            else search_query
        )

        if (
            candidate.isascii()
            and candidate.isdigit()
            and len(candidate) <= 18
        ):
            tickets = tickets.filter(
                Q(title__icontains=search_query)
                | Q(pk=int(candidate))
            )
        else:
            tickets = tickets.filter(
                title__icontains=search_query
            )

    if selected_status:
        tickets = tickets.filter(status=selected_status)

    if from_date:
        tickets = tickets.filter(
            created_at__date__gte=from_date
        )

    if to_date:
        tickets = tickets.filter(
            created_at__date__lte=to_date
        )

    date_from_value = (
        from_date.isoformat() if from_date else ''
    )
    date_to_value = (
        to_date.isoformat() if to_date else ''
    )

    filters = {
        'search_query': search_query,
        'selected_status': selected_status,
        'status_choices': Ticket.STATUS_CHOICES,
        'date_from': date_from_value,
        'date_to': date_to_value,
        'filters_applied': bool(
            search_query
            or selected_status
            or from_date
            or to_date
        ),
    }

    return tickets, filters
```

