
from django.db.models import Count, Q

from tickets.models import Ticket

import numpy as np

from tickets.services.ai_embeddings import generate_complaint_embedding


def get_recurring_product_issues(min_complaints=2, department_id=None):
    customer_tickets = Ticket.objects.filter(division='customer')

    if department_id is not None:
        customer_tickets = customer_tickets.filter(
            department_id=department_id
        )

    recurring_products = (
        customer_tickets
        .filter(product__isnull=False)
        .values('product_id', 'product__name')
        .annotate(complaint_count=Count('id'))
        .filter(complaint_count__gte=min_complaints)
        .order_by('-complaint_count', 'product__name')
    )

    results = [
        {
            'product_id': item['product_id'],
            'product_name': item['product__name'],
            'complaint_count': item['complaint_count'],
        }
        for item in recurring_products
    ]

    other_products = (
        customer_tickets
        .filter(product__isnull=True)
        .exclude(
            Q(other_product_name__isnull=True)
            | Q(other_product_name='')
        )
        .values('other_product_name')
        .annotate(complaint_count=Count('id'))
        .filter(complaint_count__gte=min_complaints)
        .order_by('-complaint_count', 'other_product_name')
    )

    for item in other_products:
        results.append({
            'product_id': None,
            'product_name': item['other_product_name'],
            'complaint_count': item['complaint_count'],
        })

    return sorted(
        results,
        key=lambda item: (
            -item['complaint_count'],
            item['product_name'],
        ),
    )


def get_recurring_issue_groups(
    product_id,
    min_complaints=2,
    similarity_threshold=0.70,
    department_id=None,
):
    """
    Group Customer complaints about the same registered
    product when their descriptions are semantically similar.

    Returns (groups, error).
    """

    tickets_query = Ticket.objects.filter(
    division='customer',
    product_id=product_id,
)

    if department_id is not None:
        tickets_query = tickets_query.filter(
        department_id=department_id
    )

    tickets = list(
        tickets_query.order_by('created_at', 'pk')
    )

    if len(tickets) < min_complaints:
        return [], None

    vectors = []
    valid_tickets = []

    for ticket in tickets:
        vector, error = generate_complaint_embedding(
            ticket.description
        )

        if error:
            return None, error

        valid_tickets.append(ticket)
        vectors.append(vector)

    groups = []
    assigned_ids = set()

    for index, anchor in enumerate(valid_tickets):
        if anchor.pk in assigned_ids:
            continue

        members = [anchor]
        assigned_ids.add(anchor.pk)

        for other_index in range(index + 1, len(valid_tickets)):
            candidate = valid_tickets[other_index]

            if candidate.pk in assigned_ids:
                continue

            score = float(
                np.dot(vectors[index], vectors[other_index])
            )

            if score >= similarity_threshold:
                members.append(candidate)
                assigned_ids.add(candidate.pk)

        if len(members) >= min_complaints:
            groups.append({
                'summary': anchor.title,
                'complaint_count': len(members),
                'ticket_ids': [ticket.pk for ticket in members],
                'statuses': [ticket.status for ticket in members],
            })

    groups.sort(
        key=lambda group: -group['complaint_count']
    )

    return groups, None
