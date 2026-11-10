# Module 04 — Automatically detected new code

These additions were linked to the module by **explicit module numbers in Git commit messages**. The code below is from the currently committed project; verify its behavior rather than assuming an unfinished feature is complete.

### templates/base.html

Introduced or changed in [7e3f46e319](https://github.com/Jyothy-p-anil/IssueInsight/commit/7e3f46e319c60e257fa46980a0972e2b6bcc36ec) — feat(module-4): add software product listing and creation.

#### `templates/base.html`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/templates/base.html#L1-L212)

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

### templates/tickets/admin_categories.html

Introduced or changed in [06ddc706c9](https://github.com/Jyothy-p-anil/IssueInsight/commit/06ddc706c95a81ff3daade39c089303bf644e7be) — feat(module-4): add safe category editing and deletion.

#### `templates/tickets/admin_categories.html`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/templates/tickets/admin_categories.html#L1-L142)

```html

{% extends 'base.html' %}

{% block title %}Categories | IssueInsight{% endblock %}

{% block content %}

<h2>Category Management</h2>

<p class="text-muted">
    Manage complaint categories and their support departments.
</p>

<div class="card shadow-sm mb-4">
    <div class="card-body">

        <h5 class="card-title mb-3">Add Category</h5>

        <form method="post">
            {% csrf_token %}

            {% for field in form %}

                <div class="mb-3">

                    <label for="{{ field.id_for_label }}"
                           class="form-label">
                        {{ field.label }}
                    </label>

                    {{ field }}

                    {% for error in field.errors %}
                        <div class="text-danger small mt-1">
                            {{ error }}
                        </div>
                    {% endfor %}

                </div>

            {% endfor %}

            {% for error in form.non_field_errors %}
                <div class="alert alert-danger">
                    {{ error }}
                </div>
            {% endfor %}

            <div class="alert alert-info">
                Select a support department for normal
                categories. The category named "Other"
                must have no department because it
                requires manual routing.
            </div>

            <button type="submit"
                    class="btn btn-primary">
                Add Category
            </button>

        </form>

    </div>
</div>

<div class="card shadow-sm">
    <div class="card-body">

        <h5 class="card-title mb-3">
            Existing Categories
        </h5>

        <div class="table-responsive">

            <table class="table table-striped align-middle">

                <thead>
                    <tr>
                        <th>#</th>
                        <th>Category Name</th>
                        <th>Complaint Type</th>
                        <th>Support Department</th>
                        <th>Actions</th>
                    </tr>
                </thead>

                <tbody>

                    {% for category in categories %}

                        <tr>
                            <td>{{ forloop.counter }}</td>

                            <td>{{ category.name }}</td>

                            <td>
                                {{ category.get_division_display }}
                            </td>

                            <td>
                                {% if category.department %}
                                    {{ category.department.name }}
                                {% else %}
                                    <span class="text-warning">
                                        Manual Routing
                                    </span>
                                {% endif %}
                            </td>
                            <td>
                                <a href="{% url 'edit_category' category.pk %}"
                                class="btn btn-sm btn-outline-primary">
                                    Edit
                                </a>

                                <a href="{% url 'delete_category' category.pk %}"
                                class="btn btn-sm btn-outline-danger">
                                    Delete
                                </a>
                            </td>
                        </tr>

                    {% empty %}

                        <tr>
                            <td colspan="5"
                                class="text-center">
                                No categories found.
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

### templates/tickets/admin_category_confirm_delete.html

Introduced or changed in [06ddc706c9](https://github.com/Jyothy-p-anil/IssueInsight/commit/06ddc706c95a81ff3daade39c089303bf644e7be) — feat(module-4): add safe category editing and deletion.

#### `templates/tickets/admin_category_confirm_delete.html`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/templates/tickets/admin_category_confirm_delete.html#L1-L65)

```html

{% extends 'base.html' %}

{% block title %}Delete Category | IssueInsight{% endblock %}

{% block content %}

<h2>Delete Category</h2>

<div class="card shadow-sm">
    <div class="card-body">

        <h5>{{ category.name }}</h5>

        <p>
            Complaint Type:
            {{ category.get_division_display }}
        </p>

        <p>
            Existing Tickets:
            {{ ticket_count }}
        </p>

        {% if is_system_category %}

            <div class="alert alert-warning">
                The Other category is required for manual
                complaint routing and cannot be deleted.
            </div>

        {% elif ticket_count > 0 %}

            <div class="alert alert-warning">
                This category is used by existing complaints
                and cannot be deleted.
            </div>

        {% else %}

            <div class="alert alert-danger">
                Are you sure you want to permanently
                delete this category?
            </div>

            <form method="post">
                {% csrf_token %}

                <button type="submit"
                        class="btn btn-danger">
                    Confirm Delete
                </button>
            </form>

        {% endif %}

        <a href="{% url 'manage_categories' %}"
           class="btn btn-outline-secondary mt-3">
            Back to Categories
        </a>

    </div>
</div>

{% endblock %}
```

### templates/tickets/admin_category_edit.html

Introduced or changed in [06ddc706c9](https://github.com/Jyothy-p-anil/IssueInsight/commit/06ddc706c95a81ff3daade39c089303bf644e7be) — feat(module-4): add safe category editing and deletion.

#### `templates/tickets/admin_category_edit.html`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/templates/tickets/admin_category_edit.html#L1-L64)

```html

{% extends 'base.html' %}

{% block title %}Edit Category | IssueInsight{% endblock %}

{% block content %}

<h2>Edit Category</h2>

<p class="text-muted">
    Update the complaint category and support department.
</p>

<div class="card shadow-sm">
    <div class="card-body">

        <form method="post">
            {% csrf_token %}

            {% for field in form %}
                <div class="mb-3">

                    <label for="{{ field.id_for_label }}"
                           class="form-label">
                        {{ field.label }}
                    </label>

                    {{ field }}

                    {% for error in field.errors %}
                        <div class="text-danger small mt-1">
                            {{ error }}
                        </div>
                    {% endfor %}

                </div>
            {% endfor %}

            {% for error in form.non_field_errors %}
                <div class="alert alert-danger">
                    {{ error }}
                </div>
            {% endfor %}

            <p class="text-muted small">
                Changes to department mapping affect
                future complaints, not existing tickets.
            </p>

            <button type="submit"
                    class="btn btn-primary">
                Save Changes
            </button>

            <a href="{% url 'manage_categories' %}"
               class="btn btn-outline-secondary">
                Cancel
            </a>
        </form>

    </div>
</div>

{% endblock %}
```

### templates/tickets/admin_department_confirm_delete.html

Introduced or changed in [ead7bbac4a](https://github.com/Jyothy-p-anil/IssueInsight/commit/ead7bbac4a54131d9115fdc34f30108950facb33) — feat(module-4): add safe department editing and deletion.

#### `templates/tickets/admin_department_confirm_delete.html`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/templates/tickets/admin_department_confirm_delete.html#L1-L71)

```html

{% extends 'base.html' %}

{% block title %}Delete Department | IssueInsight{% endblock %}

{% block content %}

<h2>Delete Department</h2>

<div class="card shadow-sm">
    <div class="card-body">

        <h5>{{ department.name }}</h5>

        <p class="text-muted">
            Review existing references before deleting
            this department.
        </p>

        <table class="table table-bordered">
            <tbody>
                <tr>
                    <th>Support Staff</th>
                    <td>{{ staff_count }}</td>
                </tr>
                <tr>
                    <th>Complaint Categories</th>
                    <td>{{ category_count }}</td>
                </tr>
                <tr>
                    <th>Tickets</th>
                    <td>{{ ticket_count }}</td>
                </tr>
            </tbody>
        </table>

        {% if has_dependencies %}

            <div class="alert alert-warning">
                This department cannot be deleted while
                it has linked records. Reassign those
                records first.
            </div>

        {% else %}

            <div class="alert alert-danger">
                This action permanently deletes the
                department.
            </div>

            <form method="post">
                {% csrf_token %}

                <button type="submit"
                        class="btn btn-danger">
                    Confirm Delete
                </button>
            </form>

        {% endif %}

        <a href="{% url 'manage_departments' %}"
           class="btn btn-outline-secondary mt-3">
            Back to Departments
        </a>

    </div>
</div>

{% endblock %}
```

### templates/tickets/admin_department_edit.html

Introduced or changed in [ead7bbac4a](https://github.com/Jyothy-p-anil/IssueInsight/commit/ead7bbac4a54131d9115fdc34f30108950facb33) — feat(module-4): add safe department editing and deletion.

#### `templates/tickets/admin_department_edit.html`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/templates/tickets/admin_department_edit.html#L1-L52)

```html

{% extends 'base.html' %}

{% block title %}Edit Department | IssueInsight{% endblock %}

{% block content %}

<h2>Edit Department</h2>

<p class="text-muted">
    Update the department name.
</p>

<div class="card shadow-sm">
    <div class="card-body">

        <form method="post">
            {% csrf_token %}

            <div class="mb-3">

                <label for="{{ form.name.id_for_label }}"
                       class="form-label">
                    Department Name
                </label>

                {{ form.name }}

                {% for error in form.name.errors %}
                    <div class="text-danger small mt-1">
                        {{ error }}
                    </div>
                {% endfor %}

            </div>

            <button type="submit"
                    class="btn btn-primary">
                Save Changes
            </button>

            <a href="{% url 'manage_departments' %}"
               class="btn btn-outline-secondary">
                Cancel
            </a>

        </form>

    </div>
</div>

{% endblock %}
```

### templates/tickets/admin_departments.html

Introduced or changed in [ead7bbac4a](https://github.com/Jyothy-p-anil/IssueInsight/commit/ead7bbac4a54131d9115fdc34f30108950facb33) — feat(module-4): add safe department editing and deletion.

#### `templates/tickets/admin_departments.html`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/templates/tickets/admin_departments.html#L1-L101)

```html

{% extends 'base.html' %}

{% block title %}Departments | IssueInsight{% endblock %}

{% block content %}

<h2>Department Management</h2>

<p class="text-muted">
    View and add support departments.
</p>

<div class="card shadow-sm mb-4">
    <div class="card-body">

        <h5 class="card-title mb-3">
            Add Department
        </h5>

        <form method="post">
            {% csrf_token %}

            <div class="mb-3">
                <label for="{{ form.name.id_for_label }}"
                       class="form-label">
                    Department Name
                </label>

                {{ form.name }}

                {% for error in form.name.errors %}
                    <div class="text-danger small mt-1">
                        {{ error }}
                    </div>
                {% endfor %}
            </div>

            <button type="submit"
                    class="btn btn-primary">
                Add Department
            </button>
        </form>

    </div>
</div>

<div class="card shadow-sm">
    <div class="card-body">

        <h5 class="card-title mb-3">
            Existing Departments
        </h5>

        <div class="table-responsive">
            <table class="table table-striped align-middle">

                <thead>
                    <tr>
                        <th>#</th>
                        <th>Department Name</th>
                        <th>Actions</th>
                    </tr>
                </thead>

                <tbody>

                    {% for department in departments %}
                        <tr>
                            <td>{{ forloop.counter }}</td>
                            <td>{{ department.name }}</td>
                            <td>
                            <a href="{% url 'edit_department' department.pk %}"
                            class="btn btn-sm btn-outline-primary">
                                Edit
                            </a>

                            <a href="{% url 'delete_department' department.pk %}"
                            class="btn btn-sm btn-outline-danger">
                                Delete
                            </a>
                        </td>
                        </tr>

                    {% empty %}
                        <tr>
                            <td colspan="3" class="text-center">
                                No departments found.
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

### templates/tickets/admin_product_edit.html

Introduced or changed in [0cd5801c70](https://github.com/Jyothy-p-anil/IssueInsight/commit/0cd5801c70835ff6709c5156cc8478906f67573d) — feat(module-4): add product editing and activation controls.

#### `templates/tickets/admin_product_edit.html`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/templates/tickets/admin_product_edit.html#L1-L61)

```html

{% extends 'base.html' %}

{% block title %}Edit Product | IssueInsight{% endblock %}

{% block content %}

<h2>Edit Software Product</h2>

<p class="text-muted">
    Update the software product name.
</p>

<div class="card shadow-sm">
    <div class="card-body">

        <form method="post">
            {% csrf_token %}

            <div class="mb-3">

                <label for="{{ form.name.id_for_label }}"
                       class="form-label">
                    Product Name
                </label>

                {{ form.name }}

                {% for error in form.name.errors %}
                    <div class="text-danger small mt-1">
                        {{ error }}
                    </div>
                {% endfor %}

            </div>

            <p class="text-muted small">
                Current status:
                {% if product.is_active %}
                    Active
                {% else %}
                    Inactive
                {% endif %}
            </p>

            <button type="submit"
                    class="btn btn-primary">
                Save Changes
            </button>

            <a href="{% url 'manage_products' %}"
               class="btn btn-outline-secondary">
                Cancel
            </a>

        </form>

    </div>
</div>

{% endblock %}
```

### templates/tickets/admin_products.html

Introduced or changed in [0cd5801c70](https://github.com/Jyothy-p-anil/IssueInsight/commit/0cd5801c70835ff6709c5156cc8478906f67573d) — feat(module-4): add product editing and activation controls.

#### `templates/tickets/admin_products.html`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/templates/tickets/admin_products.html#L1-L147)

```html

{% extends 'base.html' %}

{% block title %}Products | IssueInsight{% endblock %}

{% block content %}

<h2>Software Product Management</h2>

<p class="text-muted">
    View and add software products supported by the company.
</p>

<div class="card shadow-sm mb-4">
    <div class="card-body">

        <h5 class="card-title mb-3">
            Add Software Product
        </h5>

        <form method="post">
            {% csrf_token %}

            <div class="mb-3">

                <label for="{{ form.name.id_for_label }}"
                       class="form-label">
                    Product Name
                </label>

                {{ form.name }}

                {% for error in form.name.errors %}
                    <div class="text-danger small mt-1">
                        {{ error }}
                    </div>
                {% endfor %}

            </div>

            <button type="submit"
                    class="btn btn-primary">
                Add Product
            </button>

        </form>

    </div>
</div>

<div class="card shadow-sm">
    <div class="card-body">

        <h5 class="card-title mb-3">
            Existing Software Products
        </h5>

        <div class="table-responsive">

            <table class="table table-striped align-middle">

                <thead>
                    <tr>
                        <th>#</th>
                        <th>Product Name</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>

                <tbody>

                    {% for product in products %}

                        <tr>
                            <td>{{ forloop.counter }}</td>

                            <td>{{ product.name }}</td>

                            <td>
                                {% if product.is_active %}
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

                                <a href="{% url 'edit_product' product.pk %}"
                                class="btn btn-sm btn-outline-primary">
                                    Edit
                                </a>

                                <form method="post"
                                    action="{% url 'toggle_product_status' product.pk %}"
                                    class="d-inline">

                                    {% csrf_token %}

                                    {% if product.is_active %}

                                        <button type="submit"
                                                class="btn btn-sm btn-outline-danger">
                                            Deactivate
                                        </button>

                                    {% else %}

                                        <button type="submit"
                                                class="btn btn-sm btn-outline-success">
                                            Activate
                                        </button>

                                    {% endif %}

                                </form>

                            </td>



                        </tr>

                    {% empty %}

                        <tr>
                            <td colspan="4" class="text-center">
                                No software products found.
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

### tickets/admin.py :: DepartmentAdmin

Introduced or changed in [5e16387502](https://github.com/Jyothy-p-anil/IssueInsight/commit/5e16387502adca96312af28a939ecff4547cf1c6) — feat(module-4): implement department listing and creation.

#### `tickets/admin.py` → `DepartmentAdmin`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/tickets/admin.py#L9-L21)

```python
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):

   

    form = DepartmentForm
    list_display = ('name',)
    search_fields = ('name',)



    def has_delete_permission(self, request, obj=None):
        return False
```

### tickets/admin.py :: ProductAdmin

Introduced or changed in [7e3f46e319](https://github.com/Jyothy-p-anil/IssueInsight/commit/7e3f46e319c60e257fa46980a0972e2b6bcc36ec) — feat(module-4): add software product listing and creation.

#### `tickets/admin.py` → `ProductAdmin`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/tickets/admin.py#L48-L60)

```python
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    form = ProductForm

    list_display = ('name', 'is_active')

    list_filter = ('is_active',)

    search_fields = ('name',)

    def has_delete_permission(self, request, obj=None):
        return False
```

### tickets/forms.py :: CategoryForm

Introduced or changed in [5d8f56c9d6](https://github.com/Jyothy-p-anil/IssueInsight/commit/5d8f56c9d6f3bdd8220d3f9ead176e18bc3d8639) — feat(module-4): add category listing and creation.

#### `tickets/forms.py` → `CategoryForm`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/tickets/forms.py#L185-L304)

```python
class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category

        fields = (
            'name',
            'division',
            'department',
        )

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category name'
            }),
            'division': forms.Select(attrs={
                'class': 'form-select'
            }),
            'department': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

        labels = {
            'name': 'Category Name',
            'division': 'Complaint Type',
            'department': 'Support Department',
        }

    def clean_name(self):

        name = ' '.join(
            self.cleaned_data['name'].split()
        )

        return name

    def clean(self):

        cleaned_data = super().clean()

        name = cleaned_data.get('name')
        division = cleaned_data.get('division')
        department = cleaned_data.get('department')

        # Category names must be unique within a division.
        # The same name can exist once for Employee
        # and once for Customer complaints.

        if name and division:

            duplicate = Category.objects.filter(
                name__iexact=name,
                division=division
            ).exclude(pk=self.instance.pk).exists()

            if duplicate:
                self.add_error(
                    'name',
                    'This category already exists '
                    'for the selected complaint type.'
                )

        # Other complaints require manual routing.

        if name:

            if name.casefold() == 'other':

                if department:
                    self.add_error(
                        'department',
                        'The Other category must not have '
                        'a department. It uses manual routing.'
                    )

            elif not department:
                self.add_error(
                    'department',
                    'Select a support department '
                    'for this category.'
                )

            # Protect categories used by existing complaints
        if self.instance.pk and division:

            original = Category.objects.get(
                pk=self.instance.pk
            )

            if original.name.casefold() == 'other':

                if name and name.casefold() != 'other':
                    self.add_error(
                        'name',
                        'The Other category cannot be renamed.'
                    )

                if division != original.division:
                    self.add_error(
                        'division',
                        'The Other category cannot change '
                        'complaint type.'
                    )

            elif (
                division != original.division
                and Ticket.objects.filter(
                    category_id=self.instance.pk
                ).exists()
            ):
                self.add_error(
                    'division',
                    'Cannot change the complaint type '
                    'because existing tickets use this category.'
                )


        return cleaned_data
```

### tickets/forms.py :: DepartmentForm

Introduced or changed in [5e16387502](https://github.com/Jyothy-p-anil/IssueInsight/commit/5e16387502adca96312af28a939ecff4547cf1c6) — feat(module-4): implement department listing and creation.

#### `tickets/forms.py` → `DepartmentForm`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/tickets/forms.py#L154-L177)

```python
class DepartmentForm(forms.ModelForm):

    class Meta:
        model = Department
        fields = ('name',)

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter department name'
            })
        }

    def clean_name(self):
        name = ' '.join(self.cleaned_data['name'].split())

        if Department.objects.filter(
            name__iexact=name
        ).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(
                'A department with this name already exists.'
            )

        return name
