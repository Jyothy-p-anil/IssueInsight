from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from accounts.decorators import role_required



from django.contrib import messages
from .forms import EmployeeComplaintForm, CustomerComplaintForm


from .models import Ticket, Department, Category

from .forms import (
    EmployeeComplaintForm,
    CustomerComplaintForm,
    ManualRoutingForm,
    TicketMessageForm,
    SupportMessageForm,
    DepartmentForm,
    CategoryForm,
)

from django.db import transaction

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

    
    conversation = ticket.ticket_messages.filter(
        is_internal=False
    ).select_related('author')

    can_reply = ticket.status in (
        'submitted', 'in_progress', 'reopened'
    )

    return render(
        request,
        'tickets/ticket_detail.html',
        {
            'ticket': ticket,
            'conversation': conversation,
            'reply_form': TicketMessageForm(),
            'can_reply': can_reply,
        }
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

    
    conversation = ticket.ticket_messages.select_related(
        'author'
    )

    can_reply = (
        ticket.assigned_to_id == request.user.id
        and ticket.status in ('in_progress', 'reopened')
    )

    return render(
        request,
        'tickets/support_ticket_detail.html',
        {
            'ticket': ticket,
            'can_claim': can_claim,
            'conversation': conversation,
            'reply_form': SupportMessageForm(),
            'can_reply': can_reply,
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


# Employee / Customer: add public message to own ticket

@role_required('employee', 'customer')
@require_POST
def add_reporter_message(request, ticket_id):

    ticket = get_object_or_404(
        Ticket,
        pk=ticket_id,
        reporter=request.user
    )

    if ticket.status not in (
        'submitted', 'in_progress', 'reopened'
    ):
        messages.error(
            request,
            'Replies are not available for this ticket status.'
        )
        return redirect('ticket_detail', ticket_id=ticket_id)

    form = TicketMessageForm(request.POST)

    if form.is_valid():
        message = form.save(commit=False)
        message.ticket = ticket
        message.author = request.user
        message.is_internal = False
        message.save()

        messages.success(request, 'Message sent successfully.')

    else:
        messages.error(request, 'Please enter a valid message.')

    return redirect('ticket_detail', ticket_id=ticket_id)


# Support Staff: public reply or internal note

@role_required('support')
@require_POST
def add_support_message(request, ticket_id):

    ticket = get_object_or_404(
        Ticket,
        pk=ticket_id,
        department_id=request.user.department_id,
        assigned_to=request.user
    )

    if ticket.status not in ('in_progress', 'reopened'):
        messages.error(
            request,
            'Replies are not available for this ticket status.'
        )
        return redirect(
            'support_ticket_detail',
            ticket_id=ticket_id
        )

    form = SupportMessageForm(request.POST)

    if form.is_valid():

        with transaction.atomic():
            message = form.save(commit=False)
            message.ticket = ticket
            message.author = request.user
            message.save()

            # Record only the first PUBLIC Support Staff reply.
            if not message.is_internal:
                Ticket.objects.filter(
                    pk=ticket.pk,
                    first_response_at__isnull=True
                ).update(
                    first_response_at=message.created_at
                )

        messages.success(
            request,
            'Internal note saved.' if message.is_internal
            else 'Public reply sent successfully.'
        )

    else:
        messages.error(request, 'Please enter a valid message.')

    return redirect(
        'support_ticket_detail',
        ticket_id=ticket_id
    )


# Step 45: Admin manual complaint routing

@role_required('admin')
def admin_pending_routing(request):

    tickets = Ticket.objects.filter(
        department__isnull=True,
        assigned_to__isnull=True,
        status__in=['submitted', 'reopened']
    ).select_related(
        'reporter', 'category', 'product'
    ).order_by('created_at')

    return render(
        request,
        'tickets/admin_pending_routing.html',
        {'tickets': tickets}
    )


@role_required('admin')
def admin_route_ticket(request, ticket_id):

    ticket = get_object_or_404(
        Ticket.objects.select_related(
            'reporter', 'category', 'product'
        ),
        pk=ticket_id,
        department__isnull=True,
        assigned_to__isnull=True,
        status__in=['submitted', 'reopened']
    )

    if request.method == 'POST':
        form = ManualRoutingForm(request.POST)

        if form.is_valid():
            department = form.cleaned_data['department']

            updated = Ticket.objects.filter(
                pk=ticket.pk,
                department__isnull=True,
                assigned_to__isnull=True,
                status__in=['submitted', 'reopened']
            ).update(
                department_id=department.pk
            )

            if updated:
                messages.success(
                    request,
                    f'Ticket #{ticket.pk} routed to '
                    f'{department.name}.'
                )
            else:
                messages.warning(
                    request,
                    'This ticket has already been routed '
                    'or is no longer eligible.'
                )

            return redirect('admin_pending_routing')

    else:
        form = ManualRoutingForm()

    return render(
        request,
        'tickets/admin_route_ticket.html',
        {
            'ticket': ticket,
            'form': form
        }
    )

# Module 4: Admin department management

@role_required('admin')
def manage_departments(request):

    if request.method == 'POST':
        form = DepartmentForm(request.POST)

        if form.is_valid():
            department = form.save()

            messages.success(
                request,
                f'{department.name} added successfully.'
            )

            return redirect('manage_departments')

    else:
        form = DepartmentForm()

    departments = Department.objects.order_by('name')

    return render(
        request,
        'tickets/admin_departments.html',
        {
            'departments': departments,
            'form': form,
        }
    )





# Module 4: Edit department

@role_required('admin')
def edit_department(request, department_id):

    department = get_object_or_404(
        Department,
        pk=department_id
    )

    if request.method == 'POST':
        form = DepartmentForm(
            request.POST,
            instance=department
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Department updated successfully.'
            )

            return redirect('manage_departments')

    else:
        form = DepartmentForm(instance=department)

    return render(
        request,
        'tickets/admin_department_edit.html',
        {
            'form': form,
            'department': department,
        }
    )


# Module 4: Delete only unused departments

@role_required('admin')
def delete_department(request, department_id):

    department = get_object_or_404(
        Department,
        pk=department_id
    )

    staff_count = department.staff_members.count()
    category_count = department.category_set.count()
    ticket_count = department.ticket_set.count()

    has_dependencies = any((
        staff_count,
        category_count,
        ticket_count
    ))

    if request.method == 'POST':

        if has_dependencies:
            messages.error(
                request,
                'Cannot delete this department because it '
                'is linked to staff, categories or tickets.'
            )

            return redirect('manage_departments')

        department_name = department.name
        department.delete()

        messages.success(
            request,
            f'{department_name} deleted successfully.'
        )

        return redirect('manage_departments')

    return render(
        request,
        'tickets/admin_department_confirm_delete.html',
        {
            'department': department,
            'staff_count': staff_count,
            'category_count': category_count,
            'ticket_count': ticket_count,
            'has_dependencies': has_dependencies,
        }
    )



# Module 4: Admin category management

@role_required('admin')
def manage_categories(request):

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            category = form.save()

            messages.success(
                request,
                f'{category.name} category added successfully.'
            )

            return redirect('manage_categories')

    else:
        form = CategoryForm()

    categories = Category.objects.select_related(
        'department'
    ).order_by(
        'division',
        'name',
        'pk'
    )

    return render(
        request,
        'tickets/admin_categories.html',
        {
            'categories': categories,
            'form': form,
        }
    )



# Step 53: Edit category

@role_required('admin')
def edit_category(request, category_id):

    category = get_object_or_404(
        Category,
        pk=category_id
    )

    if request.method == 'POST':
        form = CategoryForm(
            request.POST,
            instance=category
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Category updated successfully.'
            )

            return redirect('manage_categories')

    else:
        form = CategoryForm(instance=category)

    return render(
        request,
        'tickets/admin_category_edit.html',
        {
            'form': form,
            'category': category,
        }
    )


#Delete unused categories only

@role_required('admin')
def delete_category(request, category_id):

    category = get_object_or_404(
        Category,
        pk=category_id
    )

    ticket_count = category.ticket_set.count()
    is_system_category = (
        category.name.casefold() == 'other'
    )

    can_delete = (
        ticket_count == 0
        and not is_system_category
    )

    if request.method == 'POST':

        if not can_delete:
            messages.error(
                request,
                'This category cannot be deleted. '
                'It is either used by existing tickets '
                'or required for manual routing.'
            )

            return redirect('manage_categories')

        category_name = category.name
        category.delete()

        messages.success(
            request,
            f'{category_name} deleted successfully.'
        )

        return redirect('manage_categories')

    return render(
        request,
        'tickets/admin_category_confirm_delete.html',
        {
            'category': category,
            'ticket_count': ticket_count,
            'is_system_category': is_system_category,
            'can_delete': can_delete,
        }
    )
