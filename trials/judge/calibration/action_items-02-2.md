# Calibration: action_items-02-2

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
# Deadlines given as a day of the week get lost

In our meetings people say "by Friday" or "by next Wednesday". They almost never say a date. Those deadlines mostly do not make it into the action list: the task is there, the owner is there, the due date is empty. Since the list is ordered by deadline, these tasks also sink to the bottom, below things due weeks later.

Example. Meeting on Tuesday 3 March 2026, notes:

> Ana will send the revised quote to Halden by Friday. Tom to confirm the venue by next Wednesday. Priya orders the badges by 20 March.

What we got:

| Task | Owner | Due |
| --- | --- | --- |
| Order the badges | Priya Raman | 20 March |
| Send the revised quote to Halden | Ana Ruiz | |
| Confirm the venue | Tom Becker | |

What I expected:

| Task | Owner | Due |
| --- | --- | --- |
| Send the revised quote to Halden | Ana Ruiz | 6 March |
| Confirm the venue | Tom Becker | 11 March |
| Order the badges | Priya Raman | 20 March |

A day of the week should count as a deadline: the first such day after the meeting, and the one in the following week when the notes say "next". If the meeting is on a Friday and someone says "by Friday", they mean a week later, not the same day.
````

## 4. The diff

````diff
--- a/seam.py
+++ b/seam.py
@@ -2,14 +2,14 @@
 
 import re
 from dataclasses import dataclass
-from datetime import date
+from datetime import date, timedelta
 from typing import Callable, List, Optional, Sequence
 
 MAX_ITEMS = 10
 MAX_TASK_CHARS = 120
 
 PROMPT = """\
-Below are the notes of a meeting held on {meeting_date}.
+Below are the notes of a meeting held on {meeting_date} ({meeting_weekday}).
 The people present were: {attendees}.
 
 List every action item agreed in the meeting: something a person committed
@@ -23,6 +23,10 @@
 - owner: the name of the person responsible, as written in the list above,
   or "none" if nobody took it.
 - due: the deadline as YYYY-MM-DD, or "none" if no deadline was given.
+  A day of the week is a deadline: "by Friday" is the first Friday after the
+  meeting (a week later if the meeting itself is on a Friday), and "by next
+  Wednesday" is the Wednesday of the following week. The next two weeks are:
+{calendar}
 
 If there are no action items, write only: NONE
 
@@ -31,6 +35,12 @@
 """
 
 _EMPTY = {"", "none", "n/a", "-", "?", "tbd", "unassigned"}
+_WEEKDAYS = [
+    "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"
+]
+_WEEKDAY_DUE = re.compile(
+    r"^(?:(?:by|on|before|until)\s+)?(?:(this|next)\s+)?(" + "|".join(_WEEKDAYS) + r")$"
+)
 _BULLET = re.compile(r"^\s*(?:[-*•]|\d+[.)])\s*")
 
 
@@ -59,6 +69,11 @@
 
     prompt = PROMPT.format(
         meeting_date=meeting_date.isoformat(),
+        meeting_weekday=_WEEKDAYS[meeting_date.weekday()].capitalize(),
+        calendar="\n".join(
+            f"  {_WEEKDAYS[d.weekday()].capitalize()} {d.isoformat()}"
+            for d in (meeting_date + timedelta(days=n) for n in range(1, 15))
+        ),
         attendees=", ".join(attendees),
         notes=notes.strip(),
     )
@@ -108,5 +123,21 @@
     try:
         due = date.fromisoformat(text)
     except ValueError:
+        due = _weekday_due(text, meeting_date)
+        if due is None:
+            return None
+    return due if due >= meeting_date else None
+
+
+def _weekday_due(text: str, meeting_date: date) -> Optional[date]:
+    """Resolve "Friday" or "next Wednesday" relative to the meeting."""
+    match = _WEEKDAY_DUE.match(_key(text))
+    if not match:
         return None
-    return due if due >= meeting_date else None
+    qualifier, name = match.groups()
+    weekday = _WEEKDAYS.index(name)
+    if qualifier == "next":
+        monday = meeting_date - timedelta(days=meeting_date.weekday())
+        return monday + timedelta(days=7 + weekday)
+    # First such day strictly after the meeting.
+    return meeting_date + timedelta(days=(weekday - meeting_date.weekday() - 1) % 7 + 1)
--- a/test.py
+++ b/test.py
@@ -112,6 +112,28 @@
         self.assertEqual(run("Book the room | Tom Becker | 2026-03-03")[0].due, MEETING)
 
 
+class WeekdayDueTest(unittest.TestCase):
+    def due(self, text, meeting=MEETING):
+        answer = f"Do it | Ana Ruiz | {text}"
+        return extract_action_items(NOTES, ATTENDEES, meeting, FakeModel(answer))[0].due
+
+    def test_weekday_is_the_first_such_day_after_the_meeting(self):
+        self.assertEqual(self.due("Friday"), date(2026, 3, 6))
+        self.assertEqual(self.due("by Friday"), date(2026, 3, 6))
+
+    def test_next_weekday_is_in_the_following_week(self):
+        self.assertEqual(self.due("next Wednesday"), date(2026, 3, 11))
+
+    def test_same_weekday_as_the_meeting_means_a_week_later(self):
+        self.assertEqual(self.due("Friday", date(2026, 3, 6)), date(2026, 3, 13))
+
+    def test_prompt_lists_the_calendar(self):
+        model = FakeModel("NONE")
+        extract_action_items(NOTES, ATTENDEES, MEETING, model)
+        self.assertIn("Friday 2026-03-06", model.prompts[0])
+        self.assertIn("Wednesday 2026-03-11", model.prompts[0])
+
+
 class ListTest(unittest.TestCase):
     def test_sorted_by_deadline_with_undated_items_last_in_original_order(self):
         items = run(

````

## 5. The agent's final answer

````
Day-of-week deadlines now get a due date, and the list sorts them in with the dated items. All 21 tests pass, including four new ones.

Changes in `seam.py`:

- **Prompt:** it now gives the meeting's weekday and the rule for "by Friday" and "by next Wednesday". It also lists the next 14 days with weekday and ISO date, so the model doesn't have to do the calendar arithmetic itself.
- **Parser:** if the model returns a weekday phrase instead of a date (`Friday`, `by Friday`, `next Wednesday`, `on Monday`), the code resolves it. This covers a model that ignores the prompt.

The resolution rules:

- **Plain weekday:** the first such day strictly after the meeting, so a Friday meeting with "by Friday" gives the Friday a week later.
- **"next" weekday:** that weekday in the following Monday–Sunday week. For your Tuesday 3 March example, Friday is 6 March and next Wednesday is 11 March.

The new tests are in `test.py` and cover those rules, the Friday-on-Friday case, and the calendar in the prompt.

One ambiguity to be aware of: "next Friday" said on a Tuesday resolves to 13 March, not 6 March. That follows your "the one in the following week" rule, but people sometimes mean the nearer one.
````
