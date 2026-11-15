
import re

HIGH_URGENCY_KEYWORDS = (
    "security breach",
    "data loss",
    "data leak",
    "system down",
    "server down",
    "complete outage",
    "cannot access",
    "unable to access",
    "fire",
    "electric shock",
    "server is down",
    "system is down",
    "website is down",
    "application is down",
)
MEDIUM_URGENCY_KEYWORDS = (
    "not working",
    "not responding",
    "crashing",
    "crashes",
    "failed",
    "failure",
    "slow",
    "intermittent",
    "disconnected",
)


def detect_complaint_urgency(description):
    """
    Suggest urgency using predefined keyword rules.

    Returns a dictionary containing urgency and reason.
    This does not modify a Ticket or its status.
    """
    if not isinstance(description, str) or not description.strip():
        return {
            "urgency": "low",
            "reason": "No complaint description provided.",
        }

    text = description.lower()

    for keyword in HIGH_URGENCY_KEYWORDS:
        if re.search(r"\b" + re.escape(keyword) + r"\b", text):
            return {
                "urgency": "high",
                "reason": f"High-urgency phrase detected: {keyword}.",
            }

    for keyword in MEDIUM_URGENCY_KEYWORDS:
        if re.search(r"\b" + re.escape(keyword) + r"\b", text):
            return {
                "urgency": "medium",
                "reason": f"Medium-urgency phrase detected: {keyword}.",
            }

    return {
        "urgency": "low",
        "reason": "No urgent indicators detected.",
    }
