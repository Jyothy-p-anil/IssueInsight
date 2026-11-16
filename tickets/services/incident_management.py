from django.core.exceptions import ValidationError
from django.db import transaction

from tickets.models import Incident, Ticket


@transaction.atomic
def create_incident(*, user, title, description, ticket):
    """
    Create an incident owned by the Support Staff creator.
    Link the initial complaint without changing its assignment.
    """

    if not user.is_authenticated or user.role != "support":
        raise ValidationError(
            "Only Support Staff can create incidents."
        )

    if not user.department_id:
        raise ValidationError(
            "Support Staff must belong to a department."
        )

    if not isinstance(ticket, Ticket) or not ticket.pk:
        raise ValidationError(
            "A saved complaint is required."
        )

    if ticket.department_id != user.department_id:
        raise ValidationError(
            "The complaint belongs to another department."
        )

    if not title or not title.strip():
        raise ValidationError(
            "Incident title is required."
        )

    if not description or not description.strip():
        raise ValidationError(
            "Incident description is required."
        )
    # Prevent creating another incident for an already-linked ticket.
    if Incident.objects.filter(tickets=ticket).exists():
        raise ValidationError(
            "This complaint is already linked to an incident."
        )

    incident = Incident.objects.create(
        title=title.strip(),
        description=description.strip(),
        department_id=user.department_id,
        owner=user,
    )

    incident.tickets.add(ticket)

    return incident

@transaction.atomic
def link_ticket_to_incident(*, user, incident, ticket):
    """
    Link an additional complaint to an existing incident.
    Preserve the complaint's assignment and status.
    """

    if not user.is_authenticated or user.role != "support":
        raise ValidationError(
            "Only Support Staff can link complaints to incidents."
        )

    if not user.department_id:
        raise ValidationError(
            "Support Staff must belong to a department."
        )

    if not isinstance(incident, Incident) or not incident.pk:
        raise ValidationError(
            "A saved incident is required."
        )

    if not isinstance(ticket, Ticket) or not ticket.pk:
        raise ValidationError(
            "A saved complaint is required."
        )

    if incident.department_id != user.department_id:
        raise ValidationError(
            "The incident belongs to another department."
        )

    if ticket.department_id != incident.department_id:
        raise ValidationError(
            "The complaint belongs to another department."
        )

    if Incident.objects.filter(tickets=ticket).exists():
        raise ValidationError(
            "This complaint is already linked to an incident."
        )

    incident.tickets.add(ticket)

    return incident