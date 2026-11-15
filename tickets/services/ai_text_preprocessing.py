
import re
import unicodedata

MAX_TEXT_LENGTH = 5000


def preprocess_complaint_text(text):
    if not isinstance(text, str):
        return ""

    text = unicodedata.normalize("NFKC", text)

    text = "".join(
        char for char in text
        if unicodedata.category(char) != "Cc"
        or char in "\n\t\r"
    )

    text = re.sub(r"\s+", " ", text).strip()

    return text[:MAX_TEXT_LENGTH]


def validate_ai_description(text):
    cleaned = preprocess_complaint_text(text)

    if not cleaned:
        return "", "Description cannot be empty."

    if len(cleaned) < 10:
        return "", "Description is too short for AI analysis."

    if not any(char.isalpha() for char in cleaned):
        return "", "Description must contain meaningful text."

    if len(cleaned.split()) < 3:
        return "", "Please provide a more detailed description."

    return cleaned, None
