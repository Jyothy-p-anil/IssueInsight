from django import forms
from .models import Ticket, Category, Product
from .models import Ticket, Category, Product, Department

from .models import (
    Ticket, Category, Product, Department, TicketMessage
)


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


# Form for manual routing of complaints to support departments
class ManualRoutingForm(forms.Form):

    department = forms.ModelChoiceField(
        queryset=Department.objects.order_by('name'),
        empty_label='Select a support department',
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )


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


# Form for creating and editing support departments
class DepartmentForm(forms.ModelForm):

    class Meta:
        model = Department
        fields = ('name',)

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter department name'
            })
        }

    def clean_name(self):
        name = ' '.join(self.cleaned_data['name'].split())

        if Department.objects.filter(
            name__iexact=name
        ).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(
                'A department with this name already exists.'
            )

        return name





# Module 4: Category management

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category

        fields = (
            'name',
            'division',
            'department',
        )

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category name'
            }),
            'division': forms.Select(attrs={
                'class': 'form-select'
            }),
            'department': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

        labels = {
            'name': 'Category Name',
            'division': 'Complaint Type',
            'department': 'Support Department',
        }

    def clean_name(self):

        name = ' '.join(
            self.cleaned_data['name'].split()
        )

        return name

    def clean(self):

        cleaned_data = super().clean()

        name = cleaned_data.get('name')
        division = cleaned_data.get('division')
        department = cleaned_data.get('department')

        # Category names must be unique within a division.
        # The same name can exist once for Employee
        # and once for Customer complaints.

        if name and division:

            duplicate = Category.objects.filter(
                name__iexact=name,
                division=division
            ).exclude(pk=self.instance.pk).exists()

            if duplicate:
                self.add_error(
                    'name',
                    'This category already exists '
                    'for the selected complaint type.'
                )

        # Other complaints require manual routing.

        if name:

            if name.casefold() == 'other':

                if department:
                    self.add_error(
                        'department',
                        'The Other category must not have '
                        'a department. It uses manual routing.'
                    )

            elif not department:
                self.add_error(
                    'department',
                    'Select a support department '
                    'for this category.'
                )

        return cleaned_data
