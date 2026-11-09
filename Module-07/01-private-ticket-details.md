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

Source revision: [`02a68f05b7ab`](https://github.com/Jyothy-p-anil/IssueInsight/commit/02a68f05b7ab83749791ab60b9cf2245a201c26d) on `master`. The excerpts are current code, not invented historical versions.

#### `tickets/views.py` → `ticket_detail`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/02a68f05b7ab83749791ab60b9cf2245a201c26d/tickets/views.py#L177-L210)

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

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/02a68f05b7ab83749791ab60b9cf2245a201c26d/templates/tickets/ticket_detail.html#L1-L195)

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

**Verified references in this chapter:** 2/2.

### Related development commits

- [734a0417b0](https://github.com/Jyothy-p-anil/IssueInsight/commit/734a0417b0a72dc08f8fabe1a1fb5cc19d0a3d1f) — feat: implement employee complaint submission and my tickets (2026-11-08)
- [67d4f75d55](https://github.com/Jyothy-p-anil/IssueInsight/commit/67d4f75d55377472f716645288ee2a2dc335e91d) — feat: implement customer complaint submission and my tickets (2026-11-08)

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