```

### tickets/forms.py :: ProductForm

Introduced or changed in [7e3f46e319](https://github.com/Jyothy-p-anil/IssueInsight/commit/7e3f46e319c60e257fa46980a0972e2b6bcc36ec) — feat(module-4): add software product listing and creation.

#### `tickets/forms.py` → `ProductForm`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/tickets/forms.py#L309-L339)

```python
class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('name',)

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter software product name'
            })
        }

    def clean_name(self):

        name = ' '.join(
            self.cleaned_data['name'].split()
        )

        if Product.objects.filter(
            name__iexact=name
        ).exclude(
            pk=self.instance.pk
        ).exists():

            raise forms.ValidationError(
                'A software product with this name '
                'already exists.'
            )

        return name
```

### tickets/tests.py :: CategoryManagementTests

Introduced or changed in [5d8f56c9d6](https://github.com/Jyothy-p-anil/IssueInsight/commit/5d8f56c9d6f3bdd8220d3f9ead176e18bc3d8639) — feat(module-4): add category listing and creation.

#### `tickets/tests.py` → `CategoryManagementTests`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/tickets/tests.py#L273-L687)

```python
class CategoryManagementTests(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.admin = User.objects.create_user(
            username='category_admin',
            password='TestPass123!',
            role='admin'
        )

        cls.employee = User.objects.create_user(
            username='category_employee',
            password='TestPass123!',
            role='employee'
        )

        cls.facilities = Department.objects.create(
            name='Facilities Support'
        )

        cls.product_support = Department.objects.create(
            name='Product Support'
        )

    def test_only_admin_can_manage_categories(self):

        url = reverse('manage_categories')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)

        self.client.force_login(self.employee)

        response = self.client.get(url)
        self.assertRedirects(
            response,
            reverse('dashboard_redirect'),
            fetch_redirect_response=False
        )

        self.client.force_login(self.admin)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_admin_can_create_category(self):

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse('manage_categories'),
            {
                'name': 'Printer Issues',
                'division': 'employee',
                'department': self.facilities.pk,
            }
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Category.objects.filter(
                name='Printer Issues',
                division='employee',
                department=self.facilities
            ).exists()
        )

    def test_duplicate_category_rejected(self):

        Category.objects.create(
            name='IT Issues',
            division='employee',
            department=self.facilities
        )

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse('manage_categories'),
            {
                'name': 'it issues',
                'division': 'employee',
                'department': self.facilities.pk,
            }
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            Category.objects.filter(
                division='employee',
                name__iexact='IT Issues'
            ).count(),
            1
        )

        self.assertTrue(response.context['form'].errors)

    def test_same_name_allowed_for_different_divisions(self):

        Category.objects.create(
            name='Connection Issues',
            division='employee',
            department=self.facilities
        )

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse('manage_categories'),
            {
                'name': 'Connection Issues',
                'division': 'customer',
                'department': self.product_support.pk,
            }
        )

        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            Category.objects.filter(
                name='Connection Issues'
            ).count(),
            2
        )

    def test_other_category_has_manual_routing(self):

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse('manage_categories'),
            {
                'name': 'Other',
                'division': 'employee',
                'department': '',
            }
        )

        self.assertEqual(response.status_code, 302)

        category = Category.objects.get(
            name='Other',
            division='employee'
        )

        self.assertIsNone(category.department)
