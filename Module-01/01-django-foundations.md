# Module 01 — Project Setup and Database

## Django project and application setup

### Before we begin

IssueInsight needs a Django entry point and separate apps before it can serve pages or save data.

### What we worked on

The manage.py command loads Django settings; Django finds the installed apps, URL routes and database configuration.

### Picture it this way

Follow one real request or data change through the functions shown below. Notice which fields come from the user and which are set by the server.

### Important Django concepts

`project vs app`, `settings`, `URL routing`, `virtual environment`.

### Actual code from the committed project

Source revision: [`02a68f05b7ab`](https://github.com/Jyothy-p-anil/IssueInsight/commit/02a68f05b7ab83749791ab60b9cf2245a201c26d) on `master`. The excerpts are current code, not invented historical versions.

#### `manage.py`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/02a68f05b7ab83749791ab60b9cf2245a201c26d/manage.py#L1-L22)

```python
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
```

#### `accounts/apps.py`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/02a68f05b7ab83749791ab60b9cf2245a201c26d/accounts/apps.py#L1-L5)

```python
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'
```

#### `tickets/apps.py`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/02a68f05b7ab83749791ab60b9cf2245a201c26d/tickets/apps.py#L1-L5)

```python
from django.apps import AppConfig


class TicketsConfig(AppConfig):
    name = 'tickets'
```

#### `config/settings.py` → `AUTH_USER_MODEL`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/02a68f05b7ab83749791ab60b9cf2245a201c26d/config/settings.py#L155)

```python
AUTH_USER_MODEL = 'accounts.User'
```

#### `config/settings.py` → `INSTALLED_APPS`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/02a68f05b7ab83749791ab60b9cf2245a201c26d/config/settings.py#L32-L41)

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tickets',
    "accounts",
]
```

**Verified references in this chapter:** 5/5.

### Related development commits

- [3550479d2a](https://github.com/Jyothy-p-anil/IssueInsight/commit/3550479d2a7bd785532f8dda48de80a64ed1a92d) — chore: initialize IssueInsight workspace (2026-11-03)
- [db45fe466a](https://github.com/Jyothy-p-anil/IssueInsight/commit/db45fe466abef90d2bb887cc57fcc5e75ef630dc) — chore: complete secure Django project setup (2026-11-04)

*These links show historical changes. A commit may touch several modules; inspect its diff before attributing every edit to this chapter.*

### How we checked it

The source code and test definitions were inspected from Git. **This journal generator does not run Django tests** and cannot prove that every workflow works.

### Explain it independently

1. What existed before this feature?
2. Which file handles the incoming request or data?
3. Which checks protect the operation?
4. How do the results reach the next page or database record?

### Teacher / interview questions

- What is the difference between a Django project and a Django app?
- What does manage.py do?

### Connections

Back to [this module's chapter list](README.md), or view the [complete source module map](../MODULE_INDEX.md).
