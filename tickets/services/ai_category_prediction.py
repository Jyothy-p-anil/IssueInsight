
import numpy as np

from tickets.services.ai_category_references import load_category_references
from tickets.services.ai_embeddings import generate_complaint_embedding


from tickets.models import Category

def suggest_complaint_category(description, division):
    """
    Suggest a category using semantic similarity.

    Returns (result, error).
    """

    if division not in {"employee", "customer"}:
        return None, "Invalid complaint division."

    complaint_vector, error = generate_complaint_embedding(
        description
    )

    if error:
        return None, error

    references = load_category_references()
    candidates = []

    for (ref_division, category), examples in references.items():
        if ref_division != division:
            continue

        scores = []

        for example in examples:
            example_vector, ref_error = generate_complaint_embedding(
                example
            )

            if ref_error:
                continue

            similarity = float(
                np.dot(complaint_vector, example_vector)
            )

            scores.append(similarity)

        if scores:
            candidates.append({
                "category": category,
                "score": round(max(scores), 4),
            })

    if not candidates:
        return None, "No category references available."

    candidates.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return {
        "suggested_category": candidates[0]["category"],
        "similarity_score": candidates[0]["score"],
        "alternatives": candidates[1:3],
    }, None


def validate_suggested_category(category_name, division):
    """
    Confirm the suggested category belongs
    to the correct complaint division.
    """

    if division not in {"employee", "customer"}:
        return False

    return Category.objects.filter(
        name=category_name,
        division=division
    ).exists()


def get_suggested_department(category_name, division):
    """
    Retrieve the department assigned to a category.

    Returns (department, error).
    """

    if division not in {"employee", "customer"}:
        return None, "Invalid complaint division."

    category = (
        Category.objects
        .select_related("department")
        .filter(
            name=category_name,
            division=division
        )
        .first()
    )

    if category is None:
        return None, "Category not found for this division."

    if category.department is None:
        return None, "No department assigned to this category."

    return category.department, None


MIN_SIMILARITY = 0.50
MIN_SCORE_GAP = 0.10


def assess_category_suggestion(prediction):
    if not prediction or not isinstance(prediction, dict):
        return {
            "needs_review": True,
            "reason": "No valid AI prediction available.",
        }

    top_score = prediction.get("similarity_score")
    alternatives = prediction.get("alternatives", [])

    if not isinstance(top_score, (int, float)):
        return {
            "needs_review": True,
            "reason": "Invalid similarity score.",
        }

    if top_score < MIN_SIMILARITY:
        return {
            "needs_review": True,
            "reason": "Low semantic similarity.",
        }

    if alternatives:
        second_score = alternatives[0].get("score")

        if not isinstance(second_score, (int, float)):
            return {
                "needs_review": True,
                "reason": "Invalid alternative score.",
            }

        if top_score - second_score < MIN_SCORE_GAP:
            return {
                "needs_review": True,
                "reason": "Multiple categories have similar scores.",
            }

    return {
        "needs_review": False,
        "reason": "Category suggestion meets initial thresholds.",
    }
