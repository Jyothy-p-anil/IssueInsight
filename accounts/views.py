
import logging

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from .forms import CustomerRegistrationForm


logger = logging.getLogger(__name__)


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
