# Module 08 — Complaint Routing and Support Workflows

## Department queue, assigned tickets and claiming

### Before we begin

Support Staff must see only the workload for their own department; concurrent claims must not assign one ticket twice.

### What we worked on

The queue filters eligible unassigned tickets by department; a POST conditionally updates assigned_to and status.

### Picture it this way

Follow one real request or data change through the functions shown below. Notice which fields come from the user and which are set by the server.

### Important Django concepts

`queryset filters`, `atomic conditional update`, `POST`, `404 vs redirect`, `assignment`.

### Actual code from the committed project

Source revision: [`9d0620abbb2d`](https://github.com/Jyothy-p-anil/IssueInsight/commit/9d0620abbb2df25ca00a4301a4a2318325521dbe) on `master`. The excerpts are current code, not invented historical versions.

#### `tickets/views.py` → `support_department_queue`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/tickets/views.py#L219-L248)

```python
@role_required('support')
def support_department_queue(request):

    if not request.user.department_id:
        messages.warning(
            request,
            'Your account has no support department assigned.'
        )
        return redirect('support_dashboard')

    tickets = Ticket.objects.filter(
        department_id=request.user.department_id,
        assigned_to__isnull=True,
        status__in=['submitted', 'reopened']
    ).select_related(
        'reporter', 'category'
    ).order_by('created_at')

    return render(
        request,
        'tickets/support_ticket_list.html',
        {
            'tickets': tickets,
            'page_title': 'Department Queue',
            'description': (
                'Unassigned complaints waiting for your department.'
            ),
            'empty_message': 'No unassigned complaints.',
        }
    )
```

#### `tickets/views.py` → `support_assigned_tickets`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/tickets/views.py#L253-L279)

```python
@role_required('support')
def support_assigned_tickets(request):

    if not request.user.department_id:
        messages.warning(
            request,
            'Your account has no support department assigned.'
        )
        return redirect('support_dashboard')

    tickets = Ticket.objects.filter(
        department_id=request.user.department_id,
        assigned_to=request.user
    ).select_related(
        'reporter', 'category'
    ).order_by('-created_at')

    return render(
        request,
        'tickets/support_ticket_list.html',
        {
            'tickets': tickets,
            'page_title': 'Assigned Tickets',
            'description': 'Complaints assigned to you.',
            'empty_message': 'No tickets assigned to you.',
        }
    )
```

#### `tickets/views.py` → `support_ticket_detail`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/tickets/views.py#L284-L331)

```python
@role_required('support')
def support_ticket_detail(request, ticket_id):

    if not request.user.department_id:
        messages.warning(
            request,
            'Your account has no support department assigned.'
        )
        return redirect('support_dashboard')

    ticket = get_object_or_404(
        Ticket.objects.select_related(
            'reporter',
            'category',
            'department',
            'product',
            'assigned_to'
        ),
        pk=ticket_id,
        department_id=request.user.department_id
    )

    can_claim = (
        ticket.assigned_to_id is None
        and ticket.status in ('submitted', 'reopened')
    )

    
    conversation = ticket.ticket_messages.select_related(
        'author'
    )

    can_reply = (
        ticket.assigned_to_id == request.user.id
        and ticket.status in ('in_progress', 'reopened')
    )

    return render(
        request,
        'tickets/support_ticket_detail.html',
        {
            'ticket': ticket,
            'can_claim': can_claim,
            'conversation': conversation,
            'reply_form': SupportMessageForm(),
            'can_reply': can_reply,
        }
    )
```

#### `tickets/views.py` → `claim_support_ticket`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/tickets/views.py#L337-L383)

```python
@role_required('support')
@require_POST
def claim_support_ticket(request, ticket_id):

    if not request.user.department_id:
        messages.error(
            request,
            'Your account has no support department assigned.'
        )
        return redirect('support_dashboard')

    # Conditional update prevents two staff members
    # from successfully claiming the same ticket.

    updated = Ticket.objects.filter(
        pk=ticket_id,
        department_id=request.user.department_id,
        assigned_to__isnull=True,
        status__in=['submitted', 'reopened']
    ).update(
        assigned_to=request.user,
        status='in_progress'
    )

    if updated:
        messages.success(
            request,
            f'Ticket #{ticket_id} assigned to you.'
        )
        return redirect(
            'support_ticket_detail',
            ticket_id=ticket_id
        )

    # Do not reveal tickets from other departments.
    get_object_or_404(
        Ticket,
        pk=ticket_id,
        department_id=request.user.department_id
    )

    messages.warning(
        request,
        'This ticket is already assigned or cannot be claimed.'
    )

    return redirect('support_department_queue')
```

#### `templates/tickets/support_ticket_list.html`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/templates/tickets/support_ticket_list.html#L1-L66)

```html

{% extends 'base.html' %}

{% block title %}{{ page_title }} | IssueInsight{% endblock %}

{% block content %}

<h2>{{ page_title }}</h2>
<p class="text-muted">{{ description }}</p>

<div class="card shadow-sm mt-4">
    <div class="card-body">

        <div class="table-responsive">
            <table class="table table-striped align-middle">

                <thead>
                    <tr>
                        <th>Ticket</th>
                        <th>Title</th>
                        <th>Source</th>
                        <th>Category</th>
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
                        <td>{{ ticket.get_division_display }}</td>
                        <td>
                            {{ ticket.category|default:"—" }}
                        </td>
                        <td>{{ ticket.get_status_display }}</td>
                        <td>
                            {{ ticket.created_at|date:"d M Y, h:i A" }}
                        </td>
                        <td>
                            <a href="{% url 'support_ticket_detail' ticket.id %}"
                               class="btn btn-outline-primary btn-sm">
                                View Details
                            </a>
                        </td>
                    </tr>

                    {% empty %}
                    <tr>
                        <td colspan="7"
                            class="text-center text-muted py-4">
                            {{ empty_message }}
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>

            </table>
        </div>

    </div>
</div>

{% endblock %}
```

**Verified references in this chapter:** 5/5.

### Related development commits

- [2088cf9734](https://github.com/Jyothy-p-anil/IssueInsight/commit/2088cf9734d734220127fd71d0393ec3c612fd4c) — feat: implement support department queue and ticket claiming (2026-11-08)
- [fbf064e527](https://github.com/Jyothy-p-anil/IssueInsight/commit/fbf064e52736bab686affe4564365f9f8d6510c8) — feat: implement support department queue and ticket claiming (2026-11-08)

*These links show historical changes. A commit may touch several modules; inspect its diff before attributing every edit to this chapter.*

### How we checked it

The source code and test definitions were inspected from Git. **This journal generator does not run Django tests** and cannot prove that every workflow works.

### Explain it independently

1. What existed before this feature?
2. Which file handles the incoming request or data?
3. Which checks protect the operation?
4. How do the results reach the next page or database record?

### Teacher / interview questions

- How does claiming prevent two staff from taking the same ticket?
- Why isn't claiming equivalent to a first human acknowledgement?

### Connections

Back to [this module's chapter list](README.md), or view the [complete source module map](../MODULE_INDEX.md).
