# Module 04 — Master Data Management

## Software products and active status

### Before we begin

Customer complaints should identify the product affected, including cases where the product is not in the dropdown.

### What we worked on

Product stores the name and active flag. CustomerComplaintForm displays active products and permits a separate unlisted product name.

### Picture it this way

Follow one real request or data change through the functions shown below. Notice which fields come from the user and which are set by the server.

### Important Django concepts

`BooleanField`, `ModelChoiceField`, `active/inactive data`, `foreign-key history`.

### Actual code from the committed project

Source revision: [`0f32b2d705eb`](https://github.com/Jyothy-p-anil/IssueInsight/commit/0f32b2d705ebbe252fa5f9726861428f5bb85900) on `master`. The excerpts are current code, not invented historical versions.

#### `tickets/models.py` → `Product`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/tickets/models.py#L39-L49)

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

#### `tickets/forms.py` → `CustomerComplaintForm`

[Open the exact committed source](https://github.com/Jyothy-p-anil/IssueInsight/blob/0f32b2d705ebbe252fa5f9726861428f5bb85900/tickets/forms.py#L45-L114)

```python
class CustomerComplaintForm(forms.ModelForm):

    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),
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

        self.fields['category'].queryset = (
        get_suggestion_candidates('customer')
        )

        for field in self.fields.values():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'
```

**Verified references in this chapter:** 2/2.

### Related development commits

- [2f8f46bb3d](https://github.com/Jyothy-p-anil/IssueInsight/commit/2f8f46bb3d1160f78902d8657b39d03452619968) — feat: create software product model (2026-11-04)
- [67d4f75d55](https://github.com/Jyothy-p-anil/IssueInsight/commit/67d4f75d55377472f716645288ee2a2dc335e91d) — feat: implement customer complaint submission and my tickets (2026-11-08)
- [b1b1f5e53a](https://github.com/Jyothy-p-anil/IssueInsight/commit/b1b1f5e53a80b8dfaec25fd31ce2e9d337258fb6) — docs: fix module 4 index row (2026-11-10)
- [9d0620abbb](https://github.com/Jyothy-p-anil/IssueInsight/commit/9d0620abbb2df25ca00a4301a4a2318325521dbe) — test(module-4): complete master data management review (2026-11-10)
- [0cd5801c70](https://github.com/Jyothy-p-anil/IssueInsight/commit/0cd5801c70835ff6709c5156cc8478906f67573d) — feat(module-4): add product editing and activation controls (2026-11-10)
- [7e3f46e319](https://github.com/Jyothy-p-anil/IssueInsight/commit/7e3f46e319c60e257fa46980a0972e2b6bcc36ec) — feat(module-4): add software product listing and creation (2026-11-10)
- [06ddc706c9](https://github.com/Jyothy-p-anil/IssueInsight/commit/06ddc706c95a81ff3daade39c089303bf644e7be) — feat(module-4): add safe category editing and deletion (2026-11-10)
- [5d8f56c9d6](https://github.com/Jyothy-p-anil/IssueInsight/commit/5d8f56c9d6f3bdd8220d3f9ead176e18bc3d8639) — feat(module-4): add category listing and creation (2026-11-10)
- [ead7bbac4a](https://github.com/Jyothy-p-anil/IssueInsight/commit/ead7bbac4a54131d9115fdc34f30108950facb33) — feat(module-4): add safe department editing and deletion (2026-11-10)
- [5e16387502](https://github.com/Jyothy-p-anil/IssueInsight/commit/5e16387502adca96312af28a939ecff4547cf1c6) — feat(module-4): implement department listing and creation (2026-11-10)

*These links show historical changes. A commit may touch several modules; inspect its diff before attributing every edit to this chapter.*

### How we checked it

The source code and test definitions were inspected from Git. **This journal generator does not run Django tests** and cannot prove that every workflow works.

### Explain it independently

1. What existed before this feature?
2. Which file handles the incoming request or data?
3. Which checks protect the operation?
4. How do the results reach the next page or database record?

### Teacher / interview questions

- Why might a product be made inactive instead of deleted?
- How does the form handle an unlisted product?

### Connections

Back to [this module's chapter list](README.md), or view the [complete source module map](../MODULE_INDEX.md).
