
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from tickets import views
from accounts import views as account_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path(
    'dashboard/',
    views.dashboard_redirect,
    name='dashboard_redirect'
),
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='accounts/login.html',
            redirect_authenticated_user=True
        ),
        name='login'
    ),
   path(
    'logout/',
    auth_views.LogoutView.as_view(next_page='login'),
    name='logout'
),
    path('register/', account_views.register, name='register'),
    
path(
    'password-reset/',
    auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset_form.html'
    ),
    name='password_reset'
),

path(
    'password-reset/done/',
    auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ),
    name='password_reset_done'
),


path(
    'password-reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html'
    ),
    name='password_reset_confirm'
),

path(
    'password-reset/complete/',
    auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ),
    name='password_reset_complete'
),


    path(
        'employee/dashboard/',
        views.employee_dashboard,
        name='employee_dashboard'
    ),
    path(
        'customer/dashboard/',
        views.customer_dashboard,
        name='customer_dashboard'
    ),
    path(
        'support/dashboard/',
        views.support_dashboard,
        name='support_dashboard'
    ),
    path(
        'management/dashboard/',
        views.admin_dashboard,
        name='admin_dashboard'
    ),
    path(
    'management/users/',
    account_views.manage_users,
    name='manage_users'
),
path(
    'management/users/add/',
    account_views.create_staff_account,
    name='create_staff_account'
),
path(
    'management/users/<int:user_id>/edit/',
    account_views.edit_user,
    name='edit_user'
),
path(
    'management/users/<int:user_id>/status/',
    account_views.change_user_status,
    name='change_user_status'
),

# Employee Complaint Submission and Ticket Viewing URLs

path(
    'employee/complaints/new/',
    views.submit_employee_complaint,
    name='submit_employee_complaint'
),
path(
    'employee/tickets/',
    views.employee_my_tickets,
    name='employee_my_tickets'
),
]
