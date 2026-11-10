# Module 01 — Project Setup and Database

## Django Admin, migrations and starter records

### Before we begin

Before building custom management pages, administrators need a way to inspect tables and establish starter departments, categories and products.

### What we worked on

Models define tables, migrations record database changes, Django Admin manages records, and the seed command inserts initial reference data.

### Picture it this way

Follow one real request or data change through the functions shown below. Notice which fields come from the user and which are set by the server.

### Important Django concepts

`makemigrations`, `migrate`, `ModelAdmin`, `management command`, `idempotence`.

### Actual code from the committed project

Source revision: [`8aa5fec6ff3d`](https://github.com/Jyothy-p-anil/IssueInsight/commit/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a) on `master`. The excerpts are current code, not invented historical versions.

#### `tickets/admin.py` → `TicketAdmin`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/tickets/admin.py#L63-L88)

```python
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'reporter',
        'division',
        'category',
        'department',
        'status',
        'created_at',
    )

    list_filter = (
        'division',
        'status',
        'department',
    )

    search_fields = (
        'title',
        'description',
        'reporter__username',
    )

    ordering = ('-created_at',)
```

#### `tickets/admin.py` → `CategoryAdmin`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/tickets/admin.py#L28-L42)

```python
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ('name', 'division', 'department')

    list_filter = ('division', 'department')

    search_fields = ('name',)

    ordering = ('division', 'name')

    form = CategoryForm

    def has_delete_permission(self, request, obj=None):
        return False
```

#### `accounts/admin.py` → `CustomUserAdmin`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/accounts/admin.py#L20-L79)

```python
@admin.register(User)
class CustomUserAdmin(UserAdmin):

    add_form = StaffAccountCreationForm

    fieldsets = UserAdmin.fieldsets + (
        ('IssueInsight Details', {
            'fields': ('role', 'department')
        }),
    )

    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'department'),
        }),
    )

    
    list_display = (
        'username',
        'email',
        'role',
        'department',
        'is_active',
        'is_staff',
        'is_superuser',
    )

    list_filter = (
        'role',
        'department',
        'is_active',
        'is_staff',
    )



    

    def save_model(self, request, obj, form, change):
        previous_active = None

        if change:
            previous_active = User.objects.filter(
                pk=obj.pk
            ).values_list('is_active', flat=True).first()

        super().save_model(request, obj, form, change)



        if not change and obj.role in ('employee', 'support'):
            send_password_setup_email(request, obj)

            
        if change and previous_active is not None:
            if previous_active != obj.is_active:
                send_account_status_email(obj)
```

#### `tickets/management/commands/seed_initial_data.py` → `Command`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/tickets/management/commands/seed_initial_data.py#L6-L63)

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

- [ec8b47f32d](https://github.com/Jyothy-p-anil/IssueInsight/commit/ec8b47f32d9ff68c4a91d683dab119dbeae29a96) — feat: register ticket models in Django admin (2026-11-04)
- [0fce6059da](https://github.com/Jyothy-p-anil/IssueInsight/commit/0fce6059da2d94006e4d4b83936acb9a66b4c266) — feat: improve category admin display (2026-11-04)
- [9d821abe6e](https://github.com/Jyothy-p-anil/IssueInsight/commit/9d821abe6efbdc23d35683906578db85d442cdae) — feat: improve ticket admin list (2026-11-04)
- [3d0a5b9b34](https://github.com/Jyothy-p-anil/IssueInsight/commit/3d0a5b9b34dfcabe3ad1db732b6429b1b8a0feb6) — feat: add initial database seed command (2026-11-04)

*These links show historical changes. A commit may touch several modules; inspect its diff before attributing every edit to this chapter.*

### How we checked it

The source code and test definitions were inspected from Git. **This journal generator does not run Django tests** and cannot prove that every workflow works.

### Explain it independently

1. What existed before this feature?
2. Which file handles the incoming request or data?
3. Which checks protect the operation?
4. How do the results reach the next page or database record?

### Teacher / interview questions

- Why are migrations necessary?
- Why are initial data records separate from model definitions?

### Connections

Back to [this module's chapter list](README.md), or view the [complete source module map](../MODULE_INDEX.md).
