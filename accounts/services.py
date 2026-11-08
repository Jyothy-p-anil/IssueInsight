
import logging

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import transaction
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


logger = logging.getLogger(__name__)


def send_password_setup_email(request, user):

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    path = reverse(
        'password_reset_confirm',
        kwargs={'uidb64': uid, 'token': token}
    )

    setup_link = request.build_absolute_uri(path)

    username = user.username
    email = user.email
    user_id = user.pk

    def send_email():
        try:
            send_mail(
                subject='Set Up Your IssueInsight Password',
                message=(
                    f'Hello {username},\n\n'
                    'Your IssueInsight account has been created.\n\n'
                    'Set your password using this link:\n'
                    f'{setup_link}\n\n'
                    'Thank you,\nIssueInsight Team'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception:
            logger.exception(
                'Password setup email failed for user %s',
                user_id
            )

    transaction.on_commit(send_email)


def send_account_status_email(user):

    if not user.email:
        return

    status = (
        'reactivated' if user.is_active
        else 'deactivated'
    )

    username = user.username
    email = user.email
    user_id = user.pk

    def send_email():
        try:
            send_mail(
                subject=f'IssueInsight Account {status.title()}',
                message=(
                    f'Hello {username},\n\n'
                    f'Your IssueInsight account has been '
                    f'{status}.\n\n'
                    'Thank you,\nIssueInsight Team'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception:
            logger.exception(
                'Account status email failed for user %s',
                user_id
            )

    transaction.on_commit(send_email)