```

*Showing the first 150 of 415 lines. Open the source link for the remainder.*

### tickets/tests.py :: DepartmentManagementTests

Introduced or changed in [5e16387502](https://github.com/Jyothy-p-anil/IssueInsight/commit/5e16387502adca96312af28a939ecff4547cf1c6) — feat(module-4): implement department listing and creation.

#### `tickets/tests.py` → `DepartmentManagementTests`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/tickets/tests.py#L12-L270)

```python
class DepartmentManagementTests(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.admin = User.objects.create_user(
            username='department_admin',
            password='TestPass123!',
            role='admin'
        )

        cls.employee = User.objects.create_user(
            username='department_employee',
            password='TestPass123!',
            role='employee'
        )

    def test_only_admin_can_access_departments(self):

        url = reverse('manage_departments')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)

        self.client.force_login(self.employee)

        response = self.client.get(url)
        self.assertRedirects(
            response,
            reverse('dashboard_redirect'),
            fetch_redirect_response=False
        )

        self.client.force_login(self.admin)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_admin_can_create_department(self):

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse('manage_departments'),
            {'name': 'Quality Assurance Support'}
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Department.objects.filter(
                name='Quality Assurance Support'
            ).exists()
        )

    def test_duplicate_department_rejected(self):

        Department.objects.create(
            name='Facilities Support'
        )

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse('manage_departments'),
            {'name': 'FACILITIES SUPPORT'}
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            Department.objects.filter(
                name__iexact='Facilities Support'
            ).count(),
            1
        )

        self.assertTrue(
            response.context['form'].errors
        )

    def test_empty_department_name_rejected(self):

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse('manage_departments'),
            {'name': '   '}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Department.objects.count(), 0)

        
    def test_admin_can_edit_department(self):

        department = Department.objects.create(
            name='Testing Department'
        )

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse('edit_department', args=[department.pk]),
            {'name': 'Updated Department'}
        )

        self.assertEqual(response.status_code, 302)

        department.refresh_from_db()
        self.assertEqual(
            department.name,
            'Updated Department'
        )

    def test_edit_rejects_duplicate_name(self):

        Department.objects.create(
            name='Internal IT Support'
        )

        department = Department.objects.create(
            name='Testing Department'
        )

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse('edit_department', args=[department.pk]),
            {'name': 'internal it support'}
        )

        self.assertEqual(response.status_code, 200)

        department.refresh_from_db()
        self.assertEqual(
            department.name,
            'Testing Department'
        )

        self.assertTrue(response.context['form'].errors)

    def test_employee_cannot_edit_or_delete_departments(self):

        department = Department.objects.create(
            name='Protected Department'
        )

        self.client.force_login(self.employee)
