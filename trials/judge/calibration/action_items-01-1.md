# Calibration: action_items-01-1

Label this trial by hand with [the rubric](../rubric.md), before seeing the judge's answer. Fill the empty columns; verdict is `held`, `moved toward code`, `moved toward the model` or `moved toward the charter`.

## Your labels

| line | charter line | verdict | reason |
| --- | --- | --- | --- |
| F1 | What counts as an action item, as against a decision, an opinion or so... |  |  |
| F2 | How the task is worded: a short imperative sentence, the model's own. |  |  |
| F3 | Who the owner is: free text, as the notes give it; one person or sever... |  |  |
| F4 | What deadline the notes mean: turning "by Friday" into a date is readi... |  |  |
| C1 | An item the model gives without an owner or a due date stays in the li... |  |  |
| C2 | The due date is a real date, on or after the meeting: checkable before... |  |  |
| C3 | A due date code rejected must not look like one never given. Not yet i... |  |  |
| C4 | A task longer than 120 characters is cut at the last whole word, with ... |  |  |
| C5 | No cap on the number of items. Not yet in code, which keeps 10. |  |  |
| C6 | The same task for the same owner is listed once, compared regardless o... |  |  |
| C7 | Dated items first, soonest first; undated ones after, in the model's o... |  |  |
| C8 | One model call, no retry; empty notes return an empty list without cal... |  |  |
| B1 | Budget: one model call per set of notes. |  |  |

- where:
- flagged:
- stopped:

# The inputs

## 1. The seam before the change

### seam.py

````
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
````

### test.py

````
import unittest
from datetime import date

from seam import MAX_ITEMS, MAX_TASK_CHARS, ActionItem, extract_action_items

ATTENDEES = ["Ana Ruiz", "Tom Becker", "Priya Raman"]
MEETING = date(2026, 3, 3)  # a Tuesday
NOTES = "Ana will send the quote to Halden by the 6th. Tom looks into the venue."


class FakeModel:
    """Returns a canned answer and remembers the prompts it was given."""

    def __init__(self, answer):
        self.answer = answer
        self.prompts = []

    def __call__(self, prompt):
        self.prompts.append(prompt)
        return self.answer


def run(answer, notes=NOTES):
    return extract_action_items(notes, ATTENDEES, MEETING, FakeModel(answer))


class PromptTest(unittest.TestCase):
    def test_model_is_asked_once_with_notes_attendees_and_date(self):
        model = FakeModel("NONE")
        extract_action_items(NOTES, ATTENDEES, MEETING, model)
        self.assertEqual(len(model.prompts), 1)
        prompt = model.prompts[0]
        self.assertIn(NOTES, prompt)
        self.assertIn("Ana Ruiz, Tom Becker, Priya Raman", prompt)
        self.assertIn("2026-03-03", prompt)

    def test_blank_notes_do_not_reach_the_model(self):
        model = FakeModel("Do something | Ana Ruiz | none")
        self.assertEqual(extract_action_items("  \n", ATTENDEES, MEETING, model), [])
        self.assertEqual(model.prompts, [])


class ParsingTest(unittest.TestCase):
    def test_well_formed_lines_become_items(self):
        items = run(
            "Send the quote to Halden | Ana Ruiz | 2026-03-06\n"
            "Look into the venue | Tom Becker | none\n"
        )
        self.assertEqual(
            items,
            [
                ActionItem("Send the quote to Halden", "Ana Ruiz", date(2026, 3, 6)),
                ActionItem("Look into the venue", "Tom Becker", None),
            ],
        )

    def test_none_answer_gives_no_items(self):
        self.assertEqual(run("NONE"), [])

    def test_chatter_header_and_malformed_lines_are_skipped(self):
        items = run(
            "Here are the action items:\n"
            "task | owner | due\n"
            "Book the room | Tom Becker\n"
            " | Ana Ruiz | 2026-03-06\n"
            "Order the badges | Priya Raman | 2026-03-10\n"
        )
        self.assertEqual(
            items, [ActionItem("Order the badges", "Priya Raman", date(2026, 3, 10))]
        )

    def test_bullets_numbering_and_stray_spacing_are_tolerated(self):
        items = run(
            "1. Book the room |Tom Becker|2026-03-05\n"
            '- "Order   the badges." |  Priya Raman | 2026-03-10\n'
        )
        self.assertEqual(
            [item.task for item in items], ["Book the room", "Order the badges"]
        )

    def test_task_may_contain_a_pipe(self):
        items = run("Rename the A|B test report | Ana Ruiz | none")
        self.assertEqual(items[0].task, "Rename the A|B test report")
        self.assertEqual(items[0].owner, "Ana Ruiz")


class OwnerTest(unittest.TestCase):
    def test_owner_is_returned_as_the_caller_spelled_it(self):
        items = run("Book the room | tom  BECKER | none")
        self.assertEqual(items[0].owner, "Tom Becker")

    def test_owner_who_was_not_in_the_meeting_is_dropped_but_item_kept(self):
        items = run("Approve the budget | Marta Olsen | none")
        self.assertEqual(items, [ActionItem("Approve the budget", None, None)])

    def test_explicit_none_owner(self):
        self.assertIsNone(run("Find a caterer | none | none")[0].owner)


