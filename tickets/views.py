from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from accounts.decorators import role_required
from datetime import timedelta
from django.utils import timezone
from django.utils import timezone
from datetime import date
from django.db.models import Q


from django.contrib import messages


from .models import Ticket, Department, Category, Product, TicketActivity, TicketActivity,Announcement

from django.db import transaction

from .models import Notification

from .services.notifications import create_notification 

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .services.ai_category_prediction import (
    suggest_complaint_category,
    assess_category_suggestion,
    validate_suggested_category,
    
)




from .forms import (
    EmployeeComplaintForm,
    CustomerComplaintForm,
    ManualRoutingForm,
    TicketMessageForm,
    SupportMessageForm,
    DepartmentForm,
    CategoryForm,
    ProductForm,
    TicketResolutionForm,
    TicketReopeningForm,
    TicketMessage,
    AnnouncementForm,

)

from django.db import transaction

from django.views.decorators.http import require_POST


from .services.ai_urgency_detection import detect_complaint_urgency


from tickets.services.ai_complaint_similarity import find_similar_complaints



from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .models import Incident
from .services.incident_management import (
    create_incident,
    link_ticket_to_incident,
)


from .models import Incident, IncidentTicket, IncidentUpdate


from .services.recurring_product_issues import (
    get_recurring_product_issues,
    get_recurring_issue_groups,
    get_recurring_other_product_issue_groups,
)


from django.db.models import Avg, F, DurationField, ExpressionWrapper


from .services.public_holidays import get_kerala_public_holidays 

import calendar


#--------------------------



def home(request):
    announcements = Announcement.objects.filter(
        is_published=True
    ).order_by('-created_at')

    today = timezone.localdate()
    year = today.year
    month = today.month

    public_holidays = get_kerala_public_holidays(year)

    holiday_lookup = {}

    for holiday in public_holidays:
        holiday_lookup.setdefault(
            holiday["date"], []
        ).append(holiday["name"])

    calendar_data = []

    for month_number in range(1, 13):
        weeks = []

        for week in calendar.monthcalendar(year, month_number):
            days = []

            for day in week:
                date_string = (
                    f"{year}-{month_number:02d}-{day:02d}"
                    if day else None
                )

                days.append({
                    "day": day,
                    "date": date_string,
                    "holidays": holiday_lookup.get(
                        date_string, []
                    ),
                })

            weeks.append(days)

        calendar_data.append({
            "number": month_number,
            "name": calendar.month_name[month_number],
            "weeks": weeks,
        })

    return render(
        request,
        'home.html',
        {
            'announcements': announcements,
            'public_holidays': public_holidays,
            'calendar_data': calendar_data,
            'current_month': month,
            'current_year': year,
        }
    )

#FAQ and Contact Directory pages are public, no login required
def public_faq(request):
    return render(request, "tickets/public_faq.html")

def public_contact_directory(request):
    return render(
        request,
        "tickets/public_contact_directory.html",
    )

@role_required('employee')
def employee_dashboard(request):
    tickets = Ticket.objects.filter(
        reporter=request.user,
        division='employee',
    )

    status_counts = {
        status: tickets.filter(status=status).count()
        for status, label in Ticket.STATUS_CHOICES
    }

    recent_tickets = tickets.order_by(
        '-created_at'
    )[:5]

    return render(request, 'role_dashboard.html', {
        'page_title': 'Employee Dashboard',
        'total_tickets': tickets.count(),
        'status_counts': status_counts,
        'recent_tickets': recent_tickets,
    })



@role_required('customer')
def customer_dashboard(request):
    tickets = Ticket.objects.filter(
        reporter=request.user,
        division='customer',
    )

    status_counts = {
        status: tickets.filter(status=status).count()
        for status, label in Ticket.STATUS_CHOICES
    }

    recent_tickets = tickets.order_by('-created_at')[:5]

    return render(request, 'role_dashboard.html', {
        'page_title': 'Customer Dashboard',
        'total_tickets': tickets.count(),
        'status_counts': status_counts,
        'recent_tickets': recent_tickets,
    })


@role_required('support')
def support_dashboard(request):
    department = request.user.department

    if department is None:
        return render(request, 'role_dashboard.html', {
            'page_title': 'Support Staff Dashboard',
            'department_missing': True,
        })

    tickets = Ticket.objects.filter(
        department_id=request.user.department_id
    )

    assigned_tickets = tickets.filter(
        assigned_to=request.user
    )

    unassigned_tickets = tickets.filter(
        assigned_to__isnull=True,
        status__in=['submitted', 'reopened']
    )

    resolved_by_me = assigned_tickets.filter(
        status='resolved'
    )
    status_chart_labels = [
        label for value, label in Ticket.STATUS_CHOICES
    ]

    status_chart_counts = [
        tickets.filter(status=value).count()
        for value, label in Ticket.STATUS_CHOICES
    ]
    # Weekly complaint trends for the last four weeks.
    # The current week and three preceding weeks are included.
    today = timezone.localdate()
    current_week_start = today - timedelta(days=today.weekday())

    trend_labels = []
    trend_received = []
    trend_resolved = []

    for weeks_ago in range(3, -1, -1):
        week_start = current_week_start - timedelta(weeks=weeks_ago)
        week_end = week_start + timedelta(weeks=1)

        received_count = tickets.filter(
            created_at__date__gte=week_start,
            created_at__date__lt=week_end,
        ).count()

        resolved_count = tickets.filter(
            resolved_at__date__gte=week_start,
            resolved_at__date__lt=week_end,
        ).count()

        trend_labels.append(week_start.strftime('%d %b'))
        trend_received.append(received_count)
        trend_resolved.append(resolved_count)
    response_stats = tickets.filter(
        first_response_at__isnull=False
    ).aggregate(
        average=Avg(
            ExpressionWrapper(
                F('first_response_at') - F('created_at'),
                output_field=DurationField()
            )
        )
    )

    resolution_stats = tickets.filter(
        resolved_at__isnull=False
    ).aggregate(
        average=Avg(
            ExpressionWrapper(
                F('resolved_at') - F('created_at'),
                output_field=DurationField()
            )
        )
    )

    def format_hours(duration):
        if duration is None:
            return 'N/A'
        hours = duration.total_seconds() / 3600
        return f'{hours:.1f} hrs'
    
    return render(request, 'role_dashboard.html', {
        'page_title': 'Support Staff Dashboard',
        'department_name': department.name,
        'department_total': tickets.count(),
        'assigned_to_me': assigned_tickets.count(),
        'resolved_by_me': resolved_by_me.count(),
        'unassigned_count': unassigned_tickets.count(),
        'avg_response_time': format_hours(response_stats['average']),
        'avg_resolution_time': format_hours(resolution_stats['average']),
        'status_chart_labels': status_chart_labels,
        'status_chart_counts': status_chart_counts,
        'trend_labels': trend_labels,
        'trend_received': trend_received,
        'trend_resolved': trend_resolved,
    })


