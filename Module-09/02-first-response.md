# Module 09 — Communication and Notifications

## First public Support Staff response

### Before we begin

Response time should be measured from an actual human public reply, not from ticket claiming or an internal note.

### What we worked on

A first public support message records first_response_at once. Internal notes leave it unchanged.

### Picture it this way

Follow one real request or data change through the functions shown below. Notice which fields come from the user and which are set by the server.

### Important Django concepts

`DateTimeField`, `transaction.atomic`, `conditional update`, `audit history`.

### Actual code from the committed project

Source revision: [`02a68f05b7ab`](https://github.com/Jyothy-p-anil/IssueInsight/commit/02a68f05b7ab83749791ab60b9cf2245a201c26d) on `master`. The excerpts are current code, not invented historical versions.

#### `tickets/models.py` → `Ticket`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/02a68f05b7ab83749791ab60b9cf2245a201c26d/tickets/models.py#L53-L134)

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

#### `tickets/views.py` → `add_support_message`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/02a68f05b7ab83749791ab60b9cf2245a201c26d/tickets/views.py#L423-L475)

```python
@role_required('support')
@require_POST
def add_support_message(request, ticket_id):

    ticket = get_object_or_404(
        Ticket,
        pk=ticket_id,
        department_id=request.user.department_id,
        assigned_to=request.user
    )

    if ticket.status not in ('in_progress', 'reopened'):
        messages.error(
            request,
            'Replies are not available for this ticket status.'
        )
        return redirect(
            'support_ticket_detail',
            ticket_id=ticket_id
        )

    form = SupportMessageForm(request.POST)

    if form.is_valid():

        with transaction.atomic():
            message = form.save(commit=False)
            message.ticket = ticket
            message.author = request.user
            message.save()

            # Record only the first PUBLIC Support Staff reply.
            if not message.is_internal:
                Ticket.objects.filter(
                    pk=ticket.pk,
                    first_response_at__isnull=True
                ).update(
                    first_response_at=message.created_at
                )

        messages.success(
            request,
            'Internal note saved.' if message.is_internal
            else 'Public reply sent successfully.'
        )

    else:
        messages.error(request, 'Please enter a valid message.')

    return redirect(
        'support_ticket_detail',
        ticket_id=ticket_id
    )
```

**Verified references in this chapter:** 2/2.

### Related development commits

- [cb2cc89fb9](https://github.com/Jyothy-p-anil/IssueInsight/commit/cb2cc89fb9d711535dadfebde08efc17c696aed5) — feat: add manual routing and ticket conversations (2026-11-08)

*These links show historical changes. A commit may touch several modules; inspect its diff before attributing every edit to this chapter.*

### How we checked it

The source code and test definitions were inspected from Git. **This journal generator does not run Django tests** and cannot prove that every workflow works.

### Explain it independently

1. What existed before this feature?
2. Which file handles the incoming request or data?
3. Which checks protect the operation?
4. How do the results reach the next page or database record?

### Teacher / interview questions

- Which event sets first_response_at?
- Why only set the timestamp if it was previously NULL?

### Connections

Back to [this module's chapter list](README.md), or view the [complete source module map](../MODULE_INDEX.md).