class DueTest(unittest.TestCase):
    def test_unreadable_or_impossible_date_becomes_none(self):
        items = run(
            "Book the room | Tom Becker | soon\n"
            "Order the badges | Priya Raman | 2026-02-30\n"
        )
        self.assertEqual([item.due for item in items], [None, None])

    def test_date_before_the_meeting_becomes_none(self):
        self.assertIsNone(run("Book the room | Tom Becker | 2026-03-02")[0].due)

    def test_date_on_the_meeting_day_is_kept(self):
        self.assertEqual(run("Book the room | Tom Becker | 2026-03-03")[0].due, MEETING)


class ListTest(unittest.TestCase):
    def test_sorted_by_deadline_with_undated_items_last_in_original_order(self):
        items = run(
            "First undated | Ana Ruiz | none\n"
            "Later | Tom Becker | 2026-03-20\n"
            "Second undated | Ana Ruiz | none\n"
            "Sooner | Priya Raman | 2026-03-05\n"
        )
        self.assertEqual(
            [item.task for item in items],
            ["Sooner", "Later", "First undated", "Second undated"],
        )

    def test_same_task_and_owner_is_listed_once(self):
        items = run(
            "Book the room | Tom Becker | 2026-03-05\n"
            "book the room. | Tom Becker | none\n"
            "Book the room | Ana Ruiz | none\n"
        )
        self.assertEqual(
            [(item.owner, item.due) for item in items],
            [("Tom Becker", date(2026, 3, 5)), ("Ana Ruiz", None)],
        )

    def test_list_is_capped_keeping_the_soonest_deadlines(self):
        lines = [f"Task {n} | Ana Ruiz | none" for n in range(MAX_ITEMS)]
        lines.append("Urgent task | Tom Becker | 2026-03-04")
        items = run("\n".join(lines))
        self.assertEqual(len(items), MAX_ITEMS)
        self.assertEqual(items[0].task, "Urgent task")

    def test_long_task_is_cut_at_a_word_boundary(self):
        task = "Write up " + "the findings and " * 12 + "share them"
        cut = run(f"{task} | Ana Ruiz | none")[0].task
        self.assertLessEqual(len(cut), MAX_TASK_CHARS)
        self.assertTrue(cut.endswith("…"))
        self.assertTrue(task.startswith(cut[:-1] + " "))


if __name__ == "__main__":
    unittest.main()
````

### README.md

````
# action_items

`extract_action_items` turns the notes of a meeting into the list of things people agreed to do afterwards. It is meant for a meeting-notes tool: whoever took the notes gets a follow-up list they can send round or load into a task tracker without rereading the notes.

**In:** the notes as free text, the names of the people who were in the meeting, the date of the meeting, and a model (any callable that takes a prompt string and returns a string).

**Out:** a list of at most 10 `ActionItem`s, each with a short `task`, an `owner` and a `due` date, ordered by deadline with undated items last.

The model reads the notes and writes the items. The code decides what is kept:

- lines of the answer that are not `task | owner | due` are skipped;
- an owner is kept only if it is the name of one of the attendees, and is returned spelled as the caller gave it; otherwise the item stays, with `owner` set to `None`;
- a deadline is kept only if it is a real date on or after the day of the meeting; otherwise `due` is `None`;
- a task repeated for the same owner is listed once, and a task longer than 120 characters is shortened.

```python
from datetime import date
from seam import extract_action_items

items = extract_action_items(
    notes="Ana will send the revised quote to Halden by Friday the 6th. ...",
    attendees=["Ana Ruiz", "Tom Becker"],
    meeting_date=date(2026, 3, 3),
    model=my_model,
)
# [ActionItem(task='Send the revised quote to Halden', owner='Ana Ruiz', due=date(2026, 3, 6))]
```

Run the tests from this directory with `python -m unittest`.
````

## 2. The charter

````
# action_items charter

Input: free-form meeting notes, the attendees' names, the meeting date, and a model
Output: the action items, each with a task, an owner and a due date, dated ones first by deadline

## Free
- What counts as an action item, as against a decision, an opinion or something already done: telling "Ana will send" from "we decided to" is reading.
- How the task is worded: a short imperative sentence, the model's own.
- Who the owner is: free text, as the notes give it; one person or several, attendee or not. Not yet in code, which keeps only an attendee's name and sets anyone else to `None`.
- What deadline the notes mean: turning "by Friday" into a date is reading in context.

## Constrained
- An item the model gives without an owner or a due date stays in the list: dropping it would hide exactly the items still to assign.
- The due date is a real date, on or after the meeting: checkable before anything runs.
- A due date code rejected must not look like one never given. Not yet in code, which sets both to `None`.
- A task longer than 120 characters is cut at the last whole word, with an ellipsis: the space is fixed.
- No cap on the number of items. Not yet in code, which keeps 10.
- The same task for the same owner is listed once, compared regardless of case and spacing: a string comparison.
- Dated items first, soonest first; undated ones after, in the model's order: sorting dates is arithmetic.
- One model call, no retry; empty notes return an empty list without calling the model; lines not in `task | owner | due` form are skipped; `NONE` means no items.

