from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from accounts.decorators import role_required



from django.contrib import messages
from .forms import EmployeeComplaintForm, CustomerComplaintForm
from .models import Ticket


from django.views.decorators.http import require_POST

@login_required
def home(request):
    return render(request, 'home.html')
    
@role_required('employee')
def employee_dashboard(request):
    return render(request, 'role_dashboard.html', {
        'page_title': 'Employee Dashboard'
    })


@role_required('customer')
def customer_dashboard(request):
    return render(request, 'role_dashboard.html', {
        'page_title': 'Customer Dashboard'
    })


@role_required('support')
def support_dashboard(request):
    return render(request, 'role_dashboard.html', {
        'page_title': 'Support Staff Dashboard'
    })


@role_required('admin')
def admin_dashboard(request):
    return render(request, 'role_dashboard.html', {
        'page_title': 'Admin Dashboard'
    })

@login_required
def dashboard_redirect(request):
    user = request.user

    if user.is_superuser or user.role == 'admin':
        return redirect('admin_dashboard')

    dashboards = {
        'employee': 'employee_dashboard',
        'customer': 'customer_dashboard',
        'support': 'support_dashboard',
    }

    dashboard = dashboards.get(user.role, 'home')

    return redirect(dashboard)


#function to submit employee complaint

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


@role_required('employee')
def employee_my_tickets(request):

    tickets = Ticket.objects.filter(
        reporter=request.user,
        division='employee'
    ).select_related(
        'category', 'department'
    ).order_by('-created_at')

    return render(request, 'tickets/employee_my_tickets.html', {
        'tickets': tickets
    })

#function to submit customer complaint and view tickets

@role_required('customer')
def submit_customer_complaint(request):

    if request.method == 'POST':
        form = CustomerComplaintForm(request.POST)

        if form.is_valid():
            ticket = form.save(commit=False)

            ticket.reporter = request.user
            ticket.division = 'customer'
            ticket.status = 'submitted'

            ticket.department = ticket.category.department

            ticket.save()

            messages.success(
                request,
                f'Complaint #{ticket.pk} submitted successfully.'
            )

            return redirect('customer_my_tickets')

    else:
        form = CustomerComplaintForm()

    return render(
        request,
        'tickets/customer_complaint_form.html',
        {'form': form}
    )


@role_required('customer')
def customer_my_tickets(request):

    tickets = Ticket.objects.filter(
        reporter=request.user,
        division='customer'
    ).select_related(
        'category', 'department', 'product'
    ).order_by('-created_at')

    return render(
        request,
        'tickets/customer_my_tickets.html',
        {'tickets': tickets}
    )


# Employee and Customer ticket detail page

@role_required('employee', 'customer')
def ticket_detail(request, ticket_id):

    ticket = get_object_or_404(
        Ticket.objects.select_related(
            'reporter',
            'category',
            'department',
            'product',
            'assigned_to'
        ),
        pk=ticket_id,
        reporter=request.user
    )

    return render(
        request,
        'tickets/ticket_detail.html',
        {'ticket': ticket}
    )


# Support Staff: unassigned complaints for their department

@role_required('support')
def support_department_queue(request):

    if not request.user.department_id:
        messages.warning(
            request,
            'Your account has no support department assigned.'
        )
        return redirect('support_dashboard')

    tickets = Ticket.objects.filter(
        department_id=request.user.department_id,
        assigned_to__isnull=True,
        status__in=['submitted', 'reopened']
    ).select_related(
        'reporter', 'category'
    ).order_by('created_at')

    return render(
        request,
        'tickets/support_ticket_list.html',
        {
            'tickets': tickets,
            'page_title': 'Department Queue',
            'description': (
                'Unassigned complaints waiting for your department.'
            ),
            'empty_message': 'No unassigned complaints.',
        }
    )


# Support Staff: complaints assigned personally to them

@role_required('support')
def support_assigned_tickets(request):

    if not request.user.department_id:
        messages.warning(
            request,
            'Your account has no support department assigned.'
        )
        return redirect('support_dashboard')

    tickets = Ticket.objects.filter(
        department_id=request.user.department_id,
        assigned_to=request.user
    ).select_related(
        'reporter', 'category'
    ).order_by('-created_at')

    return render(
        request,
        'tickets/support_ticket_list.html',
        {
            'tickets': tickets,
            'page_title': 'Assigned Tickets',
            'description': 'Complaints assigned to you.',
            'empty_message': 'No tickets assigned to you.',
        }
    )


# Support Staff: view a ticket from their own department

@role_required('support')
def support_ticket_detail(request, ticket_id):

    if not request.user.department_id:
        messages.warning(
            request,
            'Your account has no support department assigned.'
        )
        return redirect('support_dashboard')

    ticket = get_object_or_404(
        Ticket.objects.select_related(
            'reporter',
            'category',
            'department',
            'product',
            'assigned_to'
        ),
        pk=ticket_id,
        department_id=request.user.department_id
    )

    can_claim = (
        ticket.assigned_to_id is None
        and ticket.status in ('submitted', 'reopened')
    )

    return render(
        request,
        'tickets/support_ticket_detail.html',
        {
            'ticket': ticket,
            'can_claim': can_claim
        }
    )


# Support Staff: claim an available ticket

@role_required('support')
@require_POST
def claim_support_ticket(request, ticket_id):

    if not request.user.department_id:
        messages.error(
            request,
            'Your account has no support department assigned.'
        )
        return redirect('support_dashboard')

    # Conditional update prevents two staff members
    # from successfully claiming the same ticket.

    updated = Ticket.objects.filter(
        pk=ticket_id,
        department_id=request.user.department_id,
        assigned_to__isnull=True,
        status__in=['submitted', 'reopened']
    ).update(
        assigned_to=request.user,
        status='in_progress'
    )

    if updated:
        messages.success(
            request,
            f'Ticket #{ticket_id} assigned to you.'
        )
        return redirect(
            'support_ticket_detail',
            ticket_id=ticket_id
        )

    # Do not reveal tickets from other departments.
    get_object_or_404(
        Ticket,
        pk=ticket_id,
        department_id=request.user.department_id
    )

    messages.warning(
        request,
        'This ticket is already assigned or cannot be claimed.'
    )

    return redirect('support_department_queue')

