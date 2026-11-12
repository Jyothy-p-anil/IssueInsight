
from tickets.models import Notification


def create_notification(recipient, ticket, message, event_key):
    """
    Create one notification per recipient and event.
    """

    notification, created = Notification.objects.get_or_create(
        recipient=recipient,
        ticket=ticket,
        event_key=event_key,
        defaults={
            'message': message,
        }
    )

    return notification, created
