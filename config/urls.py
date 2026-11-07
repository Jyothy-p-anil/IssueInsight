
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from tickets import views
from accounts import views as account_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
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
    auth_views.LogoutView.as_view(),
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


]
