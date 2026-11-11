# Module 09 — Communication and Notifications

## Public replies and internal support notes

### Before we begin

Reporters and their assigned support staff need a visible communication history without exposing private operational notes.

### What we worked on

TicketMessage stores author, ticket, message and internal flag. Reporter replies are always public; only assigned support may add internal notes.

### Picture it this way

Follow one real request or data change through the functions shown below. Notice which fields come from the user and which are set by the server.

### Important Django concepts

`related_name`, `form validation`, `object authorization`, `internal vs public message`.

### Actual code from the committed project

Source revision: [`4c179f64e177`](https://github.com/Jyothy-p-anil/IssueInsight/commit/4c179f64e177a16ce2f536aa4b8c025639566ab9) on `master`. The excerpts are current code, not invented historical versions.

#### `tickets/models.py` → `TicketMessage`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/4c179f64e177a16ce2f536aa4b8c025639566ab9/tickets/models.py#L137-L161)

```python
class TicketMessage(models.Model):

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='ticket_messages'
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='written_ticket_messages'
    )

    body = models.TextField()

    is_internal = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at', 'id']

    def __str__(self):
        return f'Message #{self.pk} on Ticket #{self.ticket_id}'
```

#### `tickets/forms.py` → `TicketMessageForm`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/4c179f64e177a16ce2f536aa4b8c025639566ab9/tickets/forms.py#L130-L142)

```python
class TicketMessageForm(forms.ModelForm):

    class Meta:
        model = TicketMessage
        fields = ('body',)

        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your message...'
            })
        }
```

#### `tickets/forms.py` → `SupportMessageForm`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/4c179f64e177a16ce2f536aa4b8c025639566ab9/tickets/forms.py#L145-L159)

```python
class SupportMessageForm(TicketMessageForm):

    class Meta(TicketMessageForm.Meta):
        fields = ('body', 'is_internal')

        widgets = {
            **TicketMessageForm.Meta.widgets,
            'is_internal': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

        labels = {
            'is_internal': 'Internal note (hidden from reporter)'
        }
```

#### `tickets/views.py` → `add_reporter_message`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/4c179f64e177a16ce2f536aa4b8c025639566ab9/tickets/views.py#L422-L455)

```python
@role_required('employee', 'customer')
@require_POST
def add_reporter_message(request, ticket_id):

    ticket = get_object_or_404(
        Ticket,
        pk=ticket_id,
        reporter=request.user
    )

    if ticket.status not in (
        'submitted', 'in_progress', 'reopened'
    ):
        messages.error(
            request,
            'Replies are not available for this ticket status.'
        )
        return redirect('ticket_detail', ticket_id=ticket_id)

    form = TicketMessageForm(request.POST)

    if form.is_valid():
        message = form.save(commit=False)
        message.ticket = ticket
        message.author = request.user
        message.is_internal = False
        message.save()

        messages.success(request, 'Message sent successfully.')

    else:
        messages.error(request, 'Please enter a valid message.')

    return redirect('ticket_detail', ticket_id=ticket_id)
```

#### `tickets/views.py` → `add_support_message`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/4c179f64e177a16ce2f536aa4b8c025639566ab9/tickets/views.py#L460-L512)

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

**Verified references in this chapter:** 5/5.

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

- Who can create an internal note?
- Where is the reporter prevented from marking a message internal?

### Connections

Back to [this module's chapter list](README.md), or view the [complete source module map](../MODULE_INDEX.md).
