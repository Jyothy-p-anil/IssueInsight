# IssueInsight

**Intelligent Complaint Analysis & Resolution Tracking System**

IssueInsight is a Django-based web application for managing employee workplace complaints and customer software complaints within a company.

It combines role-based complaint management, support workflows, AI-assisted categorization, notifications, incident tracking and reporting.

## Technology Stack

- Python 3.14
- Django 6.1.2
- SQLite
- HTML, CSS and Bootstrap
- Scikit-learn and Sentence Transformers

## User Roles

| Role | Responsibilities |
|---|---|
| Employee | Submit workplace complaints, track progress, communicate with support and confirm resolutions |
| Customer | Submit software complaints, track progress, communicate with support and confirm resolutions |
| Support Staff | Claim assigned-department complaints, respond, escalate, resolve and manage incidents |
| Admin | Manage users, departments, categories, products, complaint routing, announcements and reports |

## Main Features

- Secure login, registration and password recovery
- Role-based dashboards and permissions
- Employee and Customer complaint submission
- AI-assisted complaint categorization
- Complaint urgency and recurring-issue analysis
- Automatic and manual department routing
- Support Staff assignment and escalation
- Public conversations and private internal notes
- Resolution confirmation and complaint reopening
- Notifications and activity history
- Incident management
- Admin and department-level reports
- CSV and PDF report exports

## Installation

Clone the repository:

```bash
git clone https://github.com/Jyothy-p-anil/IssueInsight.git
cd IssueInsight
```

Create and activate a virtual environment on Windows:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Create `config/local_secret.py` with the following variables:

```python
SECRET_KEY = "your-local-django-secret-key"
EMAIL_HOST_USER = "your-gmail-address@gmail.com"
EMAIL_HOST_PASSWORD = "your-gmail-app-password"
```

Use your own credentials. Never commit this file to GitHub.

Apply database migrations:

```powershell
python manage.py migrate
```

Create an administrator account if needed:

```powershell
python manage.py createsuperuser
```

Start the development server:

```powershell
python manage.py runserver
```

Open http://127.0.0.1:8000/.

## Testing

Run the Django system check:

```powershell
python manage.py check
```

Run the automated test suite:

```powershell
python manage.py test
```

Check for pending migrations:

```powershell
python manage.py makemigrations --check --dry-run
```

**Latest verified regression result:** 393 tests passed.

Manual integration testing covered Employee and Customer complaint lifecycles, resolution confirmation, reopening, ticket privacy, internal-note privacy and Admin report exports.

## Project Structure

- `accounts/` — Authentication, user management and role permissions
- `tickets/` — Complaints, support workflows, AI features, incidents and reports
- `config/` — Django settings and URL configuration
- `templates/` — User interface templates
- `static/` — Shared CSS and other static resources
- `NOTES.md` — Development history and implementation notes
- `MODULE_INDEX.md` — Module-wise source-code reference

## Development Limitations

This is an academic development project configured for local execution.

- SQLite is used for local data storage.
- `DEBUG = True` is enabled for development.
- Production deployment and infrastructure hardening are not included.
- Email delivery requires valid SMTP credentials and connectivity.
- AI features depend on the configured local dependencies and available resources.

## Repository

https://github.com/Jyothy-p-anil/IssueInsight


## Module 15 — Integration Testing and Final Delivery

### Automated Verification
- Django system check completed.
- Full regression suite: 393 tests passed.
- No pending model migrations.

### Manual Integration Testing
- Employee complaint submission, assignment, acknowledgement, resolution and closure — Passed.
- Customer complaint submission, assignment, acknowledgement, resolution and closure — Passed.
- Reporter reopening of a resolved complaint — Passed.
- Reporter ticket privacy — Passed.
- Support Staff internal-note privacy — Passed.
- Admin reporting and CSV/PDF exports — Passed.

### Documentation
- Created `README.md` with project overview, features, installation, configuration, testing and limitations.
- Existing `requirements.txt` and `.gitignore` retained.

### Status
Integration testing and README documentation completed. Final delivery verification pending.