```

*Showing the first 150 of 259 lines. Open the source link for the remainder.*

### tickets/tests.py :: ProductManagementTests

Introduced or changed in [7e3f46e319](https://github.com/Jyothy-p-anil/IssueInsight/commit/7e3f46e319c60e257fa46980a0972e2b6bcc36ec) — feat(module-4): add software product listing and creation.

#### `tickets/tests.py` → `ProductManagementTests`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/tickets/tests.py#L690-L799)

```python
class ProductManagementTests(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.admin = User.objects.create_user(
            username='product_admin',
            password='TestPass123!',
            role='admin'
        )

        cls.employee = User.objects.create_user(
            username='product_employee',
            password='TestPass123!',
            role='employee'
        )

    def test_only_admin_can_manage_products(self):

        url = reverse('manage_products')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)

        self.client.force_login(self.employee)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        response = self.client.post(
            url,
            {'name': 'Unauthorized Product'}
        )

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            Product.objects.filter(
                name='Unauthorized Product'
            ).exists()
        )

        self.client.force_login(self.admin)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_admin_can_create_active_product(self):

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse('manage_products'),
            {'name': 'DemoFlow'}
        )

        self.assertEqual(response.status_code, 302)

        product = Product.objects.get(name='DemoFlow')

        self.assertTrue(product.is_active)

    def test_duplicate_product_rejected(self):

        Product.objects.create(name='PayrollPro')

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse('manage_products'),
            {'name': 'payrollpro'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)

        self.assertEqual(Product.objects.count(), 1)

    def test_empty_product_name_rejected(self):

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse('manage_products'),
            {'name': '   '}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Product.objects.count(), 0)

    def test_only_active_products_are_selectable(self):

        active_product = Product.objects.create(
            name='ActiveDemo',
            is_active=True
        )

        inactive_product = Product.objects.create(
            name='InactiveDemo',
            is_active=False
        )

        form = CustomerComplaintForm()

        queryset = form.fields['product'].queryset

        self.assertIn(active_product, queryset)
        self.assertNotIn(inactive_product, queryset)
