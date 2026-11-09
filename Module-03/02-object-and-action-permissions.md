# Module 03 — Role-Based Permissions and Account Access

## Ticket ownership, department isolation and Admin actions

### Before we begin

Correct role alone is insufficient: a user must not access another person's ticket or another department's work.

### What we worked on

Views restrict database queries by reporter, department or assigned_to. Sensitive changes use server-side validation and POST where appropriate.

### Picture it this way

Follow one real request or data change through the functions shown below. Notice which fields come from the user and which are set by the server.

### Important Django concepts

`get_object_or_404`, `queryset filtering`, `authorization`, `POST`, `race-condition protection`.

### Actual code from the committed project

Source revision: [`02a68f05b7ab`](https://github.com/Jyothy-p-anil/IssueInsight/commit/02a68f05b7ab83749791ab60b9cf2245a201c26d) on `master`. The excerpts are current code, not invented historical versions.

#### `tickets/views.py` → `ticket_detail`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/02a68f05b7ab83749791ab60b9cf2245a201c26d/tickets/views.py#L177-L210)

```python
@role_required('employee', 'customer')
def ticket_detail(request, ticket_id):

    ticket = get_object_or_404(
        Ticket.objects.select_related(
            'reporter',
            'category',
            'department',
            'product',
            'assigned_to'
        ),
        pk=ticket_id,
        reporter=request.user
    )

    
    conversation = ticket.ticket_messages.filter(
        is_internal=False
    ).select_related('author')

    can_reply = ticket.status in (
        'submitted', 'in_progress', 'reopened'
    )

    return render(
        request,
        'tickets/ticket_detail.html',
        {
            'ticket': ticket,
            'conversation': conversation,
            'reply_form': TicketMessageForm(),
            'can_reply': can_reply,
        }
    )
```

#### `tickets/views.py` → `support_ticket_detail`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/02a68f05b7ab83749791ab60b9cf2245a201c26d/tickets/views.py#L281-L328)

```python
@role_required('support')
def support_ticket_detail(request, ticket_id):

    if not request.user.department_id:
        messages.warning(
            request,
            'Your account has no support department assigned.'
        )
        return redirect('support_dashboard')

    ticket = get_object_or_404(
        Ticket.objects.select_related(
            'reporter',
            'category',
            'department',
            'product',
            'assigned_to'
        ),
        pk=ticket_id,
        department_id=request.user.department_id
    )

    can_claim = (
        ticket.assigned_to_id is None
        and ticket.status in ('submitted', 'reopened')
    )

    
    conversation = ticket.ticket_messages.select_related(
        'author'
    )

    can_reply = (
        ticket.assigned_to_id == request.user.id
        and ticket.status in ('in_progress', 'reopened')
    )

    return render(
        request,
        'tickets/support_ticket_detail.html',
        {
            'ticket': ticket,
            'can_claim': can_claim,
            'conversation': conversation,
            'reply_form': SupportMessageForm(),
            'can_reply': can_reply,
        }
    )
```

#### `tickets/views.py` → `claim_support_ticket`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/02a68f05b7ab83749791ab60b9cf2245a201c26d/tickets/views.py#L334-L380)

```python
@role_required('support')
@require_POST
def claim_support_ticket(request, ticket_id):

    if not request.user.department_id:
        messages.error(
            request,
            'Your account has no support department assigned.'
        )
        return redirect('support_dashboard')

    # Conditional update prevents two staff members
    # from successfully claiming the same ticket.

    updated = Ticket.objects.filter(
        pk=ticket_id,
        department_id=request.user.department_id,
        assigned_to__isnull=True,
        status__in=['submitted', 'reopened']
    ).update(
        assigned_to=request.user,
        status='in_progress'
    )

    if updated:
        messages.success(
            request,
            f'Ticket #{ticket_id} assigned to you.'
        )
        return redirect(
            'support_ticket_detail',
            ticket_id=ticket_id
        )

    # Do not reveal tickets from other departments.
    get_object_or_404(
        Ticket,
        pk=ticket_id,
        department_id=request.user.department_id
    )

    messages.warning(
        request,
        'This ticket is already assigned or cannot be claimed.'
    )

    return redirect('support_department_queue')
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

#### `accounts/views.py` → `manage_users`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/02a68f05b7ab83749791ab60b9cf2245a201c26d/accounts/views.py#L75-L118)

```python
@role_required('admin')
def manage_users(request):

    search = request.GET.get('search', '').strip()
    role = request.GET.get('role', '')
    department = request.GET.get('department', '')
    status = request.GET.get('status', '')

    users = User.objects.filter(
        role__in=['employee', 'customer', 'support'],
        is_superuser=False
    ).select_related('department')

    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search)
        )

    if role in ['employee', 'customer', 'support']:
        users = users.filter(role=role)

    if department:
        users = users.filter(department__name=department)

    if status == 'active':
        users = users.filter(is_active=True)
    elif status == 'inactive':
        users = users.filter(is_active=False)

    users = users.order_by('username')

    departments = Department.objects.order_by('name')

    return render(request, 'accounts/manage_users.html', {
        'users': users,
        'departments': departments,
        'search': search,
        'selected_role': role,
        'selected_department': department,
        'selected_status': status,
    })
