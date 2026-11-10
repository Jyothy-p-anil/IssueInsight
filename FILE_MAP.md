# Shared file-to-module guide

A file can serve several modules. The `SOURCE_MAPPING.csv` file identifies functions/classes more precisely.

| File | Modules |
|---|---|
| [`accounts/admin.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/accounts/admin.py) | 1 |
| [`accounts/apps.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/accounts/apps.py) | 1 |
| [`accounts/decorators.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/accounts/decorators.py) | 3 |
| [`accounts/forms.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/accounts/forms.py) | 2 |
| [`accounts/models.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/accounts/models.py) | 1 |
| [`accounts/services.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/accounts/services.py) | 2 |
| [`accounts/test_module3_security.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/accounts/test_module3_security.py) | 3, 15 |
| [`accounts/tests.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/accounts/tests.py) | 3, 15 |
| [`accounts/views.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/accounts/views.py) | 2, 3, 13 |
| [`config/settings.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/config/settings.py) | 1 |
| [`config/urls.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/config/urls.py) | 2 |
| [`manage.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/manage.py) | 1 |
| [`static/css/style.css`](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/static/css/style.css) | 2, 14 |
| [`templates/accounts/manage_users.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/templates/accounts/manage_users.html) | 13 |
| [`templates/base.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/templates/base.html) | 2, 3, 4, 14 |
| [`templates/home.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/templates/home.html) | 2 |
| [`templates/role_dashboard.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/templates/role_dashboard.html) | 12, 14 |
| [`templates/tickets/admin_categories.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/templates/tickets/admin_categories.html) | 4 |
| [`templates/tickets/admin_category_confirm_delete.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/templates/tickets/admin_category_confirm_delete.html) | 4 |
| [`templates/tickets/admin_category_edit.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/templates/tickets/admin_category_edit.html) | 4 |
| [`templates/tickets/admin_department_confirm_delete.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/templates/tickets/admin_department_confirm_delete.html) | 4 |
| [`templates/tickets/admin_department_edit.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/templates/tickets/admin_department_edit.html) | 4 |
| [`templates/tickets/admin_departments.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/templates/tickets/admin_departments.html) | 4 |
| [`templates/tickets/admin_pending_routing.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/templates/tickets/admin_pending_routing.html) | 8 |
| [`templates/tickets/admin_product_edit.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/templates/tickets/admin_product_edit.html) | 4 |
| [`templates/tickets/admin_products.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/templates/tickets/admin_products.html) | 4 |
| [`templates/tickets/customer_complaint_form.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/templates/tickets/customer_complaint_form.html) | 6 |
| [`templates/tickets/customer_my_tickets.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/templates/tickets/customer_my_tickets.html) | 6 |
| [`templates/tickets/employee_complaint_form.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/templates/tickets/employee_complaint_form.html) | 5 |
| [`templates/tickets/employee_my_tickets.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/templates/tickets/employee_my_tickets.html) | 5 |
| [`templates/tickets/support_ticket_detail.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/templates/tickets/support_ticket_detail.html) | 3 |
| [`templates/tickets/support_ticket_list.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/templates/tickets/support_ticket_list.html) | 8 |
| [`templates/tickets/ticket_detail.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/templates/tickets/ticket_detail.html) | 3, 7 |
| [`tickets/admin.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/tickets/admin.py) | 1, 4 |
| [`tickets/apps.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/tickets/apps.py) | 1 |
| [`tickets/forms.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/tickets/forms.py) | 3, 4, 5, 6, 8, 9 |
| [`tickets/management/commands/seed_initial_data.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/tickets/management/commands/seed_initial_data.py) | 1, 4 |
| [`tickets/models.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/tickets/models.py) | 1, 3, 4, 9 |
| [`tickets/tests.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/tickets/tests.py) | 4, 5, 15 |
| [`tickets/views.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/tickets/views.py) | 2, 3, 4, 5, 6, 7, 8, 9, 12 |
