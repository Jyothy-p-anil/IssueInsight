# Module 06 — Customer Complaint Submission

## Customer product and category validation

### Before we begin

Customer complaints differ from workplace reports: they refer to a software product and may name an unlisted product.

### What we worked on

CustomerComplaintForm validates a customer category and requires either a selected product or an unlisted product name, not both.

### Picture it this way

Follow one real request or data change through the functions shown below. Notice which fields come from the user and which are set by the server.

### Important Django concepts

`ModelChoiceField`, `form.clean`, `form errors`, `queryset restrictions`.

### Actual code from the committed project

Source revision: [`9d0620abbb2d`](https://github.com/Jyothy-p-anil/IssueInsight/commit/9d0620abbb2df25ca00a4301a4a2318325521dbe) on `master`. The excerpts are current code, not invented historical versions.

#### `tickets/forms.py` → `CustomerComplaintForm`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/tickets/forms.py#L38-L105)

```python
class CustomerComplaintForm(forms.ModelForm):

    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(
            division='customer'
        ).order_by('name'),
        empty_label='Select an issue category',
        required=True
    )

    product = forms.ModelChoiceField(
        queryset=Product.objects.filter(
            is_active=True
        ).order_by('name'),
        empty_label='Other / Product not listed',
        required=False,
        label='Software Product'
    )

    class Meta:
        model = Ticket
        fields = (
            'title',
            'description',
            'product',
            'other_product_name',
            'category',
        )

        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 5
            }),
            'other_product_name': forms.TextInput(attrs={
                'placeholder': 'Only if your product is not listed'
            }),
        }

    def clean(self):
        data = super().clean()

        product = data.get('product')
        other_name = (
            data.get('other_product_name') or ''
        ).strip()

        if not product and not other_name:
            self.add_error(
                'other_product_name',
                'Enter the name of your unlisted product.'
            )

        if product and other_name:
            self.add_error(
                'other_product_name',
                'Leave this empty when selecting a listed product.'
            )

        return data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'
```

#### `templates/tickets/customer_complaint_form.html`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/9d0620abbb2df25ca00a4301a4a2318325521dbe/templates/tickets/customer_complaint_form.html#L1-L59)

```html

{% extends 'base.html' %}

{% block title %}Submit Complaint | IssueInsight{% endblock %}

{% block content %}

<h2>Submit Software Complaint</h2>

<p class="text-muted">
    Report an issue with one of our software products.
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

                    {% if field.help_text %}
                        <div class="form-text">
                            {{ field.help_text }}
                        </div>
                    {% endif %}

                    {% for error in field.errors %}
                        <div class="text-danger small">
                            {{ error }}
                        </div>
                    {% endfor %}

                </div>
            {% endfor %}

            <button type="submit"
                    class="btn btn-primary">
                Submit Complaint
            </button>

            <a href="{% url 'customer_my_tickets' %}"
               class="btn btn-outline-secondary">
                Cancel
            </a>

        </form>
    </div>
</div>

{% endblock %}
```

**Verified references in this chapter:** 2/2.

### Related development commits

- [67d4f75d55](https://github.com/Jyothy-p-anil/IssueInsight/commit/67d4f75d55377472f716645288ee2a2dc335e91d) — feat: implement customer complaint submission and my tickets (2026-11-08)

*These links show historical changes. A commit may touch several modules; inspect its diff before attributing every edit to this chapter.*

### How we checked it

The source code and test definitions were inspected from Git. **This journal generator does not run Django tests** and cannot prove that every workflow works.

### Explain it independently

1. What existed before this feature?
2. Which file handles the incoming request or data?
3. Which checks protect the operation?
4. How do the results reach the next page or database record?

### Teacher / interview questions

- Why should exactly one product choice be supplied?
- How does Django reject an Employee-only category?

### Connections

Back to [this module's chapter list](README.md), or view the [complete source module map](../MODULE_INDEX.md).