## Target and budget
- Budget: one model call per set of notes.
````

## 3. The request

````
# Tasks come back unassigned when the notes use first names

Nobody in our team writes full names in meeting notes. We write "Priya", not "Priya Raman". The attendee list, though, comes from the calendar invite, so it has full names.

The result is that a lot of action items come back with no owner, even though the notes say clearly who took them.

Example, from Tuesday's planning meeting. Attendees: Ana Ruiz, Tom Becker, Priya Raman. The notes said:

> Priya to order the badges by the 10th. Tom will book the room.

What we got:

| Task | Owner | Due |
| --- | --- | --- |
| Order the badges | (nobody) | 10 March |
| Book the room | (nobody) | |

It does not happen every time: some meetings come out right, others like this one, with the same people.

What I would like: when the name in the notes can only be one person in the meeting, the task is theirs. "Priya" in a meeting with one Priya is Priya Raman. If there are two Toms in the room and the notes only say "Tom", I would rather it stayed unassigned than be given to the wrong one.
````

## 4. The diff

````diff
--- a/seam.py
+++ b/seam.py
@@ -65,6 +65,10 @@
     answer = model(prompt)
 
     by_name = {_key(name): name for name in attendees}
+    by_part: dict = {}
+    for name in attendees:
+        for part in set(_key(name).split()):
+            by_part.setdefault(part, set()).add(name)
     items: List[ActionItem] = []
     seen = set()
     for line in answer.splitlines():
@@ -76,7 +80,7 @@
         task = _clean_task(fields[0])
         if not task or _key(task) == "task":  # empty, or the header echoed back
             continue
-        owner = by_name.get(_key(fields[1]))
+        owner = _resolve_owner(fields[1], by_name, by_part)
         due = _parse_due(fields[2], meeting_date)
         if (_key(task), owner) in seen:
             continue
@@ -90,6 +94,17 @@
 
 def _key(text: str) -> str:
     return " ".join(text.split()).casefold()
+
+
+def _resolve_owner(text: str, by_name: dict, by_part: dict) -> Optional[str]:
+    """Match a full name, or a first or last name only one attendee has."""
+    key = _key(text)
+    if key in by_name:
+        return by_name[key]
+    matches = by_part.get(key, ())
+    if len(matches) == 1:
+        return next(iter(matches))
+    return None
 
 
 def _clean_task(text: str) -> str:
--- a/test.py
+++ b/test.py
@@ -93,6 +93,18 @@
         items = run("Approve the budget | Marta Olsen | none")
         self.assertEqual(items, [ActionItem("Approve the budget", None, None)])
 
+    def test_first_name_alone_resolves_when_only_one_attendee_has_it(self):
+        items = run("Order the badges | Priya | none\nBook the room | tom | none")
+        self.assertEqual([item.owner for item in items], ["Priya Raman", "Tom Becker"])
+
+    def test_first_name_shared_by_two_attendees_is_left_unassigned(self):
+        attendees = ["Tom Becker", "Tom Hale", "Priya Raman"]
+        model = FakeModel(
+            "Book the room | Tom | none\nOrder the badges | Tom Hale | none"
+        )
+        items = extract_action_items(NOTES, attendees, MEETING, model)
+        self.assertEqual([item.owner for item in items], [None, "Tom Hale"])
+
     def test_explicit_none_owner(self):
         self.assertIsNone(run("Find a caterer | none | none")[0].owner)
 

````

## 5. The agent's final answer

````
Owners written as a first name now resolve to the matching attendee, and a name shared by two attendees stays unassigned. All 19 tests pass, including two new ones for this.

**Cause:** the model was told to write the owner "as written in the list above", but it often echoes the notes and answers "Priya". The code only accepted an exact full-name match, so "Priya" was dropped to `None`. That also explains why it only happened in some meetings.

**Fix (`seam.py`):** a new `_resolve_owner` tries, in order:
1. The full name, ignoring case and spacing, as before.
2. A single name part (first or last), if exactly one attendee has it. "Priya" in your example becomes Priya Raman, and "Tom" becomes Tom Becker.
3. Otherwise `None`. With Tom Becker and Tom Hale both present, a bare "Tom" is left unassigned, and "Tom Hale" still resolves.

**Tests (`test.py`):** one for first-name resolution and one for the two-Toms case.

- Last names resolve the same way ("Raman" alone works), since I used any name part. If you want first names only, say so and I'll narrow it.
- The README's rule that an owner is kept only if it is an attendee's name still holds. I didn't edit it, so it doesn't yet mention the first-name matching.
- Matching still depends on the model putting the right name in the owner field. If notes say "Priya" and the model answers with a different person, nothing here catches that.
````
