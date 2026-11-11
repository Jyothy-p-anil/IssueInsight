# Shared file-to-module guide

A file can serve several modules. The `SOURCE_MAPPING.csv` file identifies functions/classes more precisely.

| File | Modules |
|---|---|
| [`accounts/admin.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/accounts/admin.py) | 1 |
| [`accounts/apps.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/accounts/apps.py) | 1 |
| [`accounts/decorators.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/accounts/decorators.py) | 3 |
| [`accounts/forms.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/accounts/forms.py) | 2 |
| [`accounts/models.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/accounts/models.py) | 1 |
| [`accounts/services.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/accounts/services.py) | 2 |
| [`accounts/test_module3_security.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/accounts/test_module3_security.py) | 3, 15 |
| [`accounts/tests.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/accounts/tests.py) | 3, 15 |
| [`accounts/views.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/accounts/views.py) | 2, 3, 13 |
| [`config/settings.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/config/settings.py) | 1 |
| [`config/urls.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/config/urls.py) | 2 |
| [`manage.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/manage.py) | 1 |
| [`static/css/style.css`](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/static/css/style.css) | 2, 14 |
| [`templates/accounts/manage_users.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/templates/accounts/manage_users.html) | 13 |
| [`templates/base.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/templates/base.html) | 2, 3, 4, 14 |
| [`templates/home.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/templates/home.html) | 2 |
| [`templates/role_dashboard.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/templates/role_dashboard.html) | 12, 14 |
| [`templates/tickets/_reporter_ticket_filters.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/templates/tickets/_reporter_ticket_filters.html) | 7 |
| [`templates/tickets/admin_categories.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/templates/tickets/admin_categories.html) | 4 |
| [`templates/tickets/admin_category_confirm_delete.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/templates/tickets/admin_category_confirm_delete.html) | 4 |
| [`templates/tickets/admin_category_edit.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/templates/tickets/admin_category_edit.html) | 4 |
| [`templates/tickets/admin_department_confirm_delete.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/templates/tickets/admin_department_confirm_delete.html) | 4 |
| [`templates/tickets/admin_department_edit.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/templates/tickets/admin_department_edit.html) | 4 |
| [`templates/tickets/admin_departments.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/templates/tickets/admin_departments.html) | 4 |
| [`templates/tickets/admin_pending_routing.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/templates/tickets/admin_pending_routing.html) | 8 |
| [`templates/tickets/admin_product_edit.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/templates/tickets/admin_product_edit.html) | 4 |
| [`templates/tickets/admin_products.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/templates/tickets/admin_products.html) | 4 |
| [`templates/tickets/customer_complaint_form.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/templates/tickets/customer_complaint_form.html) | 6 |
| [`templates/tickets/customer_my_tickets.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/templates/tickets/customer_my_tickets.html) | 6, 7 |
| [`templates/tickets/employee_complaint_form.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/templates/tickets/employee_complaint_form.html) | 5 |
| [`templates/tickets/employee_my_tickets.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/templates/tickets/employee_my_tickets.html) | 5, 7 |
| [`templates/tickets/support_ticket_detail.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/templates/tickets/support_ticket_detail.html) | 3 |
| [`templates/tickets/support_ticket_list.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/templates/tickets/support_ticket_list.html) | 8 |
| [`templates/tickets/ticket_detail.html`](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/templates/tickets/ticket_detail.html) | 3, 7 |
| [`tickets/admin.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/tickets/admin.py) | 1, 4 |
| [`tickets/apps.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/tickets/apps.py) | 1 |
| [`tickets/forms.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/tickets/forms.py) | 3, 4, 5, 6, 8, 9 |
| [`tickets/management/commands/seed_initial_data.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/tickets/management/commands/seed_initial_data.py) | 1, 4 |
| [`tickets/migrations/0006_ticket_updated_at.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/tickets/migrations/0006_ticket_updated_at.py) | 7 |
| [`tickets/models.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/tickets/models.py) | 1, 3, 4, 9 |
| [`tickets/services/category_suggestions.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/tickets/services/category_suggestions.py) | 5 |
| [`tickets/tests.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/tickets/tests.py) | 4, 5, 6, 7, 15 |
| [`tickets/views.py`](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/tickets/views.py) | 2, 3, 4, 5, 6, 7, 8, 9, 12 |
