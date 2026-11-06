
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
