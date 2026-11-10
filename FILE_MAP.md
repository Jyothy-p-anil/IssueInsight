# Shared file-to-module guide

A file can serve several modules. The `SOURCE_MAPPING.csv` file identifies functions/classes more precisely.

| File | Modules |
|---|---|
| [`accounts/admin.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/accounts/admin.py) | 1 |
| [`accounts/apps.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/accounts/apps.py) | 1 |
| [`accounts/decorators.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/accounts/decorators.py) | 3 |
| [`accounts/forms.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/accounts/forms.py) | 2 |
| [`accounts/models.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/accounts/models.py) | 1 |
| [`accounts/services.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/accounts/services.py) | 2 |
| [`accounts/test_module3_security.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/accounts/test_module3_security.py) | 3, 15 |
| [`accounts/tests.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/accounts/tests.py) | 3, 15 |
| [`accounts/views.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/accounts/views.py) | 2, 3, 13 |
| [`config/settings.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/config/settings.py) | 1 |
| [`config/urls.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/config/urls.py) | 2 |
| [`manage.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/manage.py) | 1 |
| [`static/css/style.css`](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/static/css/style.css) | 2, 14 |
| [`templates/accounts/manage_users.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/templates/accounts/manage_users.html) | 13 |
| [`templates/base.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/templates/base.html) | 2, 3, 4, 14 |
| [`templates/home.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/templates/home.html) | 2 |
| [`templates/role_dashboard.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/templates/role_dashboard.html) | 12, 14 |
| [`templates/tickets/admin_categories.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/templates/tickets/admin_categories.html) | 4 |
| [`templates/tickets/admin_category_confirm_delete.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/templates/tickets/admin_category_confirm_delete.html) | 4 |
| [`templates/tickets/admin_category_edit.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/templates/tickets/admin_category_edit.html) | 4 |
| [`templates/tickets/admin_department_confirm_delete.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/templates/tickets/admin_department_confirm_delete.html) | 4 |
| [`templates/tickets/admin_department_edit.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/templates/tickets/admin_department_edit.html) | 4 |
| [`templates/tickets/admin_departments.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/templates/tickets/admin_departments.html) | 4 |
| [`templates/tickets/admin_pending_routing.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/templates/tickets/admin_pending_routing.html) | 8 |
| [`templates/tickets/admin_product_edit.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/templates/tickets/admin_product_edit.html) | 4 |
| [`templates/tickets/admin_products.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/templates/tickets/admin_products.html) | 4 |
| [`templates/tickets/customer_complaint_form.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/templates/tickets/customer_complaint_form.html) | 6 |
| [`templates/tickets/customer_my_tickets.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/templates/tickets/customer_my_tickets.html) | 6 |
| [`templates/tickets/employee_complaint_form.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/templates/tickets/employee_complaint_form.html) | 5 |
| [`templates/tickets/employee_my_tickets.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/templates/tickets/employee_my_tickets.html) | 5 |
| [`templates/tickets/support_ticket_detail.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/templates/tickets/support_ticket_detail.html) | 3 |
| [`templates/tickets/support_ticket_list.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/templates/tickets/support_ticket_list.html) | 8 |
| [`templates/tickets/ticket_detail.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/templates/tickets/ticket_detail.html) | 3, 7 |
| [`tickets/admin.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/tickets/admin.py) | 1, 4 |
| [`tickets/apps.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/tickets/apps.py) | 1 |
| [`tickets/forms.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/tickets/forms.py) | 3, 4, 5, 6, 8, 9 |
| [`tickets/management/commands/seed_initial_data.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/tickets/management/commands/seed_initial_data.py) | 1, 4 |
| [`tickets/models.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/tickets/models.py) | 1, 3, 4, 9 |
| [`tickets/tests.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/tickets/tests.py) | 4, 15 |
| [`tickets/views.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/tickets/views.py) | 2, 3, 4, 5, 6, 7, 8, 9, 12 |
