# Module 14 — User Interface Completion

## Bootstrap layout and shared CSS

### Before we begin

Consistent templates and navigation improve usability across different roles.

### What we worked on

Pages inherit base.html, use Bootstrap classes and load the static stylesheet.

### Picture it this way

Follow one real request or data change through the functions shown below. Notice which fields come from the user and which are set by the server.

### Important Django concepts

`Bootstrap`, `Django static tag`, `template inheritance`, `responsive layout`.

### Actual code from the committed project

Source revision: [`a9a40f739d52`](https://github.com/Jyothy-p-anil/IssueInsight/commit/a9a40f739d52f68c0d05b37955d53ea1baacecf8) on `master`. The excerpts are current code, not invented historical versions.

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

#### `static/css/style.css`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/a9a40f739d52f68c0d05b37955d53ea1baacecf8/static/css/style.css#L1-L11)

```css

/* Common IssueInsight styles */

body {
    font-family: Arial, sans-serif;
}

.welcome-title {
    color: #244a7d;
    font-weight: 700;
}
```

#### `templates/role_dashboard.html`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/a9a40f739d52f68c0d05b37955d53ea1baacecf8/templates/role_dashboard.html#L1-L18)

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

**Verified references in this chapter:** 3/3.

### Related development commits

- [4b84801902](https://github.com/Jyothy-p-anil/IssueInsight/commit/4b848019026ac23d14bd5c5630a41663e619bfdb) — feat: create shared base template (2026-11-05)
- [067cc07d58](https://github.com/Jyothy-p-anil/IssueInsight/commit/067cc07d58eb7691a9bd75a4e217d98a03f06769) — feat: add custom CSS styling (2026-11-05)
- [716dfced43](https://github.com/Jyothy-p-anil/IssueInsight/commit/716dfced43cfb14b301265cb9eced25295eca705) — feat: add role-specific dashboard navigation (2026-11-08)

*These links show historical changes. A commit may touch several modules; inspect its diff before attributing every edit to this chapter.*

### How we checked it

The source code and test definitions were inspected from Git. **This journal generator does not run Django tests** and cannot prove that every workflow works.

### Explain it independently

1. What existed before this feature?
2. Which file handles the incoming request or data?
3. Which checks protect the operation?
4. How do the results reach the next page or database record?

### Teacher / interview questions

- How does a child template reuse the base layout?
- Which screens still require visual review?

### Connections

Back to [this module's chapter list](README.md), or view the [complete source module map](../MODULE_INDEX.md).