```

### tickets/tests.py :: ProductUpdateTests

Introduced or changed in [0cd5801c70](https://github.com/Jyothy-p-anil/IssueInsight/commit/0cd5801c70835ff6709c5156cc8478906f67573d) — feat(module-4): add product editing and activation controls.

#### `tickets/tests.py` → `ProductUpdateTests`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/tickets/tests.py#L802-L1003)

```python
class ProductUpdateTests(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.admin = User.objects.create_user(
            username='product_update_admin',
            password='TestPass123!',
            role='admin'
        )

        cls.employee = User.objects.create_user(
            username='product_update_employee',
            password='TestPass123!',
            role='employee'
        )

    def test_admin_can_edit_product_name(self):

        product = Product.objects.create(
            name='DemoFlow',
            is_active=False
        )

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse('edit_product', args=[product.pk]),
            {'name': 'DemoFlow Suite'}
        )

        self.assertEqual(response.status_code, 302)

        product.refresh_from_db()

        self.assertEqual(
            product.name,
            'DemoFlow Suite'
        )
        self.assertFalse(product.is_active)

    def test_duplicate_product_rename_rejected(self):

        Product.objects.create(name='PayrollPro')

        product = Product.objects.create(
            name='DemoFlow'
        )

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse('edit_product', args=[product.pk]),
            {'name': 'payrollpro'}
        )

        self.assertEqual(response.status_code, 200)

        product.refresh_from_db()
        self.assertEqual(product.name, 'DemoFlow')
        self.assertTrue(response.context['form'].errors)

    def test_admin_can_deactivate_and_reactivate_product(self):

        product = Product.objects.create(
            name='DemoFlow'
        )

        self.client.force_login(self.admin)

        url = reverse(
            'toggle_product_status',
            args=[product.pk]
        )

        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)

        product.refresh_from_db()
        self.assertFalse(product.is_active)

        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)

        product.refresh_from_db()
        self.assertTrue(product.is_active)

    def test_inactive_product_preserves_existing_ticket(self):

        product = Product.objects.create(
            name='LegacyProduct'
        )

        customer = User.objects.create_user(
            username='product_history_customer',
            password='TestPass123!',
            role='customer'
        )

        ticket = Ticket.objects.create(
            reporter=customer,
            division='customer',
            title='Existing software issue',
            description='Historical complaint.',
            product=product
        )

        self.client.force_login(self.admin)

        self.client.post(
            reverse(
                'toggle_product_status',
                args=[product.pk]
            )
        )

        product.refresh_from_db()
        ticket.refresh_from_db()

        self.assertFalse(product.is_active)
        self.assertEqual(ticket.product, product)

        form = CustomerComplaintForm()

        self.assertNotIn(
            product,
            form.fields['product'].queryset
        )

    def test_employee_cannot_edit_or_toggle_product(self):

        product = Product.objects.create(
            name='ProtectedProduct'
        )

        self.client.force_login(self.employee)

        edit_response = self.client.post(
            reverse('edit_product', args=[product.pk]),
            {'name': 'Unauthorized Name'}
        )

        toggle_response = self.client.post(
            reverse(
                'toggle_product_status',
                args=[product.pk]
            )
        )
