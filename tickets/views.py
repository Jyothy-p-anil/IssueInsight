from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.decorators import role_required

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
