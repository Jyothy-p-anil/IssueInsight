# Module 08 — Complaint Routing and Support Workflows

## Admin routing of complaints without departments

### Before we begin

An Other or unassigned category can leave a complaint without an automatic support department.

### What we worked on

Admin reviews unrouted eligible complaints and selects the destination department; the update checks the ticket is still unrouted.

### Picture it this way

Follow one real request or data change through the functions shown below. Notice which fields come from the user and which are set by the server.

### Important Django concepts

`ModelChoiceField`, `admin role check`, `conditional update`, `pending queue`.

### Actual code from the committed project

Source revision: [`4c179f64e177`](https://github.com/Jyothy-p-anil/IssueInsight/commit/4c179f64e177a16ce2f536aa4b8c025639566ab9) on `master`. The excerpts are current code, not invented historical versions.

#### `tickets/forms.py` → `ManualRoutingForm`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/4c179f64e177a16ce2f536aa4b8c025639566ab9/tickets/forms.py#L118-L127)

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

#### `tickets/views.py` → `admin_pending_routing`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/4c179f64e177a16ce2f536aa4b8c025639566ab9/tickets/views.py#L517-L532)

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

#### `tickets/views.py` → `admin_route_ticket`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/4c179f64e177a16ce2f536aa4b8c025639566ab9/tickets/views.py#L535-L588)

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

#### `templates/tickets/admin_pending_routing.html`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/4c179f64e177a16ce2f536aa4b8c025639566ab9/templates/tickets/admin_pending_routing.html#L1-L66)

```html

{% extends 'base.html' %}

{% block title %}Pending Routing | IssueInsight{% endblock %}

{% block content %}

<h2>Pending Routing</h2>

<p class="text-muted">
    Review complaints that have not been assigned
    to a support department.
</p>

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
                        <td>{{ ticket.category|default:"—" }}</td>
                        <td>
                            {{ ticket.created_at|date:"d M Y, h:i A" }}
                        </td>
                        <td>
                            <a href="{% url 'admin_route_ticket' ticket.id %}"
                               class="btn btn-outline-primary btn-sm">
                                View &amp; Route
                            </a>
                        </td>
                    </tr>

                    {% empty %}
                    <tr>
                        <td colspan="6"
                            class="text-center text-muted py-4">
                            No complaints are waiting for routing.
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

**Verified references in this chapter:** 4/4.

### Related development commits

- [cb2cc89fb9](https://github.com/Jyothy-p-anil/IssueInsight/commit/cb2cc89fb9d711535dadfebde08efc17c696aed5) — feat: add manual routing and ticket conversations (2026-11-08)

*These links show historical changes. A commit may touch several modules; inspect its diff before attributing every edit to this chapter.*

### How we checked it

The source code and test definitions were inspected from Git. **This journal generator does not run Django tests** and cannot prove that every workflow works.

### Explain it independently

1. What existed before this feature?
2. Which file handles the incoming request or data?
3. Which checks protect the operation?
4. How do the results reach the next page or database record?

### Teacher / interview questions

- What causes a ticket to need manual routing?
- Why recheck department__isnull=True at update time?

### Connections

Back to [this module's chapter list](README.md), or view the [complete source module map](../MODULE_INDEX.md).
