
from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def role_required(*allowed_roles):

    def decorator(view_func):

        @login_required
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):

            user = request.user

            if user.is_superuser or user.role in allowed_roles:
                return view_func(request, *args, **kwargs)

            messages.error(
                request,
                'You do not have permission to access that page.'
            )

            return redirect('dashboard_redirect')

        return wrapped_view

    return decorator
