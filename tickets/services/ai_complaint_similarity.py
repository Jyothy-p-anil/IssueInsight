
import numpy as np

from tickets.models import Ticket
from tickets.services.ai_embeddings import generate_complaint_embedding


def find_similar_complaints(
    ticket, limit=5, min_similarity=0.60, department_id=None):
    """
    Find existing complaints with similar descriptions.

    Returns (matches, error).
    """

    if ticket.division not in {"employee", "customer"}:
        return None, "Invalid complaint division."

    complaint_vector, error = generate_complaint_embedding(
        ticket.description
    )

    if error:
        return None, error

    existing_tickets = (
        Ticket.objects
        .filter(division=ticket.division)
        .exclude(pk=ticket.pk)
        .order_by("-created_at")
    )
    if department_id is not None:
        existing_tickets = existing_tickets.filter(
            department_id=department_id
        )
    matches = []

    for existing_ticket in existing_tickets:
        existing_vector, existing_error = generate_complaint_embedding(
            existing_ticket.description
        )

        if existing_error:
            continue

        similarity = float(
            np.dot(complaint_vector, existing_vector)
        )

        if similarity >= min_similarity:
            matches.append({
                "ticket_id": existing_ticket.pk,
                "title": existing_ticket.title,
                "similarity_score": round(similarity, 4),
                "status": existing_ticket.status,
            })

    matches.sort(
        key=lambda item: item["similarity_score"],
        reverse=True
    )

    return matches[:limit], None