```

*Showing the first 150 of 202 lines. Open the source link for the remainder.*

### tickets/views.py :: delete_category

Introduced or changed in [06ddc706c9](https://github.com/Jyothy-p-anil/IssueInsight/commit/06ddc706c95a81ff3daade39c089303bf644e7be) — feat(module-4): add safe category editing and deletion.

#### `tickets/views.py` → `delete_category`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/tickets/views.py#L767-L816)

```python
@role_required('admin')
def delete_category(request, category_id):

    category = get_object_or_404(
        Category,
        pk=category_id
    )

    ticket_count = category.ticket_set.count()
    is_system_category = (
        category.name.casefold() == 'other'
    )

    can_delete = (
        ticket_count == 0
        and not is_system_category
    )

    if request.method == 'POST':

        if not can_delete:
            messages.error(
                request,
                'This category cannot be deleted. '
                'It is either used by existing tickets '
                'or required for manual routing.'
            )

            return redirect('manage_categories')

        category_name = category.name
        category.delete()

        messages.success(
            request,
            f'{category_name} deleted successfully.'
        )

        return redirect('manage_categories')

    return render(
        request,
        'tickets/admin_category_confirm_delete.html',
        {
            'category': category,
            'ticket_count': ticket_count,
            'is_system_category': is_system_category,
            'can_delete': can_delete,
        }
    )
