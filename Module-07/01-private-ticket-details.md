# Module 07 — My Tickets and Complaint Details

## Private ticket details and public conversation

### Before we begin

An ID in a URL must not allow one user to inspect someone else's complaint.

### What we worked on

ticket_detail retrieves the ticket only if its reporter is request.user, prepares public messages and renders ticket information.

### Picture it this way

Follow one real request or data change through the functions shown below. Notice which fields come from the user and which are set by the server.

### Important Django concepts

`object-level authorization`, `get_object_or_404`, `select_related`, `reverse URL`.

### Actual code from the committed project

Source revision: [`0f32b2d705eb`](https://github.com/Jyothy-p-anil/IssueInsight/commit/0f32b2d705ebbe252fa5f9726861428f5bb85900) on `master`. The excerpts are current code, not invented historical versions.

#### `tickets/views.py` → `ticket_detail`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/tickets/views.py#L287-L320)

```python
@role_required('employee', 'customer')
def ticket_detail(request, ticket_id):

    ticket = get_object_or_404(
        Ticket.objects.select_related(
            'reporter',
            'category',
            'department',
            'product',
            'assigned_to'
        ),
        pk=ticket_id,
        reporter=request.user
    )

    
    conversation = ticket.ticket_messages.filter(
        is_internal=False
    ).select_related('author')

    can_reply = ticket.status in (
        'submitted', 'in_progress', 'reopened'
    )

    return render(
        request,
        'tickets/ticket_detail.html',
        {
            'ticket': ticket,
            'conversation': conversation,
            'reply_form': TicketMessageForm(),
            'can_reply': can_reply,
        }
    )
```

#### `templates/tickets/ticket_detail.html`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/templates/tickets/ticket_detail.html#L1-L191)

```html

{% extends 'base.html' %}

{% block title %}Ticket #{{ ticket.id }} | IssueInsight{% endblock %}

{% block content %}

<div class="d-flex justify-content-between align-items-start flex-wrap gap-3 mb-4">
    <div>
        <p class="text-muted mb-1">Ticket #{{ ticket.id }}</p>
        <h2 class="text-break">{{ ticket.title }}</h2>
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
                <p>{{ ticket.department|default:"Pending routing" }}</p>
            </div>

            <div class="col-md-6">
                <strong>Assigned Support Staff</strong>
                <p>
                    {% if ticket.assigned_to %}
                        {{ ticket.assigned_to.username }}
                    {% else %}
                        Not assigned yet
                    {% endif %}
                </p>
            </div>

            <div class="col-md-6">
                <strong>Submitted By</strong>
                <p>{{ ticket.reporter.username }}</p>
            </div>

            <div class="col-md-6">
                <strong>Submitted On</strong>
                <div class="col-md-6">
                <strong>Latest Update</strong>
                <p>
                    {% if ticket.updated_at %}
                        {{ ticket.updated_at|date:"d M Y, h:i A" }}
                    {% else %}
                        Not recorded for this older ticket
                    {% endif %}
                </p>
            </div>
                <p>{{ ticket.created_at|date:"d M Y, h:i A" }}</p>
            </div>

        </div>
    </div>
</div>

<div class="card shadow-sm mb-4">
    <div class="card-header">
        <strong>Complaint Description</strong>
    </div>
    <div class="card-body text-break">
        {{ ticket.description|linebreaksbr }}
    </div>
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
            <div class="border-start border-2 ps-3 mb-3">
                 <strong>Complaint Submitted</strong>
                <div class="text-muted small">
                    {{ ticket.created_at|date:"d M Y, h:i A" }}
                </div>
            </div>
        {% for item in conversation %}
            <div class="border rounded p-3 mb-3">
                <div class="d-flex justify-content-between flex-wrap gap-2 mb-2">
                    <strong>{{ item.author.username }}</strong>
                    <small class="text-muted">
                        {{ item.created_at|date:"d M Y, h:i A" }}
                    </small>
                </div>

                <div>{{ item.body|linebreaksbr }}</div>
            </div>
        {% empty %}
            <p class="text-muted">
```

*Showing the first 150 of 191 lines. Open the source link for the remainder.*

**Verified references in this chapter:** 2/2.

### Related development commits

- [734a0417b0](https://github.com/Jyothy-p-anil/IssueInsight/commit/734a0417b0a72dc08f8fabe1a1fb5cc19d0a3d1f) — feat: implement employee complaint submission and my tickets (2026-11-08)
- [67d4f75d55](https://github.com/Jyothy-p-anil/IssueInsight/commit/67d4f75d55377472f716645288ee2a2dc335e91d) — feat: implement customer complaint submission and my tickets (2026-11-08)
- [0f32b2d705](https://github.com/Jyothy-p-anil/IssueInsight/commit/0f32b2d705ebbe252fa5f9726861428f5bb85900) — test(module-7): finalize all reporter ticket requirements (2026-11-11)
- [4c179f64e1](https://github.com/Jyothy-p-anil/IssueInsight/commit/4c179f64e177a16ce2f536aa4b8c025639566ab9) — feat(module-7): add reporter ticket status filtering (2026-11-11)
- [312193a651](https://github.com/Jyothy-p-anil/IssueInsight/commit/312193a6518f46d65a9905656917c8fc99ceca6c) — test(module-7): review reporter complaint details and privacy (2026-11-11)

*These links show historical changes. A commit may touch several modules; inspect its diff before attributing every edit to this chapter.*

### How we checked it

The source code and test definitions were inspected from Git. **This journal generator does not run Django tests** and cannot prove that every workflow works.

### Explain it independently

1. What existed before this feature?
2. Which file handles the incoming request or data?
3. Which checks protect the operation?
4. How do the results reach the next page or database record?

### Teacher / interview questions

- What happens when a user changes the ticket_id in the URL?
- Why are internal notes excluded from the reporter's view?

### Connections

Back to [this module's chapter list](README.md), or view the [complete source module map](../MODULE_INDEX.md).
