# Module 03 — Role-Based Permissions and Account Access

## Role decorator and dashboard routing

### Before we begin

Showing different links is not permission enforcement; Django must validate access on the server before executing a view.

### What we worked on

login_required checks authentication, role_required checks allowed roles, and dashboard_redirect selects the correct landing page.

### Picture it this way

Follow one real request or data change through the functions shown below. Notice which fields come from the user and which are set by the server.

### Important Django concepts

`decorator`, `login_required`, `wraps`, `request.user`, `redirect`, `messages`.

### Actual code from the committed project

Source revision: [`8aa5fec6ff3d`](https://github.com/Jyothy-p-anil/IssueInsight/commit/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a) on `master`. The excerpts are current code, not invented historical versions.

#### `accounts/decorators.py` → `role_required`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/accounts/decorators.py#L9-L31)

```python
def role_required(*allowed_roles):

    def decorator(view_func):

        @login_required
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):

            user = request.user

            if user.is_superuser or user.role in allowed_roles:
                return view_func(request, *args, **kwargs)

            messages.error(
                request,
                'You do not have permission to access that page.'
            )

            return redirect('dashboard_redirect')

        return wrapped_view

    return decorator
```

#### `tickets/views.py` → `dashboard_redirect`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/tickets/views.py#L59-L74)

```python
@login_required
def dashboard_redirect(request):
    user = request.user

    if user.is_superuser or user.role == 'admin':
        return redirect('admin_dashboard')

    dashboards = {
        'employee': 'employee_dashboard',
        'customer': 'customer_dashboard',
        'support': 'support_dashboard',
    }

    dashboard = dashboards.get(user.role, 'home')

    return redirect(dashboard)
```

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

**Verified references in this chapter:** 6/6.

### Related development commits

- [1f8dd69227](https://github.com/Jyothy-p-anil/IssueInsight/commit/1f8dd69227fc60a72c27f0b0c3c1e207411264c0) — feat: add reusable role-based access protection (2026-11-08)
- [2f17578632](https://github.com/Jyothy-p-anil/IssueInsight/commit/2f1757863287cda182a2ee3aca970ecbbe918648) — feat: create protected role dashboards (2026-11-08)
- [e4f6c84546](https://github.com/Jyothy-p-anil/IssueInsight/commit/e4f6c8454625fdc9465bcb15ad1d63cf895b2721) — feat: complete role-based dashboard redirection (2026-11-08)
- [ea64b763d1](https://github.com/Jyothy-p-anil/IssueInsight/commit/ea64b763d1c0e69bc4ef3b3645cc32fc87f12549) — test: finalize module 3 permissions (2026-11-08)
- [6885ea66b8](https://github.com/Jyothy-p-anil/IssueInsight/commit/6885ea66b8d30c3d5bf80cd622269134bf4d8665) — test: complete module 3 permission verification (2026-11-08)

*These links show historical changes. A commit may touch several modules; inspect its diff before attributing every edit to this chapter.*

### How we checked it

The source code and test definitions were inspected from Git. **This journal generator does not run Django tests** and cannot prove that every workflow works.

### Explain it independently

1. What existed before this feature?
2. Which file handles the incoming request or data?
3. Which checks protect the operation?
4. How do the results reach the next page or database record?

### Teacher / interview questions

- Explain what the three nested decorator functions do.
- What happens when an Employee guesses an Admin URL?

### Connections

Back to [this module's chapter list](README.md), or view the [complete source module map](../MODULE_INDEX.md).
