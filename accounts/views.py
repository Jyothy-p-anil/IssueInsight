
import logging

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .models import User
from .decorators import role_required
from django.db.models import Q
from tickets.models import Department

from django.contrib import messages
from .services import send_password_setup_email




from .forms import CustomerRegistrationForm, StaffAccountCreationForm

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



@role_required('admin')
def manage_users(request):

    search = request.GET.get('search', '').strip()
    role = request.GET.get('role', '')
    department = request.GET.get('department', '')
    status = request.GET.get('status', '')

    users = User.objects.filter(
        role__in=['employee', 'customer', 'support'],
        is_superuser=False
    ).select_related('department')

    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search)
        )

    if role in ['employee', 'customer', 'support']:
        users = users.filter(role=role)

    if department:
        users = users.filter(department__name=department)

    if status == 'active':
        users = users.filter(is_active=True)
    elif status == 'inactive':
        users = users.filter(is_active=False)

    users = users.order_by('username')

    departments = Department.objects.order_by('name')

    return render(request, 'accounts/manage_users.html', {
        'users': users,
        'departments': departments,
        'search': search,
        'selected_role': role,
        'selected_department': department,
        'selected_status': status,
    })


@role_required('admin')
def create_staff_account(request):

    if request.method == 'POST':
        form = StaffAccountCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            send_password_setup_email(request, user)

            messages.success(
                request,
                'Account created. Please verify that the '
                'password setup email arrives.'
            )

            return redirect('manage_users')

    else:
        form = StaffAccountCreationForm()

    return render(request, 'accounts/create_staff_account.html', {
        'form': form
    })

