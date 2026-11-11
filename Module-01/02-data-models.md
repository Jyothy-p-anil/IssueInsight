# Module 01 — Project Setup and Database

## Users, departments, categories, products and tickets

### Before we begin

The application needs a database model for people, complaints and the departments responsible for handling them.

### What we worked on

User records identify reporters and support staff. Category and department determine routing. Tickets store the reporter, complaint information, assignment and status.

### Picture it this way

Follow one real request or data change through the functions shown below. Notice which fields come from the user and which are set by the server.

### Important Django concepts

`AbstractUser`, `model`, `ForeignKey`, `choices`, `on_delete`, `nullable fields`.

### Actual code from the committed project

Source revision: [`a9a40f739d52`](https://github.com/Jyothy-p-anil/IssueInsight/commit/a9a40f739d52f68c0d05b37955d53ea1baacecf8) on `master`. The excerpts are current code, not invented historical versions.

#### `accounts/models.py` → `User`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/a9a40f739d52f68c0d05b37955d53ea1baacecf8/accounts/models.py#L5-L27)

```python
class User(AbstractUser):

    ROLE_CHOICES = [
        ('employee', 'Employee'),
        ('customer', 'Customer'),
        ('support', 'Support Staff'),
        ('admin', 'Admin'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='customer'
    )

    
    department = models.ForeignKey(
        'tickets.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='staff_members'
    )
```

#### `tickets/models.py` → `Department`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/a9a40f739d52f68c0d05b37955d53ea1baacecf8/tickets/models.py#L7-L11)

```python
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
```

#### `tickets/models.py` → `Category`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/a9a40f739d52f68c0d05b37955d53ea1baacecf8/tickets/models.py#L14-L36)

```python
class Category(models.Model):

    DIVISION_CHOICES = [
        ('employee', 'Employee'),
        ('customer', 'Customer'),
    ]

    name = models.CharField(max_length=100)

    division = models.CharField(
        max_length=10,
        choices=DIVISION_CHOICES
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name
```

#### `tickets/models.py` → `Product`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/a9a40f739d52f68c0d05b37955d53ea1baacecf8/tickets/models.py#L39-L49)

```python
class Product(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
```

#### `tickets/models.py` → `Ticket`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/a9a40f739d52f68c0d05b37955d53ea1baacecf8/tickets/models.py#L53-L134)

```python
class Ticket(models.Model):

    DIVISION_CHOICES = [
        ('employee', 'Employee'),
        ('customer', 'Customer'),
    ]

    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
        ('reopened', 'Reopened'),
    ]

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='reported_tickets'
    )

    division = models.CharField(
        max_length=10,
        choices=DIVISION_CHOICES
    )

    title = models.CharField(max_length=200)
    description = models.TextField()

    floor = models.CharField(
        max_length=30,
        blank=True
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    other_product_name = models.CharField(
        max_length=100,
        blank=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tickets'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='submitted'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    first_response_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title
```

**Verified references in this chapter:** 5/5.

### Related development commits

- [2720a9891b](https://github.com/Jyothy-p-anil/IssueInsight/commit/2720a9891b3f806fb782c879b1e5e928815ede59) — feat: link support staff to departments (2026-11-04)
- [3c0363e0ad](https://github.com/Jyothy-p-anil/IssueInsight/commit/3c0363e0ad78b2dcf7f2dde61001595e46240a51) — feat: create complaint category model (2026-11-04)
- [2f8f46bb3d](https://github.com/Jyothy-p-anil/IssueInsight/commit/2f8f46bb3d1160f78902d8657b39d03452619968) — feat: create software product model (2026-11-04)
- [cbb1fc6d5f](https://github.com/Jyothy-p-anil/IssueInsight/commit/cbb1fc6d5fcf2fdbd36b452ccd79e9d489096da6) — feat: create complaint ticket model (2026-11-04)

*These links show historical changes. A commit may touch several modules; inspect its diff before attributing every edit to this chapter.*

### How we checked it

The source code and test definitions were inspected from Git. **This journal generator does not run Django tests** and cannot prove that every workflow works.

### Explain it independently

1. What existed before this feature?
2. Which file handles the incoming request or data?
3. Which checks protect the operation?
4. How do the results reach the next page or database record?

### Teacher / interview questions

- Why did we extend AbstractUser?
- What is the difference between reporter, department and assigned_to?

### Connections

Back to [this module's chapter list](README.md), or view the [complete source module map](../MODULE_INDEX.md).
