from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from accounts.decorators import role_required



from django.contrib import messages
from .forms import EmployeeComplaintForm, CustomerComplaintForm
from .models import Ticket


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
