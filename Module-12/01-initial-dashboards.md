# Module 12 — Dashboards and Analytics

## Initial dashboards and role routing

### Before we begin

Each user role needs an appropriate landing page before we add business analytics.

### What we worked on

Dashboard views pass a page title to a shared template; dashboard_redirect selects based on role.

### Picture it this way

Follow one real request or data change through the functions shown below. Notice which fields come from the user and which are set by the server.

### Important Django concepts

`render`, `context dictionary`, `redirect`, `role-based navigation`.

### Actual code from the committed project

Source revision: [`8aa5fec6ff3d`](https://github.com/Jyothy-p-anil/IssueInsight/commit/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a) on `master`. The excerpts are current code, not invented historical versions.

#### `tickets/views.py` → `employee_dashboard`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/tickets/views.py#L32-L36)

```python
@role_required('employee')
def employee_dashboard(request):
    return render(request, 'role_dashboard.html', {
        'page_title': 'Employee Dashboard'
    })
```

#### `tickets/views.py` → `customer_dashboard`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/tickets/views.py#L39-L43)

```python
@role_required('customer')
def customer_dashboard(request):
    return render(request, 'role_dashboard.html', {
        'page_title': 'Customer Dashboard'
    })
```

#### `tickets/views.py` → `support_dashboard`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/tickets/views.py#L46-L50)

```python
@role_required('support')
def support_dashboard(request):
    return render(request, 'role_dashboard.html', {
        'page_title': 'Support Staff Dashboard'
    })
```

#### `tickets/views.py` → `admin_dashboard`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/tickets/views.py#L53-L57)

```python
@role_required('admin')
def admin_dashboard(request):
    return render(request, 'role_dashboard.html', {
        'page_title': 'Admin Dashboard'
    })
```

#### `templates/role_dashboard.html`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/templates/role_dashboard.html#L1-L18)

```html

{% extends 'base.html' %}

{% block title %}{{ page_title }} | IssueInsight{% endblock %}

{% block content %}

<h2>{{ page_title }}</h2>

<p class="text-muted">
    Welcome, {{ user.username }}.
</p>

<p>
    Your dashboard features will appear here.
</p>

{% endblock %}
```

**Verified references in this chapter:** 5/5.

### Related development commits

- [2f17578632](https://github.com/Jyothy-p-anil/IssueInsight/commit/2f1757863287cda182a2ee3aca970ecbbe918648) — feat: create protected role dashboards (2026-11-08)
- [e4f6c84546](https://github.com/Jyothy-p-anil/IssueInsight/commit/e4f6c8454625fdc9465bcb15ad1d63cf895b2721) — feat: complete role-based dashboard redirection (2026-11-08)

*These links show historical changes. A commit may touch several modules; inspect its diff before attributing every edit to this chapter.*

### How we checked it

The source code and test definitions were inspected from Git. **This journal generator does not run Django tests** and cannot prove that every workflow works.

### Explain it independently

1. What existed before this feature?
2. Which file handles the incoming request or data?
3. Which checks protect the operation?
4. How do the results reach the next page or database record?

### Teacher / interview questions

- Which parts are only placeholders?
- Where would later analytics queries belong?

### Connections

Back to [this module's chapter list](README.md), or view the [complete source module map](../MODULE_INDEX.md).
