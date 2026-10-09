"""Write the text message that reminds a patient of an appointment."""

import re

MAX_CHARS = 160
MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")

PROMPT = """Write a text message reminding a patient of an appointment.
Friendly and plain, one paragraph, at most {max_chars} characters.
Use the patient's first name and write the date and the time exactly as given.

Patient first name: {first_name}
Clinic: {clinic}
Date: {date}
Time: {time}
Preparation: {prep}
Clinic phone: {phone}
"""

TEMPLATE = ("Hi {first_name}, a reminder of your appointment at {clinic} "
            "on {date} at {time}. Questions? Call {phone}.")

LABEL = re.compile(r"^(?:sms|message|text|reminder)\s*:\s*", re.IGNORECASE)
QUOTES = "\"'“”"


def draft_reminder(appointment, model, max_chars=MAX_CHARS):
    """Return the reminder for an appointment as {"text", "source", "problem"}.

    `appointment` is a dict with "first_name", "clinic", "when" (a datetime),
    "phone" and optionally "prep".
    `model` is a callable taking a prompt string and returning a string.
    """
    when = appointment["when"]
    facts = {
        "first_name": appointment["first_name"],
        "clinic": appointment["clinic"],
        "date": f"{when.day} {MONTHS[when.month - 1]}",
        "time": f"{when:%H:%M}",
        "phone": appointment["phone"],
    }
    answer = model(PROMPT.format(
        max_chars=max_chars, prep=appointment.get("prep") or "none", **facts
    ))

    text = _clean(answer)
    problem = _problem(text, facts, max_chars)
    if problem:
        # A wrong reminder is worse than a dull one: send the fixed wording.
        return {"text": TEMPLATE.format(**facts), "source": "template", "problem": problem}
    return {"text": text, "source": "model", "problem": None}


def _clean(answer):
    text = " ".join(answer.split())
    text = LABEL.sub("", text)
    if len(text) > 1 and text[0] in QUOTES and text[-1] in QUOTES:
        text = text[1:-1].strip()
    return text


def _problem(text, facts, max_chars):
    if not text:
        return "empty"
    if len(text) > max_chars:
        return "too long"
    if facts["first_name"] not in text:
        return "name missing"
    # "4 Oct" must not be satisfied by "14 Oct", nor "9:30" by "19:30".
    if not re.search(r"(?<!\d)" + re.escape(facts["date"]), text):
        return "date missing"
    if not re.search(r"(?<!\d)" + re.escape(facts["time"]) + r"(?!\d)", text):
        return "time missing"
    return None
