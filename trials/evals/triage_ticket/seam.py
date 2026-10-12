"""Route an incoming support ticket: queue, urgency, one-line summary."""

import re

QUEUES = ("billing", "technical", "account", "shipping", "general")
URGENCIES = ("low", "normal", "high", "urgent")
RESPOND_WITHIN_HOURS = {"low": 72, "normal": 24, "high": 8, "urgent": 1}
MAX_BODY_CHARS = 8000
MAX_SUMMARY_CHARS = 120

PROMPT = """You triage customer support tickets.

Answer with exactly three lines:
queue: one of {queues}
urgency: one of {urgencies}
summary: one sentence saying what the customer needs

Subject: {subject}

{body}
"""

FIELD = re.compile(r"^\W*(queue|urgency|summary)\W*:\s*(.+)$", re.IGNORECASE)


def triage_ticket(ticket, model):
    """Return the queue, urgency, summary and response deadline for a ticket.

    `ticket` is a dict with "subject", "body" and optionally "tier".
    `model` is a callable taking a prompt string and returning a string.
    """
    subject = ticket.get("subject", "").strip()
    body = ticket.get("body", "").strip()
    if not subject and not body:
        raise ValueError("ticket has no subject and no body")

    answer = model(PROMPT.format(
        queues=", ".join(QUEUES),
        urgencies=", ".join(URGENCIES),
        subject=subject,
        body=body[:MAX_BODY_CHARS],
    ))
    fields = _parse_fields(answer)

    queue = _choice(fields.get("queue"), QUEUES, "general")
    urgency = _choice(fields.get("urgency"), URGENCIES, "normal")
    if ticket.get("tier") == "enterprise":
        # Enterprise contracts promise a faster answer: one level up.
        level = min(URGENCIES.index(urgency) + 1, len(URGENCIES) - 1)
        urgency = URGENCIES[level]

    summary = " ".join(fields.get("summary", "").split()) or subject
    return {
        "queue": queue,
        "urgency": urgency,
        "summary": summary[:MAX_SUMMARY_CHARS],
        "respond_within_hours": RESPOND_WITHIN_HOURS[urgency],
    }


def _parse_fields(answer):
    fields = {}
    for line in answer.splitlines():
        match = FIELD.match(line)
        if match:
            # The first occurrence of a field wins.
            fields.setdefault(match.group(1).lower(), match.group(2).strip())
    return fields


def _choice(value, allowed, default):
    value = (value or "").strip(" .*`\"'").lower()
    return value if value in allowed else default
