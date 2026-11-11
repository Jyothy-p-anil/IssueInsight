<!-- Snapshot of committed master/MODULE_INDEX.md. The original lives on master. -->

# IssueInsight — Module Index

**Repository:** https://github.com/Jyothy-p-anil/IssueInsight  
**Branch:** `master`  
**Purpose:** Connect the master development checklist and study lessons to actual source code and Git history.

This index documents *where* each module's code lives. It does **not** replace the master checklist, change old commits, or imply that every file belongs to only one module. A file can be used by multiple modules. Update this index after implementing and verifying each module.

## How to study a module

1. Read the module row below and inspect its named functions/classes, not just the entire file.
2. Look up the relevant commits on GitHub. A commit may contain work from more than one module.
3. To see edits to a shared file: `git log --oneline -- tickets/views.py`.
4. To inspect one commit's changes to that file: `git show <commit-id> -- tickets/views.py`.
5. Consult `NOTES.md` for step-by-step development history and the master checklist for completion criteria.

## Module map

**Status meaning:** *Core complete* = the existing module's foundational scope has been implemented; *Partial* = some features exist but the approved module scope is not finished; *Not started* = no corresponding full feature implementation identified in the current repository. Progress is not recalculated here.

| Module | Scope | Status | Relevant code locations | Example historical commits |
|---|---|---|---|---|
| **1. Project Setup and Database** | Django workspace, apps, custom User, initial complaint models and migrations, starter data | Core complete; later model extensions ongoing | `manage.py`; `config/settings.py`; `accounts/models.py` (`User`); `tickets/models.py` (`Department`, `Category`, `Product`, `Ticket`); `tickets/migrations/`; `tickets/management/commands/seed_initial_data.py` | `db45fe466a`, `2720a9891b`, `3c0363e0ad`, `2f8f46bb3d`, `cbb1fc6d5f`, `3d0a5b9b34` |
| **2. Initial UI and Authentication** | Base interface, login/logout, customer registration, password reset, staff account setup/email, role navigation | Core complete | `templates/base.html`, `templates/home.html`, `templates/role_dashboard.html`, `templates/accounts/`; `static/css/style.css`; `accounts/forms.py` (`CustomerRegistrationForm`, `StaffAccountCreationForm`); `accounts/views.py` (`register`); `accounts/services.py`; `accounts/admin.py`; `config/urls.py` | `4b84801902`, `df8ffa579b`, `e1f48fd2b3`, `cd67bca6ac`, `e06f89c70f`, `716dfced43`, `e4f6c84546` |
| **3. Role-Based Permissions and Account Access** | Four-role access, protected views, account management permissions, ticket ownership, department isolation, security tests | Core complete for features implemented so far; extend tests as new features arrive | `accounts/decorators.py` (`role_required`); `accounts/models.py` (`User.role`, `department`); `accounts/views.py` (`manage_users`, `edit_user`, `change_user_status`); `tickets/views.py` (role-protected views); `accounts/tests.py` (`RolePermissionTests`); `accounts/test_module3_security.py` (`Module3SecurityTests`); `config/urls.py` | `1f8dd69227`, `2f17578632`, `6885ea66b8`, `ea64b763d1` |
| **4. Master Data Management** | Support departments, complaint categories, software products and their management | Complete for implemented scope: Department CRUD with safe deletion; Category CRUD, division and department mapping, Other protection; Product creation, editing and activation/deactivation; Admin-only permissions and tests | `tickets/models.py`; `tickets/forms.py` (`DepartmentForm`, `CategoryForm`, `ProductForm`); `tickets/views.py` (`manage_departments`, `edit_department`, `delete_department`, `manage_categories`, `edit_category`, `delete_category`, `manage_products`, `edit_product`, `toggle_product_status`); `tickets/admin.py`; `tickets/tests.py`; `templates/tickets/admin_*.html`; `templates/base.html`; `config/urls.py`; `tickets/management/commands/seed_initial_data.py` | `ec8b47f32d`, `0fce6059da`, `3d0a5b9b34`, `5e16387502`, `ead7bbac4a`, `5d8f56c9`, `06ddc706`, `7e3f46e319`, `0cd5801c7083` |
| **5. Employee Complaint Submission** | Employee workplace complaint form, validation, automatic department routing, Other manual routing, and submission |Submission implemented; Complete — all 16 checklist requirements (71–86) verified in Step 59; 65 regression tests passed.| `tickets/forms.py` (`EmployeeComplaintForm`); `tickets/views.py` (`submit_employee_complaint`, `employee_my_tickets`); `tickets/models.py` (`Ticket`, `Category`, `Department`); `tickets/tests.py` (`EmployeeComplaintSubmissionTests`); `templates/tickets/employee_complaint_form.html`, `templates/tickets/employee_my_tickets.html`; `config/urls.py` | `734a0417b0` |
|**6. Customer Complaint Submission** | Customer form, product selection, unlisted products, category validation and routing | Complete — all 16 checklist requirements (87–102) verified in Step 62; 84 regression tests passed. | `tickets/forms.py` (`CustomerComplaintForm`); `tickets/views.py` (`submit_customer_complaint`, `customer_my_tickets`); `tickets/models.py` (`Ticket`, `Product`, `Category`); `tickets/services/category_suggestions.py`; `tickets/tests.py` (`CustomerComplaintSubmissionTests`); `templates/tickets/customer_complaint_form.html`; `templates/tickets/customer_my_tickets.html`; `config/urls.py` | `67d4f75d55`, `e92989cc689b`, `4f1b228d2471` |
| **7. My Tickets and Complaint Details** | Reporter ticket lists and details; later status, confirmation and reopening interactions | In progress — Step 64 My Tickets status filtering and privacy verified; 97 tests passed; final checklist review pending. | `tickets/views.py` (`employee_my_tickets`, `customer_my_tickets`, `ticket_detail`); `templates/tickets/employee_my_tickets.html`, `customer_my_tickets.html`, `ticket_detail.html` | `734a0417b0`, `67d4f75d55` (shared development history) |
| **8. Complaint Routing and Support Workflows** | Department queue, assigned tickets, claiming, Admin manual routing,Admin All Complaints; later resolution/escalation rules | Partial | `tickets/views.py` (`support_department_queue`, `support_assigned_tickets`, `support_ticket_detail`, `claim_support_ticket`, `admin_pending_routing`, `admin_route_ticket`); `tickets/forms.py` (`ManualRoutingForm`); support/routing templates | `2088cf9734`, `fbf064e527`, `cb2cc89fb9` |
| **9. Communication and Notifications** | Public ticket replies, internal support notes, first-response recording and notifications | Partial; first-response tracking needs final verification | `tickets/models.py` (`TicketMessage`, `Ticket.first_response_at`); `tickets/forms.py` (`TicketMessageForm`, `SupportMessageForm`); `tickets/views.py` (`add_reporter_message`, `add_support_message`); `tickets/migrations/0005_ticket_first_response_at_ticketmessage.py` | `cb2cc89fb9` (combined change); account-related email commits also appear under Module 2 |
| **10. Shared Issues, Recurring Complaints and Incidents** | Shared workplace issue verification and recurring-issue handling | Not started | Implement in the approved future module; no new models/statuses assumed | — |
| **11. AI and Intelligent Complaint Analysis** | Classification, urgency detection, recurring-issue analysis | Not started | Implement in the approved future module | — |
| **12. Dashboards and Analytics** | Role-specific reporting and analytics | Partial: initial dashboard destinations exist; analytics not yet implemented | `tickets/views.py` (`employee_dashboard`, `customer_dashboard`, `support_dashboard`, `admin_dashboard`, `dashboard_redirect`); `templates/role_dashboard.html` | `2f17578632`, `e4f6c84546` |
| **13. Search, Filtering and Reporting** | Ticket search, filters and reporting | Partial: account-management search/filtering exists | `accounts/views.py` (`manage_users` search/filtering); `templates/accounts/manage_users.html`; ticket reporting to be implemented | `b585f71486` |
| **14. User Interface Completion** | Consistent, complete role-based pages and responsive styling | Partial | `templates/base.html`; `templates/tickets/`; `templates/accounts/`; `static/css/style.css` | `4b84801902`, `067cc07d58`, `716dfced43` |
| **15. Integration Testing, Final Delivery and Documentation** | System-wide tests, final verification, delivery and documentation | Partial | `accounts/tests.py`; `accounts/test_module3_security.py`; `tickets/tests.py`; `NOTES.md`; `requirements.txt` | `6885ea66b8`, `ea64b763d1` |

## Module 3 — Permission matrix (current implemented behavior)

| Action | Employee | Customer | Support Staff | Admin |
|---|---|---|---|---|
| Submit a complaint in own division | Yes | Yes | No | No |
| View/reply to own ticket | Yes | Yes | No | No |
| View department queue and claim an unassigned ticket | No | No | Yes, own department | No |
| Reply or add internal notes on support tickets | No | No | Yes, when assigned | No |
| Manage user accounts | No | No | No | Yes |
| Route a pending/unassigned complaint | No | No | No | Yes |

Superusers have elevated access through the role decorator, but individual views may still apply object-level restrictions. The test coverage is for existing workflows, not every future feature.

## Updating this index from Module 4 onward

After each verified feature or module:

1. Add new functions/classes and file paths to its row.
2. Add the commit ID(s) that introduced the feature; keep old IDs.
3. Record whether the approved checklist is *Partial* or *Complete*. Do not mark a module complete merely because some of its functions exist.
4. Preserve `NOTES.md` as the detailed chronological development journal.
5. Use focused commit messages, for example `feat(module-4): add category management` or `test(module-4): verify admin-only master data edits`.

**Important:** Historical commits remain unchanged. A commit can serve as evidence for several modules, and a shared file can continue to evolve normally.
