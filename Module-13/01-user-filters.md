# Module 13 — Search, Filtering and Reporting

## Filtering users in Admin management

### Before we begin

Admins need to locate staff and customers without browsing the full account table.

### What we worked on

The view receives optional search, role, department and status GET parameters and builds a filtered User queryset.

### Picture it this way

Follow one real request or data change through the functions shown below. Notice which fields come from the user and which are set by the server.

### Important Django concepts

`GET parameters`, `Q objects`, `queryset filters`, `select_related`, `search`.

### Actual code from the committed project

Source revision: [`8aa5fec6ff3d`](https://github.com/Jyothy-p-anil/IssueInsight/commit/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a) on `master`. The excerpts are current code, not invented historical versions.

#### `accounts/views.py` → `manage_users`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/accounts/views.py#L75-L118)

```python
@role_required('admin')
def manage_users(request):

    search = request.GET.get('search', '').strip()
    role = request.GET.get('role', '')
    department = request.GET.get('department', '')
    status = request.GET.get('status', '')

    users = User.objects.filter(
        role__in=['employee', 'customer', 'support'],
        is_superuser=False
    ).select_related('department')

    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search)
        )

    if role in ['employee', 'customer', 'support']:
        users = users.filter(role=role)

    if department:
        users = users.filter(department__name=department)

    if status == 'active':
        users = users.filter(is_active=True)
    elif status == 'inactive':
        users = users.filter(is_active=False)

    users = users.order_by('username')

    departments = Department.objects.order_by('name')

    return render(request, 'accounts/manage_users.html', {
        'users': users,
        'departments': departments,
        'search': search,
        'selected_role': role,
        'selected_department': department,
        'selected_status': status,
    })
```

#### `templates/accounts/manage_users.html`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/templates/accounts/manage_users.html#L1-L178)

```html

{% extends 'base.html' %}

{% block title %}User Management | IssueInsight{% endblock %}

{% block content %}

<h2>User Management</h2>
<p class="text-muted">
    Manage Employees, Customers and Support Staff.
</p>
<a href="{% url 'create_staff_account' %}"
   class="btn btn-primary mt-2">
    + Add Employee / Support Staff
</a>

<div class="card shadow-sm mt-4">
    
<form method="get" class="row g-3 mt-2 mb-3">

    <div class="col-md-4">
        <label class="form-label">Search</label>
        <input type="text"
               name="search"
               value="{{ search }}"
               placeholder="Username, name or email"
               class="form-control">
    </div>

    <div class="col-md-2">
        <label class="form-label">Role</label>
        <select name="role" class="form-select">
            <option value="">All Roles</option>
            <option value="employee"
                {% if selected_role == 'employee' %}selected{% endif %}>
                Employee
            </option>
            <option value="customer"
                {% if selected_role == 'customer' %}selected{% endif %}>
                Customer
            </option>
            <option value="support"
                {% if selected_role == 'support' %}selected{% endif %}>
                Support Staff
            </option>
        </select>
    </div>

    <div class="col-md-3">
        <label class="form-label">Department</label>
        <select name="department" class="form-select">
            <option value="">All Departments</option>
            {% for dept in departments %}
                <option value="{{ dept.name }}"
                    {% if selected_department == dept.name %}selected{% endif %}>
                    {{ dept.name }}
                </option>
            {% endfor %}
        </select>
    </div>

    <div class="col-md-2">
        <label class="form-label">Status</label>
        <select name="status" class="form-select">
            <option value="">All Statuses</option>
            <option value="active"
                {% if selected_status == 'active' %}selected{% endif %}>
                Active
            </option>
            <option value="inactive"
                {% if selected_status == 'inactive' %}selected{% endif %}>
                Inactive
            </option>
        </select>
    </div>

    <div class="col-md-1 d-flex align-items-end">
        <button type="submit" class="btn btn-primary w-100">
            Go
        </button>
    </div>

    <div class="col-12">
        <a href="{% url 'manage_users' %}"
           class="btn btn-outline-secondary btn-sm">
            Clear Filters
        </a>
    </div>

</form>

    <div class="card-body">

        <div class="table-responsive">
            <table class="table table-striped align-middle">

                <thead>
                    <tr>
                        <th>Username</th>
                        <th>Email</th>
                        <th>Role</th>
                        <th>Department</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>

                <tbody>
                    {% for account in users %}
                    <tr>
                        <td>{{ account.username }}</td>
                        <td>{{ account.email }}</td>
                        <td>{{ account.get_role_display }}</td>
                        <td>{{ account.department|default:"—" }}</td>
                        <td>
                            {% if account.is_active %}
                                <span class="badge bg-success">
                                    Active
                                </span>
                            {% else %}
                                <span class="badge bg-secondary">
                                    Inactive
                                </span>
                            {% endif %}
                        </td>
                        <td>
                        <a href="{% url 'edit_user' account.id %}"
                        class="btn btn-outline-primary btn-sm">
                            Edit
                        </a>

                    <!--add buttons in User Management page to activate/deactivate user accounts-->
                            <form method="post"
                                action="{% url 'change_user_status' account.id %}"
                                class="d-inline">

                                {% csrf_token %}

                                {% if account.is_active %}
                                    <input type="hidden" name="action" value="deactivate">

                                    <button type="submit"
                                            class="btn btn-outline-danger btn-sm"
                                            onclick="return confirm('Deactivate this account?')">
                                        Deactivate
                                    </button>

                                {% else %}
                                    <input type="hidden" name="action" value="activate">
```

*Showing the first 150 of 178 lines. Open the source link for the remainder.*

**Verified references in this chapter:** 2/2.

### Related development commits

- [b585f71486](https://github.com/Jyothy-p-anil/IssueInsight/commit/b585f7148634d71ffa2b417548fe96fcdf010591) — feat: add user search and filters (2026-11-08)

*These links show historical changes. A commit may touch several modules; inspect its diff before attributing every edit to this chapter.*

### How we checked it

The source code and test definitions were inspected from Git. **This journal generator does not run Django tests** and cannot prove that every workflow works.

### Explain it independently

1. What existed before this feature?
2. Which file handles the incoming request or data?
3. Which checks protect the operation?
4. How do the results reach the next page or database record?

### Teacher / interview questions

- When would you use a Q object?
- Why is account search separate from future ticket reporting?

### Connections

Back to [this module's chapter list](README.md), or view the [complete source module map](../MODULE_INDEX.md).
