
import csv
from pathlib import Path

from tickets.models import Category


DATASET_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "ai_complaint_examples.csv"
)

REQUIRED_COLUMNS = {
    "example_id",
    "division",
    "expected_category",
    "description",
}


def validate_complaint_dataset():
    errors = []
    total = 0
    seen_ids = set()

    valid_categories = set(
        Category.objects.values_list("division", "name")
    )

    with DATASET_PATH.open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            return 0, ["CSV file is empty."]

        if set(reader.fieldnames) != REQUIRED_COLUMNS:
            return 0, ["CSV columns do not match the expected format."]

        for line_number, row in enumerate(reader, start=2):
            total += 1

            example_id = (row["example_id"] or "").strip()
            division = (row["division"] or "").strip()
            category = (row["expected_category"] or "").strip()
            description = (row["description"] or "").strip()

            if not example_id:
                errors.append(f"Line {line_number}: Missing example ID.")
            elif example_id in seen_ids:
                errors.append(f"Line {line_number}: Duplicate example ID.")
            else:
                seen_ids.add(example_id)

            if division not in {"employee", "customer"}:
                errors.append(f"Line {line_number}: Invalid division.")

            if category and (division, category) not in valid_categories:
                errors.append(
                    f"Line {line_number}: Invalid category '{category}' "
                    f"for division '{division}'."
                )
            
            if not description and category:
                errors.append(
                    f"Line {line_number}: Labelled complaint has an empty description."
    )

    return total, errors
