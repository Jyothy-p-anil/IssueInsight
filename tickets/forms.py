from django import forms
from .models import Ticket, Category, Product


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
