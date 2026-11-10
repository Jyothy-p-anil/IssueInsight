# Module 05 — Employee Complaint Submission

## Employee complaint form and save workflow

### Before we begin

Employees require a validated route for reporting facilities problems without being allowed to forge reporter IDs or assignments.

### What we worked on

EmployeeComplaintForm validates title, description, floor and category. The view assigns reporter, division, status and department before saving.

### Picture it this way

Follow one real request or data change through the functions shown below. Notice which fields come from the user and which are set by the server.

### Important Django concepts

`ModelForm`, `cleaned_data`, `commit=False`, `request.user`, `server-side assignment`.

### Actual code from the committed project

Source revision: [`b1b1f5e53a80`](https://github.com/Jyothy-p-anil/IssueInsight/commit/b1b1f5e53a80b8dfaec25fd31ce2e9d337258fb6) on `master`. The excerpts are current code, not invented historical versions.

#### `tickets/forms.py` → `EmployeeComplaintForm`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/b1b1f5e53a80b8dfaec25fd31ce2e9d337258fb6/tickets/forms.py#L7-L35)

```python
class EmployeeComplaintForm(forms.ModelForm):

    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(
            division='employee'
        ).order_by('name'),
        empty_label='Select a category',
        required=True
    )

    class Meta:
        model = Ticket
        fields = ('title', 'description', 'floor', 'category')

        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'floor': forms.TextInput(attrs={
                'placeholder': 'Example: Floor 2'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'
```

#### `tickets/views.py` → `submit_employee_complaint`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/b1b1f5e53a80b8dfaec25fd31ce2e9d337258fb6/tickets/views.py#L79-L108)

```python
@role_required('employee')
def submit_employee_complaint(request):

    if request.method == 'POST':
        form = EmployeeComplaintForm(request.POST)

        if form.is_valid():
            ticket = form.save(commit=False)

            ticket.reporter = request.user
            ticket.division = 'employee'
            ticket.status = 'submitted'

            ticket.department = ticket.category.department

            ticket.save()

            messages.success(
                request,
                f'Complaint #{ticket.pk} submitted successfully.'
            )

            return redirect('employee_my_tickets')

    else:
        form = EmployeeComplaintForm()

    return render(request, 'tickets/employee_complaint_form.html', {
        'form': form
    })
```

#### `templates/tickets/employee_complaint_form.html`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/b1b1f5e53a80b8dfaec25fd31ce2e9d337258fb6/templates/tickets/employee_complaint_form.html#L1-L50)

```html

{% extends 'base.html' %}

{% block title %}Submit Complaint | IssueInsight{% endblock %}

{% block content %}

<h2>Submit Workplace Complaint</h2>

<p class="text-muted">
    Report an issue you are experiencing at work.
</p>

<div class="card shadow-sm mt-4">
    <div class="card-body">

        <form method="post">
            {% csrf_token %}

            {% for field in form %}
                <div class="mb-3">
                    <label class="form-label"
                           for="{{ field.id_for_label }}">
                        {{ field.label }}
                    </label>

                    {{ field }}

                    {% for error in field.errors %}
                        <div class="text-danger small">
                            {{ error }}
                        </div>
                    {% endfor %}
                </div>
            {% endfor %}

            <button type="submit" class="btn btn-primary">
                Submit Complaint
            </button>

            <a href="{% url 'employee_my_tickets' %}"
               class="btn btn-outline-secondary">
                Cancel
            </a>
        </form>

    </div>
</div>

{% endblock %}
```

**Verified references in this chapter:** 3/3.

### Related development commits

- [734a0417b0](https://github.com/Jyothy-p-anil/IssueInsight/commit/734a0417b0a72dc08f8fabe1a1fb5cc19d0a3d1f) — feat: implement employee complaint submission and my tickets (2026-11-08)

*These links show historical changes. A commit may touch several modules; inspect its diff before attributing every edit to this chapter.*

### How we checked it

The source code and test definitions were inspected from Git. **This journal generator does not run Django tests** and cannot prove that every workflow works.

### Explain it independently

1. What existed before this feature?
2. Which file handles the incoming request or data?
3. Which checks protect the operation?
4. How do the results reach the next page or database record?

### Teacher / interview questions

- Why do we set reporter in the view?
- Why call form.save(commit=False)?

### Connections

Back to [this module's chapter list](README.md), or view the [complete source module map](../MODULE_INDEX.md).
