"""Turn free-form meeting notes into a checked list of action items."""

import re
from dataclasses import dataclass
from datetime import date
from typing import Callable, List, Optional, Sequence

MAX_ITEMS = 10
MAX_TASK_CHARS = 120

PROMPT = """\
Below are the notes of a meeting held on {meeting_date}.
The people present were: {attendees}.

List every action item agreed in the meeting: something a person committed
to do after it. Leave out decisions, opinions and things already done.

Write one action item per line, in exactly this form:

task | owner | due

- task: a short imperative sentence, e.g. "Send the revised quote to Halden".
- owner: the name of the person responsible, as written in the list above,
  or "none" if nobody took it.
- due: the deadline as YYYY-MM-DD, or "none" if no deadline was given.

If there are no action items, write only: NONE

Notes:
{notes}
"""

_EMPTY = {"", "none", "n/a", "-", "?", "tbd", "unassigned"}
_BULLET = re.compile(r"^\s*(?:[-*•]|\d+[.)])\s*")


@dataclass(frozen=True)
class ActionItem:
    task: str
    owner: Optional[str]  # one of the attendees, spelled as the caller gave it
    due: Optional[date]


def extract_action_items(
    notes: str,
    attendees: Sequence[str],
    meeting_date: date,
    model: Callable[[str], str],
) -> List[ActionItem]:
    """Return the action items found in `notes`, soonest deadline first.

    `model` takes a prompt and returns text. Its answer is not trusted: lines
    that are not in the requested form are skipped, an owner who was not in
    the meeting becomes None, and so does a deadline that is not a real date
    or falls before the meeting.
    """
    if not notes.strip():
        return []

    prompt = PROMPT.format(
        meeting_date=meeting_date.isoformat(),
        attendees=", ".join(attendees),
        notes=notes.strip(),
    )
    answer = model(prompt)

    by_name = {_key(name): name for name in attendees}
    items: List[ActionItem] = []
    seen = set()
    for line in answer.splitlines():
        line = _BULLET.sub("", line).strip()
        # Split from the right, so a task may itself contain a "|".
        fields = [field.strip() for field in line.rsplit("|", 2)]
        if len(fields) != 3:
            continue
        task = _clean_task(fields[0])
        if not task or _key(task) == "task":  # empty, or the header echoed back
            continue
        owner = by_name.get(_key(fields[1]))
        due = _parse_due(fields[2], meeting_date)
        if (_key(task), owner) in seen:
            continue
        seen.add((_key(task), owner))
        items.append(ActionItem(task, owner, due))

    # Dated items first, soonest first; undated ones keep the model's order.
    items.sort(key=lambda item: (item.due is None, item.due or date.max))
    return items[:MAX_ITEMS]


def _key(text: str) -> str:
    return " ".join(text.split()).casefold()


def _clean_task(text: str) -> str:
    task = " ".join(text.split()).strip("\"'").rstrip(".").strip()
    if len(task) <= MAX_TASK_CHARS:
        return task
    cut = task[: MAX_TASK_CHARS - 1]
    if " " in cut:
        cut = cut[: cut.rindex(" ")]
    return cut.rstrip(" ,;:") + "…"


def _parse_due(text: str, meeting_date: date) -> Optional[date]:
    if _key(text) in _EMPTY:
        return None
    try:
        due = date.fromisoformat(text)
    except ValueError:
        return None
    return due if due >= meeting_date else None
