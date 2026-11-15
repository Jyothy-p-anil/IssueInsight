
import csv
from collections import defaultdict

from tickets.services.ai_dataset_validation import DATASET_PATH
from tickets.services.ai_text_preprocessing import validate_ai_description


def load_category_references():
    """
    Group valid labelled examples by division and category.

    Returns:
        {(division, category): [description, ...]}
    """
    references = defaultdict(list)

    with DATASET_PATH.open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            division = (row["division"] or "").strip()
            category = (row["expected_category"] or "").strip()

            if not category:
                continue

            cleaned, error = validate_ai_description(
                row["description"]
            )

            if error:
                continue

            references[(division, category)].append(cleaned)

    return dict(references)