# Module 13 — Admin company-wide reporting


@role_required('admin')
def admin_reports(request):
    tickets = Ticket.objects.all()

    selected_period = request.GET.get('period', 'all')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    today = timezone.localdate()
    filter_error = ''

    if selected_period == 'last30':
        start_date = today - timedelta(days=29)
        tickets = tickets.filter(
            created_at__date__gte=start_date,
            created_at__date__lte=today,
        )

    elif selected_period == 'custom':
        try:
            if not date_from or not date_to:
                raise ValueError('Both dates are required.')

            start_date = date.fromisoformat(date_from)
            end_date = date.fromisoformat(date_to)

            if start_date > end_date:
                raise ValueError('Start date is after end date.')

            tickets = tickets.filter(
                created_at__date__gte=start_date,
                created_at__date__lte=end_date,
            )

        except ValueError:
            filter_error = 'Please enter a valid date range.'
            selected_period = 'all'
            date_from = ''
            date_to = ''

    else:
        selected_period = 'all'


    total = tickets.count()

    status_report = [
        {
            'label': label,
            'count': tickets.filter(status=value).count(),
        }
        for value, label in Ticket.STATUS_CHOICES
    ]

    department_report = [
        {
            'name': department.name,
            'count': tickets.filter(
                department=department
            ).count(),
        }
        for department in Department.objects.order_by('name')
    ]

    department_report.append({
        'name': 'Pending Routing',
        'count': tickets.filter(
            department__isnull=True
        ).count(),
    })

    source_report = [
        {
            'label': label,
            'count': tickets.filter(division=value).count(),
        }
        for value, label in Ticket.DIVISION_CHOICES
    ]

    urgency_report = [
        {
            'label': label,
            'count': tickets.filter(urgency=value).count(),
        }
        for value, label in Ticket.URGENCY_CHOICES
    ]


    # Module 13 — Category statistics
    category_report = [
        {
            'name': category.name,
            'count': tickets.filter(category=category).count(),
        }
        for category in Category.objects.order_by('name')
    ]

    category_report.append({
        'name': 'Uncategorised',
        'count': tickets.filter(category__isnull=True).count(),
    })

    # Response and resolution performance
    response_durations = [
        ticket.response_duration.total_seconds()
        for ticket in tickets
        if ticket.response_duration is not None
    ]

    resolution_durations = [
        ticket.resolution_duration.total_seconds()
        for ticket in tickets
        if ticket.resolution_duration is not None
    ]

    def average_hours(durations):
        if not durations:
            return None

        return round(
            sum(durations) / len(durations) / 3600,
            2
        )

    average_response_hours = average_hours(response_durations)
    average_resolution_hours = average_hours(resolution_durations)

    completed_count = tickets.filter(
        status__in=['resolved', 'closed']
    ).count()

    resolution_rate = (
        round(completed_count / total * 100, 2)
        if total else 0
    )


    return render(
        request,
        'tickets/admin_reports.html',
        {
            'total': total,
            'status_report': status_report,
            'department_report': department_report,
            'source_report': source_report,
            'urgency_report': urgency_report,
            'selected_period': selected_period,
            'date_from': date_from,
            'date_to': date_to,
            'filter_error': filter_error,
            'category_report': category_report,
            'average_response_hours': average_response_hours,
            'average_resolution_hours': average_resolution_hours,
            'resolution_rate': resolution_rate,
            'completed_count': completed_count,


        }
    )