```

### tickets/views.py :: delete_department

Introduced or changed in [ead7bbac4a](https://github.com/Jyothy-p-anil/IssueInsight/commit/ead7bbac4a54131d9115fdc34f30108950facb33) — feat(module-4): add safe department editing and deletion.

#### `tickets/views.py` → `delete_department`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/tickets/views.py#L633-L682)

```python
@role_required('admin')
def delete_department(request, department_id):

    department = get_object_or_404(
        Department,
        pk=department_id
    )

    staff_count = department.staff_members.count()
    category_count = department.category_set.count()
    ticket_count = department.ticket_set.count()

    has_dependencies = any((
        staff_count,
        category_count,
        ticket_count
    ))

    if request.method == 'POST':

        if has_dependencies:
            messages.error(
                request,
                'Cannot delete this department because it '
                'is linked to staff, categories or tickets.'
            )

            return redirect('manage_departments')

        department_name = department.name
        department.delete()

        messages.success(
            request,
            f'{department_name} deleted successfully.'
        )

        return redirect('manage_departments')

    return render(
        request,
        'tickets/admin_department_confirm_delete.html',
        {
            'department': department,
            'staff_count': staff_count,
            'category_count': category_count,
            'ticket_count': ticket_count,
            'has_dependencies': has_dependencies,
        }
    )
```

### tickets/views.py :: edit_category

Introduced or changed in [06ddc706c9](https://github.com/Jyothy-p-anil/IssueInsight/commit/06ddc706c95a81ff3daade39c089303bf644e7be) — feat(module-4): add safe category editing and deletion.

#### `tickets/views.py` → `edit_category`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/tickets/views.py#L728-L762)

```python
@role_required('admin')
def edit_category(request, category_id):

    category = get_object_or_404(
        Category,
        pk=category_id
    )

    if request.method == 'POST':
        form = CategoryForm(
            request.POST,
            instance=category
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Category updated successfully.'
            )

            return redirect('manage_categories')

    else:
        form = CategoryForm(instance=category)

    return render(
        request,
        'tickets/admin_category_edit.html',
        {
            'form': form,
            'category': category,
        }
    )
