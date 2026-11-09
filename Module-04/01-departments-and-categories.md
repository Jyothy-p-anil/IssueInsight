# Module 04 — Master Data Management

## Department and category reference data

### Before we begin

A complaint category helps decide which support team receives a ticket; departments also constrain Support Staff access.

### What we worked on

A Category links to a Department. A new complaint selects a Category, and the server derives its department unless routing is left pending.

### Picture it this way

Follow one real request or data change through the functions shown below. Notice which fields come from the user and which are set by the server.

### Important Django concepts

`reference data`, `ForeignKey`, `ModelAdmin`, `routing`, `data validation`.

### Actual code from the committed project

Source revision: [`02a68f05b7ab`](https://github.com/Jyothy-p-anil/IssueInsight/commit/02a68f05b7ab83749791ab60b9cf2245a201c26d) on `master`. The excerpts are current code, not invented historical versions.

#### `tickets/models.py` → `Department`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/02a68f05b7ab83749791ab60b9cf2245a201c26d/tickets/models.py#L7-L11)

```python
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
```

#### `tickets/models.py` → `Category`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/02a68f05b7ab83749791ab60b9cf2245a201c26d/tickets/models.py#L14-L36)

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

#### `tickets/admin.py` → `CategoryAdmin`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/02a68f05b7ab83749791ab60b9cf2245a201c26d/tickets/admin.py#L10-L19)

```python
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ('name', 'division', 'department')

    list_filter = ('division', 'department')

    search_fields = ('name',)

    ordering = ('division', 'name')
```

#### `tickets/management/commands/seed_initial_data.py` → `Command`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/02a68f05b7ab83749791ab60b9cf2245a201c26d/tickets/management/commands/seed_initial_data.py#L6-L63)

```python
class Command(BaseCommand):
    help = 'Create initial IssueInsight data'

    def handle(self, *args, **kwargs):

        departments = [
            'Internal IT Support',
            'Facilities Support',
            'Administration Support',
            'Product Support',
        ]

        for name in departments:
            Department.objects.get_or_create(name=name)

        categories = [
            ('employee', 'IT Issues', 'Internal IT Support'),
            ('employee', 'Facilities Issues', 'Facilities Support'),
            ('employee', 'Administration Issues', 'Administration Support'),
            ('employee', 'Other', None),

            ('customer', 'Login & Access', 'Product Support'),
            ('customer', 'Software Errors', 'Product Support'),
            ('customer', 'Performance Issues', 'Product Support'),
            ('customer', 'Data & Reports', 'Product Support'),
            ('customer', 'Billing, Account & Subscription', 'Product Support'),
            ('customer', 'Security & Privacy', 'Product Support'),
            ('customer', 'Setup & Integration', 'Product Support'),
            ('customer', 'Other', None),
        ]

        for division, name, department_name in categories:
            department = None

            if department_name:
                department = Department.objects.get(
                    name=department_name
                )

            Category.objects.get_or_create(
                name=name,
                division=division,
                defaults={'department': department}
            )

        products = ['PayrollPro', 'InvoiceApp', 'TaskFlow']

        for name in products:
            Product.objects.get_or_create(
                name=name,
                defaults={'is_active': True}
            )

        self.stdout.write(
            self.style.SUCCESS(
                'Initial data setup completed successfully!'
            )
        )
```

**Verified references in this chapter:** 4/4.

### Related development commits

- [b5f9735905](https://github.com/Jyothy-p-anil/IssueInsight/commit/b5f973590511d5365b60f0504a03e9db45c9afea) — docs: record initial support departments (2026-11-04)
- [3c0363e0ad](https://github.com/Jyothy-p-anil/IssueInsight/commit/3c0363e0ad78b2dcf7f2dde61001595e46240a51) — feat: create complaint category model (2026-11-04)
- [0fce6059da](https://github.com/Jyothy-p-anil/IssueInsight/commit/0fce6059da2d94006e4d4b83936acb9a66b4c266) — feat: improve category admin display (2026-11-04)

*These links show historical changes. A commit may touch several modules; inspect its diff before attributing every edit to this chapter.*

### How we checked it

The source code and test definitions were inspected from Git. **This journal generator does not run Django tests** and cannot prove that every workflow works.

### Explain it independently

1. What existed before this feature?
2. Which file handles the incoming request or data?
3. Which checks protect the operation?
4. How do the results reach the next page or database record?

### Teacher / interview questions

- Why does a Category point to a Department?
- What happens when a category has no department?

### Connections

Back to [this module's chapter list](README.md), or view the [complete source module map](../MODULE_INDEX.md).
