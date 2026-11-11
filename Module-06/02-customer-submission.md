# Module 06 — Customer Complaint Submission

## Customer submission and My Tickets

### Before we begin

The server must establish the correct reporter, division and department regardless of submitted form values.

### What we worked on

The view sets system-owned fields, saves the complaint and redirects to the customer's private ticket list.

### Picture it this way

Follow one real request or data change through the functions shown below. Notice which fields come from the user and which are set by the server.

### Important Django concepts

`role_required`, `commit=False`, `redirect`, `object ownership`.

### Actual code from the committed project

Source revision: [`b5fac3135a3b`](https://github.com/Jyothy-p-anil/IssueInsight/commit/b5fac3135a3b92826b80454b47e933eda88b75f7) on `master`. The excerpts are current code, not invented historical versions.

#### `tickets/views.py` → `submit_customer_complaint`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/b5fac3135a3b92826b80454b47e933eda88b75f7/tickets/views.py#L127-L158)

```python
@role_required('customer')
def submit_customer_complaint(request):

    if request.method == 'POST':
        form = CustomerComplaintForm(request.POST)

        if form.is_valid():
            ticket = form.save(commit=False)

            ticket.reporter = request.user
            ticket.division = 'customer'
            ticket.status = 'submitted'

            ticket.department = ticket.category.department

            ticket.save()

            messages.success(
                request,
                f'Complaint #{ticket.pk} submitted successfully.'
            )

            return redirect('customer_my_tickets')

    else:
        form = CustomerComplaintForm()

    return render(
        request,
        'tickets/customer_complaint_form.html',
        {'form': form}
    )
```

#### `tickets/views.py` → `customer_my_tickets`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/b5fac3135a3b92826b80454b47e933eda88b75f7/tickets/views.py#L161-L175)

```python
@role_required('customer')
def customer_my_tickets(request):

    tickets = Ticket.objects.filter(
        reporter=request.user,
        division='customer'
    ).select_related(
        'category', 'department', 'product'
    ).order_by('-created_at')

    return render(
        request,
        'tickets/customer_my_tickets.html',
        {'tickets': tickets}
    )
```

#### `templates/tickets/customer_my_tickets.html`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/b5fac3135a3b92826b80454b47e933eda88b75f7/templates/tickets/customer_my_tickets.html#L1-L79)

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
                        <td colspan="7" class="text-center">
                            No complaints submitted yet.
                        </td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>

    </div>
</div>

{% endblock %}
```

**Verified references in this chapter:** 3/3.

### Related development commits

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

- Where is the reporter identity determined?
- How does the My Tickets view prevent cross-account access?

### Connections

Back to [this module's chapter list](README.md), or view the [complete source module map](../MODULE_INDEX.md).