@role_required('admin')
def admin_dashboard(request):
    tickets = Ticket.objects.all()

    # Admin Dashboard filters.
    selected_department = request.GET.get('department', '')
    selected_division = request.GET.get('division', '')

    # Filter by department, if valid.
    if selected_department.isdigit():
        if Department.objects.filter(
            pk=int(selected_department)
        ).exists():
            tickets = tickets.filter(
                department_id=int(selected_department)
            )
        else:
            selected_department = ''
    else:
        selected_department = ''

    # Filter by complaint division, if valid.
    if selected_division in ['employee', 'customer']:
        tickets = tickets.filter(
            division=selected_division
        )
    else:
        selected_division = ''


    # Company-wide weekly trends: current week and
    # the three preceding weeks.
    today = timezone.localdate()
    current_week_start = today - timedelta(days=today.weekday())

    admin_trend_labels = []
    admin_trend_received = []
    admin_trend_resolved = []

    for weeks_ago in range(3, -1, -1):
        week_start = current_week_start - timedelta(weeks=weeks_ago)
        week_end = week_start + timedelta(weeks=1)

        received_count = tickets.filter(
            created_at__date__gte=week_start,
            created_at__date__lt=week_end,
        ).count()

        resolved_count = tickets.filter(
            resolved_at__date__gte=week_start,
            resolved_at__date__lt=week_end,
        ).count()

        admin_trend_labels.append(week_start.strftime('%d %b'))
        admin_trend_received.append(received_count)
        admin_trend_resolved.append(resolved_count)


    # Company-wide complaint status distribution.
    admin_status_labels = [
        label for value, label in Ticket.STATUS_CHOICES
    ]

    admin_status_counts = [
        tickets.filter(status=value).count()
        for value, label in Ticket.STATUS_CHOICES
    ]



    # Department-wise complaint distribution.
    departments = Department.objects.order_by('name')

    department_chart_labels = []
    department_chart_counts = []

    for department in departments:
        department_chart_labels.append(department.name)
        department_chart_counts.append(
            tickets.filter(department=department).count()
        )

    # Complaints awaiting department routing.
    unrouted_count = tickets.filter(
        department__isnull=True
    ).count()

    if unrouted_count:
        department_chart_labels.append('Not Yet Routed')
        department_chart_counts.append(unrouted_count)


    total_tickets = tickets.count()

    employee_tickets = tickets.filter(
        division='employee'
    ).count()

    customer_tickets = tickets.filter(
        division='customer'
    ).count()

    unassigned_tickets = tickets.filter(
        assigned_to__isnull=True,
        status__in=['submitted', 'reopened']
    ).count()

    resolved_tickets = tickets.filter(
        status='resolved'
    ).count()

    closed_tickets = tickets.filter(
        status='closed'
    ).count()

    return render(request, 'role_dashboard.html', {
        'page_title': 'Admin Dashboard',
        'admin_total': total_tickets,
        'admin_employee_total': employee_tickets,
        'admin_customer_total': customer_tickets,
        'admin_unassigned': unassigned_tickets,
        'admin_resolved': resolved_tickets,
        'admin_closed': closed_tickets,
        'department_chart_labels': department_chart_labels,
        'department_chart_counts': department_chart_counts,
        'admin_status_labels': admin_status_labels,
        'admin_status_counts': admin_status_counts,
        'admin_trend_labels': admin_trend_labels,
        'admin_trend_received': admin_trend_received,
        'admin_trend_resolved': admin_trend_resolved,
        'departments': Department.objects.order_by('name'),
        'selected_department': selected_department,
        'selected_division': selected_division,
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
            urgency_result = detect_complaint_urgency(ticket.description)
            ticket.urgency = urgency_result["urgency"]
            

            
            with transaction.atomic():
                ticket.save()

                TicketActivity.objects.create(
                    ticket=ticket,
                    actor=request.user,
                    action='created',
                    new_status='submitted',
                    description='Employee complaint submitted.'
                )


            messages.success(
                request,
                f'Complaint #{ticket.pk} submitted successfully. '
                #f'Suggested urgency: {urgency_result["urgency"].title()}. '
                #f'{urgency_result["reason"]}'
            )

            return redirect('employee_my_tickets')

    else:
        form = EmployeeComplaintForm()

    return render(request, 'tickets/employee_complaint_form.html', {
        'form': form
    })
#function to view employee tickets

@require_POST
@login_required
def suggest_ticket_category(request):
    """
    Return an AI category suggestion without saving a ticket.
    """

    division = request.user.role

    if division not in ("employee", "customer"):
        return JsonResponse(
            {"error": "This action is not available for your role."},
            status=403,
        )

    description = request.POST.get("description", "")

    prediction, error = suggest_complaint_category(
        description,
        division,
    )

    if error:
        return JsonResponse(
            {"error": error},
            status=400,
        )

    category_name = prediction["suggested_category"]

    if not validate_suggested_category(category_name, division):
        return JsonResponse(
            {"error": "Suggested category is not available."},
            status=400,
        )

    category = Category.objects.get(
        name=category_name,
        division=division,
    )

    assessment = assess_category_suggestion(prediction)

    return JsonResponse({
        "category_id": category.pk,
        "category_name": category.name,
        "similarity_score": prediction["similarity_score"],
        "alternatives": prediction["alternatives"],
        "needs_review": assessment["needs_review"],
        "reason": assessment["reason"],
    })


# Step 65: Shared search and filters for reporter ticket lists

def apply_reporter_ticket_filters(request, tickets):

    search_query = request.GET.get('q', '').strip()
    selected_status = request.GET.get('status', '')

    valid_statuses = {
        value for value, label in Ticket.STATUS_CHOICES
    }

    if selected_status not in valid_statuses:
        selected_status = ''

    def valid_date(value):
        try:
            parsed = date.fromisoformat(value)
            if parsed.isoformat() == value:
                return parsed
        except (TypeError, ValueError):
            pass
        return None

    from_date = valid_date(request.GET.get('date_from', ''))
    to_date = valid_date(request.GET.get('date_to', ''))

    if search_query:
        candidate = (
            search_query[1:]
            if search_query.startswith('#')
            else search_query
        )

        if (
            candidate.isascii()
            and candidate.isdigit()
            and len(candidate) <= 18
        ):
            tickets = tickets.filter(
                Q(title__icontains=search_query)
                | Q(pk=int(candidate))
            )
        else:
            tickets = tickets.filter(
                title__icontains=search_query
            )

    if selected_status:
        tickets = tickets.filter(status=selected_status)

    if from_date:
        tickets = tickets.filter(
            created_at__date__gte=from_date
        )

    if to_date:
        tickets = tickets.filter(
            created_at__date__lte=to_date
        )

    date_from_value = (
        from_date.isoformat() if from_date else ''
    )
    date_to_value = (
        to_date.isoformat() if to_date else ''
    )

    filters = {
        'search_query': search_query,
        'selected_status': selected_status,
        'status_choices': Ticket.STATUS_CHOICES,
        'date_from': date_from_value,
        'date_to': date_to_value,
        'filters_applied': bool(
            search_query
            or selected_status
            or from_date
            or to_date
        ),
    }

    return tickets, filters


@role_required('employee')
def employee_my_tickets(request):

    tickets = Ticket.objects.filter(
        reporter=request.user,
        division='employee'
    ).select_related(
        'category', 'department'
    ).order_by('-created_at')

    tickets, filters = apply_reporter_ticket_filters(
        request, tickets
    )

    return render(
        request,
        'tickets/employee_my_tickets.html',
        {
            'tickets': tickets,
            'reset_url': 'employee_my_tickets',
            **filters,
        }
    )


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
            urgency_result = detect_complaint_urgency(ticket.description)
            ticket.urgency = urgency_result["urgency"]

           
            
            with transaction.atomic():
                ticket.save()

                TicketActivity.objects.create(
                    ticket=ticket,
                    actor=request.user,
                    action='created',
                    new_status='submitted',
                    description='Customer complaint submitted.'
                )


            messages.success(
                request,
                f'Complaint #{ticket.pk} submitted successfully. '
                f'Suggested urgency: {urgency_result["urgency"].title()}. '
                f'{urgency_result["reason"]}'
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

    tickets, filters = apply_reporter_ticket_filters(
        request, tickets
    )

    return render(
        request,
        'tickets/customer_my_tickets.html',
        {
            'tickets': tickets,
            'reset_url': 'customer_my_tickets',
            **filters,
        }
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
            'activities': ticket.activities.select_related('actor').all(),
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

        # AI suggestions restricted to the Support Staff department.
    similar_complaints, similarity_error = find_similar_complaints(
        ticket,
        limit=5,
        min_similarity=0.60,
        department_id=request.user.department_id,
    )

    if similarity_error:
        similar_complaints = []

    # The similarity service compares tickets by division.
    # Apply department restrictions before displaying results.
        # The similarity service compares tickets by division.
    # Apply department restrictions before displaying results.
    permitted_ids = set(
        Ticket.objects.filter(
            department_id=request.user.department_id
        ).values_list('pk', flat=True)
    )

    similar_complaints = [
        match for match in similar_complaints
        if match['ticket_id'] in permitted_ids
    ]

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
            'activities': ticket.activities.select_related('actor').all(),
            'similar_complaints': similar_complaints,
        }
    )


# Step 75: Resolve an assigned complaint

@role_required('support')
@require_POST
def resolve_support_ticket(request, ticket_id):

    ticket = get_object_or_404(
        Ticket,
        pk=ticket_id,
        department_id=request.user.department_id,
        assigned_to=request.user,
        status='in_progress'
    )

    form = TicketResolutionForm(request.POST)

    if not form.is_valid():
        messages.error(
            request,
            'Enter a valid resolution summary.'
        )
        return redirect(
            'support_ticket_detail',
            ticket_id=ticket_id
        )

    resolved_time = timezone.now()


    with transaction.atomic():

        updated = Ticket.objects.filter(
            pk=ticket.pk,
            department_id=request.user.department_id,
            assigned_to=request.user,
            status='in_progress'
        ).update(
            status='resolved',
            resolution_summary=form.cleaned_data[
                'resolution_summary'
            ],
            resolved_at=resolved_time,
            updated_at=resolved_time
        )

        if updated:
            activity = TicketActivity.objects.create(
                ticket=ticket,
                actor=request.user,
                action='resolved',
                old_status='in_progress',
                new_status='resolved',
                description='Support Staff resolved the ticket.'
            )

            create_notification(
                recipient=ticket.reporter,
                ticket=ticket,
                message=(
                    f'Ticket #{ticket.pk} has been resolved. '
                    'Please review and confirm the resolution.'
                ),
                event_key=f'ticket_activity_{activity.pk}_resolved'
            )



    if updated:
        messages.success(
            request,
            f'Ticket #{ticket_id} marked as Resolved.'
        )
    else:
        messages.warning(
            request,
            'This ticket can no longer be resolved.'
        )


    return redirect(
        'support_ticket_detail',
        ticket_id=ticket_id
    )

# Step 77: Reporter reopens an unresolved complaint

@role_required('employee', 'customer')
@require_POST
def reopen_ticket(request, ticket_id):

    ticket = get_object_or_404(
        Ticket,
        pk=ticket_id,
        reporter=request.user
    )

    form = TicketReopeningForm(request.POST)

    if not form.is_valid():
        messages.error(
            request,
            'A valid reopening reason is required.'
        )
        return redirect(
            'ticket_detail',
            ticket_id=ticket_id
        )

    with transaction.atomic():

        previous_assignee = ticket.assigned_to
        updated = Ticket.objects.filter(
            pk=ticket.pk,
            reporter=request.user,
            status='resolved'
        ).update(
            status='reopened',
            assigned_to=None,
            updated_at=timezone.now()
        )

        if updated:


            activity = TicketActivity.objects.create(
                ticket=ticket,
                actor=request.user,
                action='reopened',
                old_status='resolved',
                new_status='reopened',
                description=(
                    'Reporter reopened the ticket. Reason: '
                    + form.cleaned_data['reopening_reason']
                )
            )

            TicketMessage.objects.create(
                ticket=ticket,
                author=request.user,
                body=(
                    'Reopening reason: '
                    + form.cleaned_data['reopening_reason']
                ),
                is_internal=False
            )
            if previous_assignee:
                create_notification(
                    recipient=previous_assignee,
                    ticket=ticket,
                    message=(
                        f'Ticket #{ticket.pk} has been reopened '
                        'and returned to the department queue.'
                    ),
                    event_key=f'ticket_activity_{activity.pk}_reopened'
                )

    if updated:
        messages.success(
            request,
            'Ticket reopened successfully.'
        )
    else:
        messages.warning(
            request,
            'Only resolved tickets can be reopened.'
        )

    return redirect(
        'ticket_detail',
        ticket_id=ticket_id
    )


# Step 76: Reporter confirms ticket resolution

@role_required('employee', 'customer')
@require_POST
def confirm_ticket_resolution(request, ticket_id):

    ticket = get_object_or_404(
        Ticket,
        pk=ticket_id,
        reporter=request.user
    )


    with transaction.atomic():

        updated = Ticket.objects.filter(
            pk=ticket.pk,
            reporter=request.user,
            status='resolved'
        ).update(
            status='closed',
            updated_at=timezone.now()
        )

    if updated:
        activity = TicketActivity.objects.create(
                ticket=ticket,
                actor=request.user,
                action='closed',
                old_status='resolved',
                new_status='closed',
                description='Reporter confirmed the resolution.'
        )


        if ticket.assigned_to_id:
            create_notification(
                recipient=ticket.assigned_to,
                ticket=ticket,
                message=(
                    f'Ticket #{ticket.pk} has been closed. '
                    'The reporter confirmed the resolution.'
                ),
                event_key=f'ticket_activity_{activity.pk}_closed'
            )



        messages.success(
            request,
            'Resolution confirmed. Ticket closed.'
        )
    else:
        messages.warning(
            request,
            'This ticket is not awaiting resolution confirmation.'
        )

    return redirect(
        'ticket_detail',
        ticket_id=ticket_id
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
    
    # Prevent access to tickets outside the staff member's department.
    get_object_or_404(
        Ticket,
        pk=ticket_id,
        department_id=request.user.department_id
    )


    
    previous_status = Ticket.objects.filter(
        pk=ticket_id,
        department_id=request.user.department_id,
        assigned_to__isnull=True,
        status__in=['submitted', 'reopened']
    ).values_list('status', flat=True).first()


    # Conditional update prevents two staff members
    # from successfully claiming the same ticket.

    
    with transaction.atomic():

        previous_status = Ticket.objects.filter(
            pk=ticket_id,
            department_id=request.user.department_id,
            assigned_to__isnull=True,
            status__in=['submitted', 'reopened']
        ).values_list('status', flat=True).first()

        updated = Ticket.objects.filter(
            pk=ticket_id,
            department_id=request.user.department_id,
            assigned_to__isnull=True,
            status__in=['submitted', 'reopened']
        ).update(
            assigned_to=request.user,
            status='in_progress',
            updated_at=timezone.now()
        )

        if updated:
            TicketActivity.objects.create(
                ticket_id=ticket_id,
                actor=request.user,
                action='claimed',
                old_status=previous_status or '',
                new_status='in_progress',
                description='Ticket claimed by Support Staff.'
            )
        create_notification(
            recipient=request.user,
            ticket=Ticket.objects.get(pk=ticket_id),
            message=f'Ticket #{ticket_id} has been assigned to you.',
            event_key=f'ticket_{ticket_id}_claimed'
        )


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
        if ticket.assigned_to_id:
            create_notification(
                recipient=ticket.assigned_to,
                ticket=ticket,
                message=f'New public reply on Ticket #{ticket.pk}.',
                event_key=f'ticket_message_{message.pk}'
    )

        Ticket.objects.filter(pk=ticket.pk).update(
            updated_at=message.created_at
        )

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
            if not message.is_internal:
                create_notification(
                    recipient=ticket.reporter,
                    ticket=ticket,
                    message=f'New Support Staff reply on Ticket #{ticket.pk}.',
                    event_key=f'ticket_message_{message.pk}'
    )
            if not message.is_internal:
                Ticket.objects.filter(pk=ticket.pk).update(
                    updated_at=message.created_at
                )

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


# Step 71: Admin overview of all complaints


@role_required('admin')
def admin_all_complaints(request):
    search_query = request.GET.get('q', '').strip()

    tickets = Ticket.objects.select_related(
        'reporter',
        'category',
        'department',
        'assigned_to',
        'product'
    ).order_by('-created_at', '-pk')

    if search_query:
        ticket_id = search_query.lstrip('#')

        if ticket_id.isdigit():
            tickets = tickets.filter(
                Q(pk=int(ticket_id)) |
                Q(title__icontains=search_query)
            )
        else:
            tickets = tickets.filter(
            title__icontains=search_query
    )   

    # Module 13: Advanced complaint filters
    selected_status = request.GET.get('status', '')
    selected_department = request.GET.get('department', '')
    selected_division = request.GET.get('division', '')
    selected_category = request.GET.get('category', '')
    selected_urgency = request.GET.get('urgency', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')

    if selected_status in dict(Ticket.STATUS_CHOICES):
        tickets = tickets.filter(status=selected_status)

    if selected_department.isdigit():
        tickets = tickets.filter(department_id=int(selected_department))

    if selected_division in dict(Ticket.DIVISION_CHOICES):
        tickets = tickets.filter(division=selected_division)

    if selected_category.isdigit():
        tickets = tickets.filter(category_id=int(selected_category))

    if selected_urgency in dict(Ticket.URGENCY_CHOICES):
        tickets = tickets.filter(urgency=selected_urgency)

    from datetime import date

    try:
        if date_from:
            tickets = tickets.filter(
                created_at__date__gte=date.fromisoformat(date_from)
            )
    except ValueError:
        date_from = ''

    try:
        if date_to:
            tickets = tickets.filter(
                created_at__date__lte=date.fromisoformat(date_to)
            )
    except ValueError:
        date_to = ''

    return render(
        request,
        'tickets/admin_all_complaints.html',
        {
            'tickets': tickets,
            'departments': Department.objects.order_by('name'),
            'search_query': search_query,

            'categories': Category.objects.order_by('name'),
            'status_choices': Ticket.STATUS_CHOICES,
            'division_choices': Ticket.DIVISION_CHOICES,
            'urgency_choices': Ticket.URGENCY_CHOICES,
            'selected_status': selected_status,
            'selected_department': selected_department,
            'selected_division': selected_division,
            'selected_category': selected_category,
            'selected_urgency': selected_urgency,
            'date_from': date_from,
            'date_to': date_to,

        }
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


# Step 80: Admin department correction

@role_required('admin')
@require_POST
def correct_ticket_department(request, ticket_id):

    department = get_object_or_404(
        Department,
        pk=request.POST.get('department')
    )

    with transaction.atomic():

        ticket = get_object_or_404(
            Ticket.objects.select_for_update(),
            pk=ticket_id
        )

        previous_department = ticket.department_id

        updated = Ticket.objects.filter(
            pk=ticket_id,
            assigned_to__isnull=True,
            status__in=['submitted', 'reopened'],
            department__isnull=False
        ).exclude(
            department=department
        ).update(
            department=department,
            updated_at=timezone.now()
        )

        if updated:
            TicketActivity.objects.create(
                ticket=ticket,
                actor=request.user,
                action='department_corrected',
                description=(
                    f'Department changed from ID '
                    f'{previous_department} to {department.name}.'
                )
            )

    if updated:
        messages.success(
            request,
            'Ticket department corrected successfully.'
        )
    else:
        messages.error(
            request,
            'Department correction is not allowed for this ticket.'
        )

    return redirect('admin_all_complaints')


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

            
            with transaction.atomic():

                updated = Ticket.objects.filter(
                    pk=ticket.pk,
                    department__isnull=True,
                    assigned_to__isnull=True,
                    status__in=['submitted', 'reopened']
                ).update(
                    department_id=department.pk,
                    updated_at=timezone.now()
                )


                if updated:
                    TicketActivity.objects.create(
                        ticket=ticket,
                        actor=request.user,
                        action='department_routed',
                        description=(
                            f'Ticket routed to {department.name}.'
                        )
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


# Step 54: Admin software product management

@role_required('admin')
def manage_products(request):

    if request.method == 'POST':
        form = ProductForm(request.POST)

        if form.is_valid():
            product = form.save()

            messages.success(
                request,
                f'{product.name} added successfully.'
            )

            return redirect('manage_products')

    else:
        form = ProductForm()

    products = Product.objects.order_by(
        'name',
        'pk'
    )

    return render(
        request,
        'tickets/admin_products.html',
        {
            'form': form,
            'products': products,
        }
    )


# Step 55: Edit software product

@role_required('admin')
def edit_product(request, product_id):

    product = get_object_or_404(
        Product,
        pk=product_id
    )

    if request.method == 'POST':
        form = ProductForm(
            request.POST,
            instance=product
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Software product updated successfully.'
            )

            return redirect('manage_products')

    else:
        form = ProductForm(instance=product)

    return render(
        request,
        'tickets/admin_product_edit.html',
        {
            'form': form,
            'product': product,
        }
    )


# Step 55: Activate or deactivate product

@role_required('admin')
@require_POST
def toggle_product_status(request, product_id):

    product = get_object_or_404(
        Product,
        pk=product_id
    )

    product.is_active = not product.is_active

    product.save(
        update_fields=['is_active']
    )

    status = (
        'activated'
        if product.is_active
        else 'deactivated'
    )

    messages.success(
        request,
        f'{product.name} {status} successfully.'
    )

    return redirect('manage_products')


@login_required
def notification_list(request):

    notifications = Notification.objects.filter(
        recipient=request.user
    )

    unread_count = notifications.filter(
        is_read=False
    ).count()

    return render(
        request,
        'tickets/notification_list.html',
        {
            'notifications': notifications,
            'unread_count': unread_count,
        }
    )



@login_required
@require_POST
def mark_notification_read(request, notification_id):

    notification = get_object_or_404(
        Notification,
        pk=notification_id,
        recipient=request.user
    )

    if not notification.is_read:
        notification.is_read = True
        notification.save(update_fields=['is_read'])

    return redirect('notification_list')


@role_required('support')
@require_POST
def escalate_support_ticket(request, ticket_id):

    ticket = get_object_or_404(
        Ticket,
        pk=ticket_id,
        assigned_to=request.user,
        department_id=request.user.department_id,
        status='in_progress'
    )

    with transaction.atomic():
        updated = Ticket.objects.filter(
            pk=ticket.pk,
            assigned_to=request.user,
            status='in_progress'
        ).update(
            updated_at=timezone.now()
        )

        
        if updated:
            activity, created = TicketActivity.objects.get_or_create(
                ticket=ticket,
                action='escalated',
                defaults={
                    'actor': request.user,
                    'description': (
                        'Ticket escalated for further technical review.'
                    )
                }
            )

            if created:
                create_notification(
                    recipient=ticket.reporter,
                    ticket=ticket,
                    message=(
                        f'Ticket #{ticket.pk} has been escalated '
                        'for further technical review.'
                    ),
                    event_key=f'ticket_activity_{activity.pk}_escalated'
                )
       

    messages.success(
        request,
        'Ticket escalation recorded successfully.'
    )

    return redirect(
        'support_ticket_detail',
        ticket_id=ticket_id
    )



# Module 11 — Incident management

@role_required('support')
def support_incident_list(request):
    incidents = Incident.objects.filter(
        department_id=request.user.department_id
    ).select_related('owner').prefetch_related(
        'tickets'
    ).order_by('-created_at')

    return render(
        request,
        'tickets/support_incident_list.html',
        {'incidents': incidents},
    )


@role_required('support')
def support_incident_detail(request, incident_id):
    # Step 204 — searchable incident candidates and AI suggestions.
    incident = get_object_or_404(
        Incident.objects.select_related('owner', 'department'),
        pk=incident_id,
        department_id=request.user.department_id,
    )
    linked_tickets = incident.tickets.select_related(
        'assigned_to', 'reporter'
    ).order_by('pk')

    # Only unlinked complaints in this department may be selected.
    available = Ticket.objects.filter(
        department_id=incident.department_id,
    ).exclude(incidents__isnull=False)

    query = request.GET.get('q', '').strip()[:100]
    search_results = []
    if query:
        conditions = Q(title__icontains=query) | Q(description__icontains=query)
        candidate_id = query.lstrip('#')
        if candidate_id.isascii() and candidate_id.isdecimal() and len(candidate_id) <= 18:
            conditions |= Q(pk=int(candidate_id))
        search_results = list(
            available.filter(conditions).order_by('-created_at')[:20]
        )

    ai_suggestions = []
    ai_error = None
    anchor = linked_tickets.first()
    if anchor:
        matches, ai_error = find_similar_complaints(
            anchor, limit=10, min_similarity=0.60,
            department_id=incident.department_id,
        )
        if matches:
            allowed = set(available.values_list('pk', flat=True))
            ai_suggestions = [m for m in matches if m['ticket_id'] in allowed]

    return render(request, 'tickets/support_incident_detail.html', {
        'incident': incident,
        'linked_tickets': linked_tickets,
        'search_query': query,
        'search_results': search_results,
        'ai_suggestions': ai_suggestions,
        'ai_error': ai_error,
        'investigation_updates': incident.investigation_updates.select_related(
    'author'
    ),
    })


@role_required('support')
@require_POST
def support_create_incident(request, ticket_id):
    ticket = get_object_or_404(
        Ticket,
        pk=ticket_id,
        department_id=request.user.department_id,
    )

    try:
        incident = create_incident(
            user=request.user,
            title=request.POST.get('title', ''),
            description=request.POST.get('description', ''),
            ticket=ticket,
        )
    except (ValidationError, IntegrityError) as exc:
        if isinstance(exc, ValidationError):
            error = '; '.join(exc.messages)
        else:
            error = 'This complaint is already linked to an incident.'
        messages.error(request, error)
        return redirect('support_ticket_detail', ticket_id=ticket.pk)

    messages.success(request, 'Incident created successfully.')
    return redirect('support_incident_detail', incident_id=incident.pk)


@role_required('support')
@require_POST
def support_link_incident_ticket(request, incident_id):
    incident = get_object_or_404(
        Incident,
        pk=incident_id,
        department_id=request.user.department_id,
    )

    # Accept only IDs chosen from the rendered suggestions/search results.
    raw_ids = request.POST.getlist('ticket_ids')
    if not raw_ids or len(raw_ids) > 20 or any(
        not value.isascii() or not value.isdecimal() or len(value) > 18
        for value in raw_ids
    ):
        messages.error(request, 'Select one or more valid complaints (maximum 20).')
        return redirect('support_incident_detail', incident_id=incident.pk)

    ids = [int(value) for value in raw_ids]
    if len(set(ids)) != len(ids):
        messages.error(request, 'Select each complaint only once.')
        return redirect('support_incident_detail', incident_id=incident.pk)

    tickets = list(Ticket.objects.filter(
        pk__in=ids, department_id=incident.department_id,
    ))
    if len(tickets) != len(ids):
        messages.error(request, 'One or more selected complaints are unavailable.')
        return redirect('support_incident_detail', incident_id=incident.pk)

    try:
        # One transaction: do not partially link a batch on validation failure.
        with transaction.atomic():
            for ticket in tickets:
                link_ticket_to_incident(
                    user=request.user, incident=incident, ticket=ticket,
                )
    except (ValidationError, IntegrityError) as exc:
        if isinstance(exc, ValidationError):
            error = '; '.join(exc.messages)
        else:
            error = 'A selected complaint is already linked to an incident.'
        messages.error(request, error)
    else:
        messages.success(request, f'{len(tickets)} complaint(s) linked successfully.')

    return redirect('support_incident_detail', incident_id=incident.pk)


# Step 205 — Incident progress tracking

@role_required('support')
@require_POST
def support_update_incident_status(request, incident_id):
    redirect_url = 'support_incident_detail'

    with transaction.atomic():
        incident = get_object_or_404(
            Incident.objects.select_for_update(),
            pk=incident_id,
            department_id=request.user.department_id,
        )

        if incident.owner_id != request.user.pk:
            messages.error(
                request,
                'Only the incident owner can update its status.'
            )
            return redirect(redirect_url, incident_id=incident.pk)

        transitions = {
            'open': 'in_progress',
            'in_progress': 'resolved',
        }

        new_status = request.POST.get('status', '')

        if transitions.get(incident.status) != new_status:
            messages.error(
                request,
                'Invalid incident status transition.'
            )
            return redirect(redirect_url, incident_id=incident.pk)

        if new_status == 'resolved':
            summary = request.POST.get(
                'resolution_summary', ''
            ).strip()

            if not summary or len(summary) > 2000:
                messages.error(
                    request,
                    'Enter a resolution summary of 1–2000 characters.'
                )
                return redirect(redirect_url, incident_id=incident.pk)

            incident.resolution_summary = summary
            incident.status = 'resolved'
            incident.save(
                update_fields=[
                    'status',
                    'resolution_summary',
                    'updated_at',
                ]
            )

            public_text = (
                f'Incident #{incident.pk} — {incident.title} '
                f'has been resolved.\n'
                f'Resolution summary: {summary}\n\n'
                'This is an incident-level update. '
                'The linked complaint must still be handled '
                'individually by its assigned Support Staff.'
            )

            linked_tickets = incident.tickets.select_related(
                'reporter', 'assigned_to'
            )

            for ticket in linked_tickets:
                TicketMessage.objects.create(
                    ticket=ticket,
                    author=request.user,
                    body=public_text,
                    is_internal=False,
                )

                recipients = {
                    ticket.reporter_id: ticket.reporter,
                }

                if ticket.assigned_to_id:
                    recipients[ticket.assigned_to_id] = ticket.assigned_to

                for recipient in recipients.values():
                    create_notification(
                        recipient=recipient,
                        ticket=ticket,
                        message=(
                            f'Incident #{incident.pk} resolved. '
                            f'Review the update on Ticket #{ticket.pk}.'
                        ),
                        event_key=(
                            f'incident_{incident.pk}_'
                            f'resolved_ticket_{ticket.pk}'
                        ),
                    )

        else:
            incident.status = new_status
            incident.save(update_fields=['status', 'updated_at'])

    messages.success(
        request,
        'Incident status updated successfully.'
    )

    return redirect(redirect_url, incident_id=incident_id)



@role_required('support')
@require_POST
def support_add_incident_update(request, incident_id):
    incident = get_object_or_404(
        Incident,
        pk=incident_id,
        department_id=request.user.department_id,
    )

    if incident.owner_id != request.user.pk:
        messages.error(request, 'Only the incident owner can add updates.')
    elif incident.status == 'resolved':
        messages.error(request, 'Resolved incidents cannot receive investigation updates.')
    else:
        body = request.POST.get('body', '').strip()

        if not body or len(body) > 2000:
            messages.error(request, 'Enter an update of 1–2000 characters.')
        else:
            IncidentUpdate.objects.create(
                incident=incident,
                author=request.user,
                body=body,
            )
            messages.success(request, 'Investigation update recorded.')

    return redirect('support_incident_detail', incident_id=incident.pk)



@role_required('support')
def support_recurring_product_issues(request):
    if not request.user.department_id:
        messages.warning(
            request,
            'Your account has no support department assigned.'
        )
        return redirect('support_dashboard')
    if request.user.department.name != 'Product Support':
        messages.error(
            request,
            'Only Product Support Staff can access recurring product issues.'
        )
        return redirect('support_dashboard')

    department_id = request.user.department_id

    products = get_recurring_product_issues(
        department_id=department_id
    )

    selected_product = None
    groups = []
    analysis_error = None

    product_id = request.GET.get('product_id', '')
    other_product_name = request.GET.get(
        'other_product_name', ''
    ).strip()

    if product_id.isdecimal():
        selected_product = next(
            (
                product for product in products
                if product['product_id'] == int(product_id)
            ),
            None,
        )

        if selected_product:
            groups, analysis_error = get_recurring_issue_groups(
                product_id=int(product_id),
                department_id=department_id,
            )

    elif other_product_name:
        selected_product = next(
            (
                product for product in products
                if product['product_id'] is None
                and product['product_name'].casefold()
                == other_product_name.casefold()
            ),
            None,
        )

        if selected_product:
            groups, analysis_error = (
                get_recurring_other_product_issue_groups(
                    product_name=selected_product['product_name'],
                    department_id=department_id,
                )
            )

    if groups is None:
        groups = []

    return render(
        request,
        'tickets/support_recurring_product_issues.html',
        {
            'products': products,
            'selected_product': selected_product,
            'groups': groups,
            'analysis_error': analysis_error,
        },
    )

# Module 12: Admin announcement management

@role_required('admin')
def manage_announcements(request):

    if request.method == 'POST':
        form = AnnouncementForm(request.POST)

        if form.is_valid():
            announcement = form.save()

            messages.success(
                request,
                f'{announcement.title} added successfully.'
            )

            return redirect('manage_announcements')

    else:
        form = AnnouncementForm()

    announcements = Announcement.objects.all()

    return render(
        request,
        'tickets/admin_announcements.html',
        {
            'announcements': announcements,
            'form': form,
        }
    )

# Module 12: Edit announcement

@role_required('admin')
def edit_announcement(request, announcement_id):

    announcement = get_object_or_404(
        Announcement,
        pk=announcement_id
    )

    if request.method == 'POST':
        form = AnnouncementForm(
            request.POST,
            instance=announcement
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Announcement updated successfully.'
            )

            return redirect('manage_announcements')

    else:
        form = AnnouncementForm(instance=announcement)

    return render(
        request,
        'tickets/admin_announcement_edit.html',
        {
            'form': form,
            'announcement': announcement,
        }
    )

# Module 12: Delete public announcement

@role_required('admin')
@require_POST
def delete_announcement(request, announcement_id):

    announcement = get_object_or_404(
        Announcement,
        pk=announcement_id
    )

    title = announcement.title
    announcement.delete()

    messages.success(
        request,
        f'{title} deleted successfully.'
    )

    return redirect('manage_announcements')
