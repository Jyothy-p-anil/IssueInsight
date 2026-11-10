# Module 02 — Initial UI and Authentication

## Login, logout and customer registration

### Before we begin

Users require sessions and role-specific access. Customers may register, while staff accounts have a separate controlled creation flow.

### What we worked on

Django authenticates credentials, creates a session and redirects to dashboard_redirect. A valid customer form creates a User whose role is set server-side.

### Picture it this way

Follow one real request or data change through the functions shown below. Notice which fields come from the user and which are set by the server.

### Important Django concepts

`LoginView`, `LogoutView`, `ModelForm`, `UserCreationForm`, `session`, `server-side role assignment`.

### Actual code from the committed project

Source revision: [`8aa5fec6ff3d`](https://github.com/Jyothy-p-anil/IssueInsight/commit/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a) on `master`. The excerpts are current code, not invented historical versions.

#### `accounts/views.py` → `register`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/accounts/views.py#L34-L71)

```python
def register(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()

            try:
                send_mail(
                    subject='Welcome to IssueInsight',
                    message=(
                        f'Hello {user.username},\n\n'
                        'Welcome to IssueInsight!\n\n'
                        'Your account has been created successfully.\n'
                        'You can now log in and submit complaints.\n\n'
                        'Thank you,\n'
                        'IssueInsight Team'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )

            except Exception:
                logger.exception('Welcome email could not be sent.')

            return redirect('login')

    else:
        form = CustomerRegistrationForm()

    return render(request, 'accounts/register.html', {
        'form': form
    })
```

#### `accounts/forms.py` → `CustomerRegistrationForm`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/accounts/forms.py#L7-L32)

```python
class CustomerRegistrationForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                'An account with this email already exists.'
            )

        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'customer'

        if commit:
            user.save()

        return user
```

#### `tickets/views.py` → `dashboard_redirect`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/tickets/views.py#L59-L74)

```python
@login_required
def dashboard_redirect(request):
    user = request.user

    if user.is_superuser or user.role == 'admin':
        return redirect('admin_dashboard')

    dashboards = {
        'employee': 'employee_dashboard',
        'customer': 'customer_dashboard',
        'support': 'support_dashboard',
    }

    dashboard = dashboards.get(user.role, 'home')

    return redirect(dashboard)
```

#### `config/urls.py` → `login`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/config/urls.py#L16-L23)

```python
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='accounts/login.html',
            redirect_authenticated_user=True
        ),
        name='login'
    ),
```

#### `config/urls.py` → `logout`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/config/urls.py#L24-L28)

```python
   path(
    'logout/',
    auth_views.LogoutView.as_view(next_page='login'),
    name='logout'
),
```

#### `config/urls.py` → `register`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/8aa5fec6ff3d8f653abccfbf629f89e92ba1f67a/config/urls.py#L29)

```python
    path('register/', account_views.register, name='register'),
```

**Verified references in this chapter:** 6/6.

### Related development commits

- [df8ffa579b](https://github.com/Jyothy-p-anil/IssueInsight/commit/df8ffa579b38b2e5aad3c9580ea58339ca91add1) — feat: add IssueInsight login page (2026-11-05)
- [1f477f387c](https://github.com/Jyothy-p-anil/IssueInsight/commit/1f477f387c9ba80a430fed0d4bbebb70a5559563) — feat: implement secure logout (2026-11-06)
- [e1f48fd2b3](https://github.com/Jyothy-p-anil/IssueInsight/commit/e1f48fd2b3d1a67d1070b1a4cabcaaeaa1bd03c9) — feat: implement customer registration (2026-11-06)
- [e4f6c84546](https://github.com/Jyothy-p-anil/IssueInsight/commit/e4f6c8454625fdc9465bcb15ad1d63cf895b2721) — feat: complete role-based dashboard redirection (2026-11-08)

*These links show historical changes. A commit may touch several modules; inspect its diff before attributing every edit to this chapter.*

### How we checked it

The source code and test definitions were inspected from Git. **This journal generator does not run Django tests** and cannot prove that every workflow works.

### Explain it independently

1. What existed before this feature?
2. Which file handles the incoming request or data?
3. Which checks protect the operation?
4. How do the results reach the next page or database record?

### Teacher / interview questions

- How does Django remember who is logged in?
- Why must a customer not choose an Admin role during registration?

### Connections

Back to [this module's chapter list](README.md), or view the [complete source module map](../MODULE_INDEX.md).
