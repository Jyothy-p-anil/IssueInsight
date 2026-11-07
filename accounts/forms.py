
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


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

        if data.get('role') == 'support' and not data.get('department'):
            self.add_error(
                'department',
                'Select a department for support staff.'
            )

        return data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_unusable_password()

        if commit:
            user.save()

        return user