```

#### `accounts/views.py` → `edit_user`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/02a68f05b7ab83749791ab60b9cf2245a201c26d/accounts/views.py#L148-L177)

```python
@role_required('admin')
def edit_user(request, user_id):

    account = get_object_or_404(
        User,
        pk=user_id,
        role__in=['employee', 'customer', 'support'],
        is_superuser=False
    )

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=account)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'User details updated successfully.'
            )

            return redirect('manage_users')

    else:
        form = UserEditForm(instance=account)

    return render(request, 'accounts/edit_user.html', {
        'form': form,
        'account': account,
    })
```

#### `accounts/views.py` → `change_user_status`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/02a68f05b7ab83749791ab60b9cf2245a201c26d/accounts/views.py#L179-L216)

```python
@role_required('admin')
@require_POST
def change_user_status(request, user_id):

    action = request.POST.get('action')

    if action not in ('activate', 'deactivate'):
        messages.error(request, 'Invalid account action.')
        return redirect('manage_users')

    account = get_object_or_404(
        User,
        pk=user_id,
        role__in=['employee', 'customer', 'support'],
        is_superuser=False
    )

    new_status = action == 'activate'

    with transaction.atomic():

        if account.is_active != new_status:
            account.is_active = new_status
            account.save(update_fields=['is_active'])

            send_account_status_email(account)

            messages.success(
                request,
                'Account status updated successfully.'
            )
        else:
            messages.info(
                request,
                'This account already has the selected status.'
            )

    return redirect('manage_users')
```

**Verified references in this chapter:** 7/7.

### Related development commits

- [2088cf9734](https://github.com/Jyothy-p-anil/IssueInsight/commit/2088cf9734d734220127fd71d0393ec3c612fd4c) — feat: implement support department queue and ticket claiming (2026-11-08)
- [637e9020d7](https://github.com/Jyothy-p-anil/IssueInsight/commit/637e9020d76f29c02dc68bf575d41e99fd717d84) — feat: complete in-app account status management (2026-11-08)
- [ea64b763d1](https://github.com/Jyothy-p-anil/IssueInsight/commit/ea64b763d1c0e69bc4ef3b3645cc32fc87f12549) — test: finalize module 3 permissions (2026-11-08)
- [6885ea66b8](https://github.com/Jyothy-p-anil/IssueInsight/commit/6885ea66b8d30c3d5bf80cd622269134bf4d8665) — test: complete module 3 permission verification (2026-11-08)

*These links show historical changes. A commit may touch several modules; inspect its diff before attributing every edit to this chapter.*

### How we checked it

The source code and test definitions were inspected from Git. **This journal generator does not run Django tests** and cannot prove that every workflow works.

### Explain it independently

1. What existed before this feature?
2. Which file handles the incoming request or data?
3. Which checks protect the operation?
4. How do the results reach the next page or database record?

### Teacher / interview questions

- Why do we check reporter=request.user?
- Why must department and assignment restrictions be checked on the server?

### Connections

Back to [this module's chapter list](README.md), or view the [complete source module map](../MODULE_INDEX.md).