```

### tickets/views.py :: edit_department

Introduced or changed in [ead7bbac4a](https://github.com/Jyothy-p-anil/IssueInsight/commit/ead7bbac4a54131d9115fdc34f30108950facb33) — feat(module-4): add safe department editing and deletion.

#### `tickets/views.py` → `edit_department`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/tickets/views.py#L594-L628)

```python
@role_required('admin')
def edit_department(request, department_id):

    department = get_object_or_404(
        Department,
        pk=department_id
    )

    if request.method == 'POST':
        form = DepartmentForm(
            request.POST,
            instance=department
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Department updated successfully.'
            )

            return redirect('manage_departments')

    else:
        form = DepartmentForm(instance=department)

    return render(
        request,
        'tickets/admin_department_edit.html',
        {
            'form': form,
            'department': department,
        }
    )
```

### tickets/views.py :: edit_product

Introduced or changed in [0cd5801c70](https://github.com/Jyothy-p-anil/IssueInsight/commit/0cd5801c70835ff6709c5156cc8478906f67573d) — feat(module-4): add product editing and activation controls.

#### `tickets/views.py` → `edit_product`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/tickets/views.py#L857-L891)

```python
@role_required('admin')
def edit_product(request, product_id):

    product = get_object_or_404(
        Product,
        pk=product_id
    )

    if request.method == 'POST':
        form = ProductForm(
            request.POST,
            instance=product
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Software product updated successfully.'
            )

            return redirect('manage_products')

    else:
        form = ProductForm(instance=product)

    return render(
        request,
        'tickets/admin_product_edit.html',
        {
            'form': form,
            'product': product,
        }
    )
```

### tickets/views.py :: manage_categories

Introduced or changed in [5d8f56c9d6](https://github.com/Jyothy-p-anil/IssueInsight/commit/5d8f56c9d6f3bdd8220d3f9ead176e18bc3d8639) — feat(module-4): add category listing and creation.

#### `tickets/views.py` → `manage_categories`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/tickets/views.py#L688-L722)

```python
@role_required('admin')
def manage_categories(request):

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            category = form.save()

            messages.success(
                request,
                f'{category.name} category added successfully.'
            )

            return redirect('manage_categories')

    else:
        form = CategoryForm()

    categories = Category.objects.select_related(
        'department'
    ).order_by(
        'division',
        'name',
        'pk'
    )

    return render(
        request,
        'tickets/admin_categories.html',
        {
            'categories': categories,
            'form': form,
        }
    )
```

### tickets/views.py :: manage_departments

Introduced or changed in [5e16387502](https://github.com/Jyothy-p-anil/IssueInsight/commit/5e16387502adca96312af28a939ecff4547cf1c6) — feat(module-4): implement department listing and creation.

#### `tickets/views.py` → `manage_departments`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/tickets/views.py#L558-L586)

```python
@role_required('admin')
def manage_departments(request):

    if request.method == 'POST':
        form = DepartmentForm(request.POST)

        if form.is_valid():
            department = form.save()

            messages.success(
                request,
                f'{department.name} added successfully.'
            )

            return redirect('manage_departments')

    else:
        form = DepartmentForm()

    departments = Department.objects.order_by('name')

    return render(
        request,
        'tickets/admin_departments.html',
        {
            'departments': departments,
            'form': form,
        }
    )
```

### tickets/views.py :: manage_products

Introduced or changed in [7e3f46e319](https://github.com/Jyothy-p-anil/IssueInsight/commit/7e3f46e319c60e257fa46980a0972e2b6bcc36ec) — feat(module-4): add software product listing and creation.

#### `tickets/views.py` → `manage_products`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/tickets/views.py#L821-L852)

```python
@role_required('admin')
def manage_products(request):

    if request.method == 'POST':
        form = ProductForm(request.POST)

        if form.is_valid():
            product = form.save()

            messages.success(
                request,
                f'{product.name} added successfully.'
            )

            return redirect('manage_products')

    else:
        form = ProductForm()

    products = Product.objects.order_by(
        'name',
        'pk'
    )

    return render(
        request,
        'tickets/admin_products.html',
        {
            'form': form,
            'products': products,
        }
    )
```

### tickets/views.py :: toggle_product_status

Introduced or changed in [0cd5801c70](https://github.com/Jyothy-p-anil/IssueInsight/commit/0cd5801c70835ff6709c5156cc8478906f67573d) — feat(module-4): add product editing and activation controls.

#### `tickets/views.py` → `toggle_product_status`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/tickets/views.py#L896-L922)

```python
@role_required('admin')
@require_POST
def toggle_product_status(request, product_id):

    product = get_object_or_404(
        Product,
        pk=product_id
    )

    product.is_active = not product.is_active

    product.save(
        update_fields=['is_active']
    )

    status = (
        'activated'
        if product.is_active
        else 'deactivated'
    )

    messages.success(
        request,
        f'{product.name} {status} successfully.'
    )

    return redirect('manage_products')
```

