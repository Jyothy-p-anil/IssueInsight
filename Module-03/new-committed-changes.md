# Module 03 — Automatically detected new code

These additions were linked to the module by **explicit module numbers in Git commit messages**. The code below is from the currently committed project; verify its behavior rather than assuming an unfinished feature is complete.

### templates/base.html

Introduced or changed in [6885ea66b8](https://github.com/Jyothy-p-anil/IssueInsight/commit/6885ea66b8d30c3d5bf80cd622269134bf4d8665) — test: complete module 3 permission verification.

#### `templates/base.html`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/a9a40f739d52f68c0d05b37955d53ea1baacecf8/templates/base.html#L1-L212)

```html

{% load static %}

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>{% block title %}IssueInsight{% endblock %}</title>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
          rel="stylesheet">

    <link rel="stylesheet"
          href="{% static 'css/style.css' %}">
</head>

<body class="bg-light">

    <!-- Top Navigation -->
    <nav class="navbar navbar-dark bg-dark">
        <div class="container-fluid">

            <a class="navbar-brand" href="{% url 'home' %}">
                IssueInsight
            </a>
            {% if not user.is_authenticated %}
            <a class="nav-link" href="{% url 'login' %}">
                Login
            </a>
            {% endif %}

        
<div class="d-flex align-items-center gap-3">

    {% if user.is_authenticated %}

        <span class="text-white">
            {{ user.username }}
        </span>

        <form method="post"
              action="{% url 'logout' %}"
              class="m-0">

            {% csrf_token %}

            <button type="submit"
                    class="btn btn-outline-light btn-sm">
                Logout
            </button>
        </form>

    {% else %}

        <span class="text-white">Guest</span>

    {% endif %}

</div>


        </div>
    </nav>

    <!-- Page Layout -->
    <div class="container-fluid">
        <div class="row">

            <!-- Sidebar -->
            <aside class="col-lg-3 col-xl-2 bg-white border-end p-3">

                <h6 class="text-muted mb-3">Navigation</h6>

                <div class="nav flex-column">

                    <a class="nav-link"
                       href="{% url 'home' %}">
                        Home
                    </a>

                    {% if user.is_authenticated %}

                        
                        {% if user.is_superuser or user.role == 'admin' %}

                            <a class="nav-link"
                            href="{% url 'admin_dashboard' %}">
                                Admin Dashboard
                            </a>

                            <a class="nav-link"
                            href="{% url 'manage_users' %}">
                            User Management
                            </a>
                            <a class="nav-link"
                                href="{% url 'manage_departments' %}">
                                    Departments
                                </a>
                                <a class="nav-link"
                                href="{% url 'admin_pending_routing' %}">
                                Pending Routing
                            </a>

                            <a class="nav-link"
                            href="{% url 'manage_categories' %}">
                                Categories
                            </a>
                            <a class="nav-link"
                            href="{% url 'manage_products' %}">
                                Software Products
                            </a>

                            <span class="nav-link text-muted">
                                Analytics (Coming Soon)
                            </span>

                        {% elif user.role == 'employee' %}

                            <a class="nav-link"
                            href="{% url 'employee_dashboard' %}">
                                Employee Dashboard
                            </a>

                           <a class="nav-link"
                                href="{% url 'submit_employee_complaint' %}">
                                    Submit Complaint
                                </a>

                                <a class="nav-link"
                                href="{% url 'employee_my_tickets' %}">
                                    My Tickets
                                </a>

                        {% elif user.role == 'customer' %}

                            <a class="nav-link"
                            href="{% url 'customer_dashboard' %}">
                                Customer Dashboard
                            </a>

                            <a class="nav-link"
                                href="{% url 'submit_customer_complaint' %}">
                                    Submit Complaint
                                </a>

                                <a class="nav-link"
                                href="{% url 'customer_my_tickets' %}">
```

*Showing the first 150 of 212 lines. Open the source link for the remainder.*

### templates/tickets/support_ticket_detail.html

Introduced or changed in [6885ea66b8](https://github.com/Jyothy-p-anil/IssueInsight/commit/6885ea66b8d30c3d5bf80cd622269134bf4d8665) — test: complete module 3 permission verification.

#### `templates/tickets/support_ticket_detail.html`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/a9a40f739d52f68c0d05b37955d53ea1baacecf8/templates/tickets/support_ticket_detail.html#L1-L210)

```html

{% extends 'base.html' %}

{% block title %}Ticket #{{ ticket.id }} | IssueInsight{% endblock %}

{% block content %}

<div class="d-flex justify-content-between
            align-items-start flex-wrap gap-3 mb-3">

    <div>
        <p class="text-muted mb-1">
            Ticket #{{ ticket.id }}
        </p>
        <h2>{{ ticket.title }}</h2>
        <span class="badge bg-secondary">
            {{ ticket.get_status_display }}
        </span>
    </div>

    {% if can_claim %}
        <form method="post"
              action="{% url 'claim_support_ticket' ticket.id %}">
            {% csrf_token %}
            <button type="submit" class="btn btn-primary">
                Claim Ticket
            </button>
        </form>
    {% endif %}

</div>

<div class="card shadow-sm mb-4">
    <div class="card-header">
        <strong>Complaint Information</strong>
    </div>

    <div class="card-body">
        <div class="row g-3">

            <div class="col-md-6">
                <strong>Reported By</strong>
                <p>{{ ticket.reporter.username }}</p>
            </div>

            <div class="col-md-6">
                <strong>Complaint Type</strong>
                <p>{{ ticket.get_division_display }}</p>
            </div>

            <div class="col-md-6">
                <strong>Category</strong>
                <p>{{ ticket.category|default:"Not specified" }}</p>
            </div>

            <div class="col-md-6">
                <strong>Department</strong>
                <p>{{ ticket.department }}</p>
            </div>

            {% if ticket.division == 'employee' %}
                <div class="col-md-6">
                    <strong>Floor / Location</strong>
                    <p>{{ ticket.floor|default:"Not specified" }}</p>
                </div>
            {% else %}
                <div class="col-md-6">
                    <strong>Product</strong>
                    <p>
                        {% if ticket.product %}
                            {{ ticket.product.name }}
                        {% else %}
                            {{ ticket.other_product_name|default:"Not specified" }}
                        {% endif %}
                    </p>
                </div>
            {% endif %}

            <div class="col-md-6">
                <strong>Assigned To</strong>
                <p>
                    {% if ticket.assigned_to %}
                        {{ ticket.assigned_to.username }}
                    {% else %}
                        Not assigned
                    {% endif %}
                </p>
            </div>

            <div class="col-md-6">
                <strong>Submitted</strong>
                <p>{{ ticket.created_at|date:"d M Y, h:i A" }}</p>
            </div>

        </div>
    </div>
</div>

<div class="card shadow-sm mb-4">
    <div class="card-header">
        <strong>Description</strong>
    </div>

    <div class="card-body">
        {{ ticket.description|linebreaksbr }}
    </div>
</div>


<div class="card shadow-sm mb-4">
    <div class="card-header">
        <strong>Ticket Conversation</strong>
    </div>

    <div class="card-body">

        <p class="text-muted small">
            First public support response:
            {% if ticket.first_response_at %}
                {{ ticket.first_response_at|date:"d M Y, h:i A" }}
            {% else %}
                Not recorded yet
            {% endif %}
        </p>

        {% for item in conversation %}
            <div class="border rounded p-3 mb-3
                        {% if item.is_internal %}bg-warning-subtle{% endif %}">

                <div class="d-flex justify-content-between
                            align-items-center flex-wrap gap-2 mb-2">

                    <strong>{{ item.author.username }}</strong>

                    <div>
                        {% if item.is_internal %}
                            <span class="badge bg-warning text-dark">
                                Internal Note
                            </span>
                        {% else %}
                            <span class="badge bg-primary">
                                Public
                            </span>
                        {% endif %}

                        <small class="text-muted ms-2">
                            {{ item.created_at|date:"d M Y, h:i A" }}
                        </small>
                    </div>
                </div>
```

*Showing the first 150 of 210 lines. Open the source link for the remainder.*

### templates/tickets/ticket_detail.html

Introduced or changed in [6885ea66b8](https://github.com/Jyothy-p-anil/IssueInsight/commit/6885ea66b8d30c3d5bf80cd622269134bf4d8665) — test: complete module 3 permission verification.

#### `templates/tickets/ticket_detail.html`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/a9a40f739d52f68c0d05b37955d53ea1baacecf8/templates/tickets/ticket_detail.html#L1-L195)

```html

{% extends 'base.html' %}

{% block title %}Ticket #{{ ticket.id }} | IssueInsight{% endblock %}

{% block content %}

<div class="d-flex justify-content-between
            align-items-start flex-wrap gap-3 mb-4">

    <div>
        <p class="text-muted mb-1">
            Ticket #{{ ticket.id }}
        </p>

        <h2>{{ ticket.title }}</h2>
    </div>

    <div>
        {% if ticket.status == 'submitted' %}
            <span class="badge bg-primary">
        {% elif ticket.status == 'in_progress' %}
            <span class="badge bg-warning text-dark">
        {% elif ticket.status == 'resolved' %}
            <span class="badge bg-success">
        {% elif ticket.status == 'closed' %}
            <span class="badge bg-secondary">
        {% else %}
            <span class="badge bg-info text-dark">
        {% endif %}
                {{ ticket.get_status_display }}
            </span>
    </div>
</div>

<div class="card shadow-sm mb-4">
    <div class="card-header">
        <strong>Complaint Information</strong>
    </div>

    <div class="card-body">
        <div class="row g-4">

            <div class="col-md-6">
                <strong>Complaint Type</strong>
                <p>{{ ticket.get_division_display }}</p>
            </div>

            <div class="col-md-6">
                <strong>Category</strong>
                <p>{{ ticket.category|default:"Not specified" }}</p>
            </div>

<div class="card shadow-sm mb-4">
    <div class="card-header">
        <strong>Conversation</strong>
    </div>

    <div class="card-body">

        <p class="text-muted small">
            First public support response:
            {% if ticket.first_response_at %}
                {{ ticket.first_response_at|date:"d M Y, h:i A" }}
            {% else %}
                Awaiting response
            {% endif %}
        </p>

        {% for item in conversation %}
            <div class="border rounded p-3 mb-3">
                <div class="d-flex justify-content-between
                            flex-wrap gap-2 mb-2">
                    <strong>{{ item.author.username }}</strong>
                    <small class="text-muted">
                        {{ item.created_at|date:"d M Y, h:i A" }}
                    </small>
                </div>

                <div>{{ item.body|linebreaksbr }}</div>
            </div>
        {% empty %}
            <p class="text-muted">
                No conversation messages yet.
            </p>
        {% endfor %}

        {% if can_reply %}
            <hr>

            <h6>Send a Message</h6>

            <form method="post"
                  action="{% url 'add_reporter_message' ticket.id %}">
                {% csrf_token %}

                <div class="mb-3">
                    {{ reply_form.body }}
                </div>

                <button type="submit"
                        class="btn btn-primary">
                    Send Message
                </button>
            </form>
        {% else %}
            <p class="text-muted mb-0">
                Replies are unavailable for the current
                ticket status.
            </p>
        {% endif %}

    </div>
</div>






            {% if ticket.division == 'employee' %}
                <div class="col-md-6">
                    <strong>Floor / Location</strong>
                    <p>{{ ticket.floor|default:"Not specified" }}</p>
                </div>
            {% endif %}

            {% if ticket.division == 'customer' %}
                <div class="col-md-6">
                    <strong>Software Product</strong>
                    <p>
                        {% if ticket.product %}
                            {{ ticket.product.name }}
                        {% else %}
                            {{ ticket.other_product_name|default:"Not specified" }}
                        {% endif %}
                    </p>
                </div>
            {% endif %}

            <div class="col-md-6">
                <strong>Department</strong>
                <p>
                    {{ ticket.department|default:"Pending routing" }}
                </p>
            </div>

            <div class="col-md-6">
                <strong>Assigned Support Staff</strong>
                <p>
```

*Showing the first 150 of 195 lines. Open the source link for the remainder.*

### tickets/forms.py :: ManualRoutingForm

Introduced or changed in [6885ea66b8](https://github.com/Jyothy-p-anil/IssueInsight/commit/6885ea66b8d30c3d5bf80cd622269134bf4d8665) — test: complete module 3 permission verification.

#### `tickets/forms.py` → `ManualRoutingForm`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/a9a40f739d52f68c0d05b37955d53ea1baacecf8/tickets/forms.py#L118-L127)

```python
class ManualRoutingForm(forms.Form):

    department = forms.ModelChoiceField(
        queryset=Department.objects.order_by('name'),
        empty_label='Select a support department',
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
```

### tickets/forms.py :: SupportMessageForm

Introduced or changed in [6885ea66b8](https://github.com/Jyothy-p-anil/IssueInsight/commit/6885ea66b8d30c3d5bf80cd622269134bf4d8665) — test: complete module 3 permission verification.

#### `tickets/forms.py` → `SupportMessageForm`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/a9a40f739d52f68c0d05b37955d53ea1baacecf8/tickets/forms.py#L145-L159)

```python
class SupportMessageForm(TicketMessageForm):

    class Meta(TicketMessageForm.Meta):
        fields = ('body', 'is_internal')

        widgets = {
            **TicketMessageForm.Meta.widgets,
            'is_internal': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

        labels = {
            'is_internal': 'Internal note (hidden from reporter)'
        }
```

### tickets/forms.py :: TicketMessageForm

Introduced or changed in [6885ea66b8](https://github.com/Jyothy-p-anil/IssueInsight/commit/6885ea66b8d30c3d5bf80cd622269134bf4d8665) — test: complete module 3 permission verification.

#### `tickets/forms.py` → `TicketMessageForm`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/a9a40f739d52f68c0d05b37955d53ea1baacecf8/tickets/forms.py#L130-L142)

```python
class TicketMessageForm(forms.ModelForm):

    class Meta:
        model = TicketMessage
        fields = ('body',)

        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your message...'
            })
        }
```

### tickets/models.py :: TicketMessage

Introduced or changed in [6885ea66b8](https://github.com/Jyothy-p-anil/IssueInsight/commit/6885ea66b8d30c3d5bf80cd622269134bf4d8665) — test: complete module 3 permission verification.

#### `tickets/models.py` → `TicketMessage`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/a9a40f739d52f68c0d05b37955d53ea1baacecf8/tickets/models.py#L137-L161)

```python
class TicketMessage(models.Model):

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='ticket_messages'
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='written_ticket_messages'
    )

    body = models.TextField()

    is_internal = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at', 'id']

    def __str__(self):
        return f'Message #{self.pk} on Ticket #{self.ticket_id}'
```

### tickets/views.py :: add_reporter_message

Introduced or changed in [6885ea66b8](https://github.com/Jyothy-p-anil/IssueInsight/commit/6885ea66b8d30c3d5bf80cd622269134bf4d8665) — test: complete module 3 permission verification.

#### `tickets/views.py` → `add_reporter_message`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/a9a40f739d52f68c0d05b37955d53ea1baacecf8/tickets/views.py#L388-L421)

```python
@role_required('employee', 'customer')
@require_POST
def add_reporter_message(request, ticket_id):

    ticket = get_object_or_404(
        Ticket,
        pk=ticket_id,
        reporter=request.user
    )

    if ticket.status not in (
        'submitted', 'in_progress', 'reopened'
    ):
        messages.error(
            request,
            'Replies are not available for this ticket status.'
        )
        return redirect('ticket_detail', ticket_id=ticket_id)

    form = TicketMessageForm(request.POST)

    if form.is_valid():
        message = form.save(commit=False)
        message.ticket = ticket
        message.author = request.user
        message.is_internal = False
        message.save()

        messages.success(request, 'Message sent successfully.')

    else:
        messages.error(request, 'Please enter a valid message.')

    return redirect('ticket_detail', ticket_id=ticket_id)
```

### tickets/views.py :: admin_pending_routing

Introduced or changed in [6885ea66b8](https://github.com/Jyothy-p-anil/IssueInsight/commit/6885ea66b8d30c3d5bf80cd622269134bf4d8665) — test: complete module 3 permission verification.

#### `tickets/views.py` → `admin_pending_routing`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/a9a40f739d52f68c0d05b37955d53ea1baacecf8/tickets/views.py#L483-L498)

```python
@role_required('admin')
def admin_pending_routing(request):

    tickets = Ticket.objects.filter(
        department__isnull=True,
        assigned_to__isnull=True,
        status__in=['submitted', 'reopened']
    ).select_related(
        'reporter', 'category', 'product'
    ).order_by('created_at')

    return render(
        request,
        'tickets/admin_pending_routing.html',
        {'tickets': tickets}
    )
```

### tickets/views.py :: admin_route_ticket

Introduced or changed in [6885ea66b8](https://github.com/Jyothy-p-anil/IssueInsight/commit/6885ea66b8d30c3d5bf80cd622269134bf4d8665) — test: complete module 3 permission verification.

#### `tickets/views.py` → `admin_route_ticket`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/a9a40f739d52f68c0d05b37955d53ea1baacecf8/tickets/views.py#L501-L554)

```python
@role_required('admin')
def admin_route_ticket(request, ticket_id):

    ticket = get_object_or_404(
        Ticket.objects.select_related(
            'reporter', 'category', 'product'
        ),
        pk=ticket_id,
        department__isnull=True,
        assigned_to__isnull=True,
        status__in=['submitted', 'reopened']
    )

    if request.method == 'POST':
        form = ManualRoutingForm(request.POST)

        if form.is_valid():
            department = form.cleaned_data['department']

            updated = Ticket.objects.filter(
                pk=ticket.pk,
                department__isnull=True,
                assigned_to__isnull=True,
                status__in=['submitted', 'reopened']
            ).update(
                department_id=department.pk
            )

            if updated:
                messages.success(
                    request,
                    f'Ticket #{ticket.pk} routed to '
                    f'{department.name}.'
                )
            else:
                messages.warning(
                    request,
                    'This ticket has already been routed '
                    'or is no longer eligible.'
                )

            return redirect('admin_pending_routing')

    else:
        form = ManualRoutingForm()

    return render(
        request,
        'tickets/admin_route_ticket.html',
        {
            'ticket': ticket,
            'form': form
        }
    )
```

