from tickets.models import Category


def get_suggestion_candidates(division):
    """
    Return valid complaint categories for a division.

    Future AI classification can use these candidates.
    This function does not predict a category.
    """

    if division not in ('employee', 'customer'):
        return Category.objects.none()

    return Category.objects.filter(
        division=division
    ).order_by('name')