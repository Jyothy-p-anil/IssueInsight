# Module 02 — Initial UI and Authentication

## Password reset, staff setup and account notifications

### Before we begin

Users need password recovery. Admin-created staff accounts need a safe initial password setup process without exposing passwords to Admin.

### What we worked on

A password reset view creates a time-limited token link. Email services notify users of account setup or status changes.

### Picture it this way

Follow one real request or data change through the functions shown below. Notice which fields come from the user and which are set by the server.

### Important Django concepts

`password reset token`, `email backend`, `service function`, `unusable password`, `authentication views`.

### Actual code from the committed project

Source revision: [`4c179f64e177`](https://github.com/Jyothy-p-anil/IssueInsight/commit/4c179f64e177a16ce2f536aa4b8c025639566ab9) on `master`. The excerpts are current code, not invented historical versions.

#### `accounts/forms.py` → `StaffAccountCreationForm`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/4c179f64e177a16ce2f536aa4b8c025639566ab9/accounts/forms.py#L37-L83)

```python
class StaffAccountCreationForm(forms.ModelForm):

    role = forms.ChoiceField(choices=[
        ('employee', 'Employee'),
        ('support', 'Support Staff'),
    ])

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'department')

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                'This email is already registered.'
            )

        return email

    
    def clean(self):
        data = super().clean()

        if data.get('role') == 'support':
            if not data.get('department'):
                self.add_error(
                    'department',
                    'Select a department for Support Staff.'
                )
        else:
            data['department'] = None

        return data


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_unusable_password()

        if commit:
            user.save()

        return user
```

#### `accounts/services.py` → `send_password_setup_email`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/4c179f64e177a16ce2f536aa4b8c025639566ab9/accounts/services.py#L16-L53)

```python
def send_password_setup_email(request, user):

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    path = reverse(
        'password_reset_confirm',
        kwargs={'uidb64': uid, 'token': token}
    )

    setup_link = request.build_absolute_uri(path)

    username = user.username
    email = user.email
    user_id = user.pk

    def send_email():
        try:
            send_mail(
                subject='Set Up Your IssueInsight Password',
                message=(
                    f'Hello {username},\n\n'
                    'Your IssueInsight account has been created.\n\n'
                    'Set your password using this link:\n'
                    f'{setup_link}\n\n'
                    'Thank you,\nIssueInsight Team'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception:
            logger.exception(
                'Password setup email failed for user %s',
                user_id
            )

    transaction.on_commit(send_email)
```

#### `accounts/services.py` → `send_account_status_email`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/4c179f64e177a16ce2f536aa4b8c025639566ab9/accounts/services.py#L56-L90)

```python
def send_account_status_email(user):

    if not user.email:
        return

    status = (
        'reactivated' if user.is_active
        else 'deactivated'
    )

    username = user.username
    email = user.email
    user_id = user.pk

    def send_email():
        try:
            send_mail(
                subject=f'IssueInsight Account {status.title()}',
                message=(
                    f'Hello {username},\n\n'
                    f'Your IssueInsight account has been '
                    f'{status}.\n\n'
                    'Thank you,\nIssueInsight Team'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception:
            logger.exception(
                'Account status email failed for user %s',
                user_id
            )

    transaction.on_commit(send_email)
```

#### `config/urls.py` → `password_reset`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/4c179f64e177a16ce2f536aa4b8c025639566ab9/config/urls.py#L31-L37)

```python
path(
    'password-reset/',
    auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset_form.html'
    ),
    name='password_reset'
),
```

#### `config/urls.py` → `password_reset_confirm`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/4c179f64e177a16ce2f536aa4b8c025639566ab9/config/urls.py#L48-L54)

```python
path(
    'password-reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html'
    ),
    name='password_reset_confirm'
),
```

**Verified references in this chapter:** 5/5.

### Related development commits

- [1f574365cb](https://github.com/Jyothy-p-anil/IssueInsight/commit/1f574365cb248fc82bb6f10a3474e9f3c8565fa6) — feat: add password reset request pages (2026-11-06)
- [cd67bca6ac](https://github.com/Jyothy-p-anil/IssueInsight/commit/cd67bca6ac60bb06611713c2394527005717e01f) — feat: complete password reset pages and routing (2026-11-07)
- [e06f89c70f](https://github.com/Jyothy-p-anil/IssueInsight/commit/e06f89c70fd47a288786180fe4f1769d58cc517b) — feat: email password setup links for staff accounts (2026-11-07)
- [585145d145](https://github.com/Jyothy-p-anil/IssueInsight/commit/585145d145608857e6f9f730fd6c04df0b96d47f) — refactor: reuse staff password setup email service (2026-11-08)

*These links show historical changes. A commit may touch several modules; inspect its diff before attributing every edit to this chapter.*

### How we checked it

The source code and test definitions were inspected from Git. **This journal generator does not run Django tests** and cannot prove that every workflow works.

### Explain it independently

1. What existed before this feature?
2. Which file handles the incoming request or data?
3. Which checks protect the operation?
4. How do the results reach the next page or database record?

### Teacher / interview questions

- Why shouldn't Admin know a staff member's password?
- What makes a password-reset link safe to use?

### Connections

Back to [this module's chapter list](README.md), or view the [complete source module map](../MODULE_INDEX.md).
