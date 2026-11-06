
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

]
