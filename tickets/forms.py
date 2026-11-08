from django import forms
from .models import Ticket, Category


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