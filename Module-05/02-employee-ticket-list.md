# Module 05 — Employee Complaint Submission

## Employee My Tickets

### Before we begin

After submission, an Employee needs a private overview of their own complaints.

### What we worked on

employee_my_tickets filters by reporter and employee division, then renders results newest-first.

### Picture it this way

Follow one real request or data change through the functions shown below. Notice which fields come from the user and which are set by the server.

### Important Django concepts

`filter`, `select_related`, `order_by`, `template context`.

### Actual code from the committed project

Source revision: [`a9a40f739d52`](https://github.com/Jyothy-p-anil/IssueInsight/commit/a9a40f739d52f68c0d05b37955d53ea1baacecf8) on `master`. The excerpts are current code, not invented historical versions.

#### `tickets/views.py` → `employee_my_tickets`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/a9a40f739d52f68c0d05b37955d53ea1baacecf8/tickets/views.py#L111-L123)

```python
@role_required('employee')
def employee_my_tickets(request):

    tickets = Ticket.objects.filter(
        reporter=request.user,
        division='employee'
    ).select_related(
        'category', 'department'
    ).order_by('-created_at')

    return render(request, 'tickets/employee_my_tickets.html', {
        'tickets': tickets
    })
```

#### `templates/tickets/employee_my_tickets.html`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/a9a40f739d52f68c0d05b37955d53ea1baacecf8/templates/tickets/employee_my_tickets.html#L1-L71)

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
                            You have not submitted any complaints yet.
                        </td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>

    </div>
</div>

{% endblock %}
```

**Verified references in this chapter:** 2/2.

### Related development commits

- [734a0417b0](https://github.com/Jyothy-p-anil/IssueInsight/commit/734a0417b0a72dc08f8fabe1a1fb5cc19d0a3d1f) — feat: implement employee complaint submission and my tickets (2026-11-08)
- [b5fac3135a](https://github.com/Jyothy-p-anil/IssueInsight/commit/b5fac3135a3b92826b80454b47e933eda88b75f7) — test(module-5): finalize all employee submission requirements (2026-11-11)
- [8ddf5a4945](https://github.com/Jyothy-p-anil/IssueInsight/commit/8ddf5a4945684003c31d54a3bc19af43a53799f3) — test(module-5): close employee submission checklist gaps (2026-11-10)
- [8aa5fec6ff](https://github.com/Jyothy-p-anil/IssueInsight/commit/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a) — test(module-5): complete employee complaint submission review (2026-11-10)

*These links show historical changes. A commit may touch several modules; inspect its diff before attributing every edit to this chapter.*

### How we checked it

The source code and test definitions were inspected from Git. **This journal generator does not run Django tests** and cannot prove that every workflow works.

### Explain it independently

1. What existed before this feature?
2. Which file handles the incoming request or data?
3. Which checks protect the operation?
4. How do the results reach the next page or database record?

### Teacher / interview questions

- Why filter by reporter instead of displaying every ticket?
- Why use select_related?

### Connections

Back to [this module's chapter list](README.md), or view the [complete source module map](../MODULE_INDEX.md).
