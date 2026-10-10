# Calibration: action_items-03-3

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
# A task taken by two people shows up as nobody's

Some of our action items are shared: two people agree to do something together. Those come back with no owner at all, which is worse than useless, because in the follow-up email they look like the tasks nobody picked up, and someone then chases the team to find a volunteer.

Example. Attendees: Ana Ruiz, Tom Becker, Priya Raman. Notes:

> Ana and Tom will draft the supplier shortlist by 12 March. Priya books the demo room.

What we got:

| Task | Owner | Due |
| --- | --- | --- |
| Draft the supplier shortlist | (nobody) | 12 March |
| Book the demo room | Priya Raman | |

What I want is to see both Ana Ruiz and Tom Becker on the shortlist task, each with their name as it is in the attendee list, like for any other task. It is one task, so it should stay one line, not become two.

If one of the two names is not somebody who was in the meeting (say "Ana and Marta from legal"), keep the one we know, Ana Ruiz, rather than dropping both.
````

## 4. The diff

````diff
--- a/README.md
+++ b/README.md
@@ -9,7 +9,7 @@
 The model reads the notes and writes the items. The code decides what is kept:
 
 - lines of the answer that are not `task | owner | due` are skipped;
-- an owner is kept only if it is the name of one of the attendees, and is returned spelled as the caller gave it; otherwise the item stays, with `owner` set to `None`;
+- an owner is kept only if it is the name of one of the attendees, and is returned spelled as the caller gave it; otherwise the item stays, with `owner` set to `None`. A task shared by several people stays one item: `owner` is the first of them, `co_owners` the rest, and `owners` all of them. Names that were not in the meeting are left out, so the attendees who are named are kept;
 - a deadline is kept only if it is a real date on or after the day of the meeting; otherwise `due` is `None`;
 - a task repeated for the same owner is listed once, and a task longer than 120 characters is shortened.
 
--- a/seam.py
+++ b/seam.py
@@ -3,7 +3,7 @@
 import re
 from dataclasses import dataclass
 from datetime import date
-from typing import Callable, List, Optional, Sequence
+from typing import Callable, List, Optional, Sequence, Tuple
 
 MAX_ITEMS = 10
 MAX_TASK_CHARS = 120
@@ -21,7 +21,8 @@
 
 - task: a short imperative sentence, e.g. "Send the revised quote to Halden".
 - owner: the name of the person responsible, as written in the list above,
-  or "none" if nobody took it.
+  or "none" if nobody took it. If several people share the task, write all
+  their names separated by ";", e.g. "Ana Ruiz; Tom Becker".
 - due: the deadline as YYYY-MM-DD, or "none" if no deadline was given.
 
 If there are no action items, write only: NONE
@@ -32,6 +33,7 @@
 
 _EMPTY = {"", "none", "n/a", "-", "?", "tbd", "unassigned"}
 _BULLET = re.compile(r"^\s*(?:[-*•]|\d+[.)])\s*")
+_OWNER_SEP = re.compile(r"\s*[;,&/]\s*|\s+and\s+", re.IGNORECASE)
 
 
 @dataclass(frozen=True)
@@ -39,6 +41,12 @@
     task: str
     owner: Optional[str]  # one of the attendees, spelled as the caller gave it
     due: Optional[date]
+    co_owners: Tuple[str, ...] = ()  # the other attendees sharing the task
+
+    @property
+    def owners(self) -> Tuple[str, ...]:
+        """Everyone who took the task, in the order the model gave them."""
+        return ((self.owner,) if self.owner is not None else ()) + self.co_owners
 
 
 def extract_action_items(
@@ -50,9 +58,9 @@
     """Return the action items found in `notes`, soonest deadline first.
 
     `model` takes a prompt and returns text. Its answer is not trusted: lines
-    that are not in the requested form are skipped, an owner who was not in
-    the meeting becomes None, and so does a deadline that is not a real date
-    or falls before the meeting.
+    that are not in the requested form are skipped, owners who were not in
+    the meeting are left out (an item with none left is unowned), and a
+    deadline that is not a real date or falls before the meeting becomes None.
     """
     if not notes.strip():
         return []
@@ -76,12 +84,13 @@
         task = _clean_task(fields[0])
         if not task or _key(task) == "task":  # empty, or the header echoed back
             continue
-        owner = by_name.get(_key(fields[1]))
+        owners = _parse_owners(fields[1], by_name)
         due = _parse_due(fields[2], meeting_date)
-        if (_key(task), owner) in seen:
+        if (_key(task), owners) in seen:
             continue
-        seen.add((_key(task), owner))
-        items.append(ActionItem(task, owner, due))
+        seen.add((_key(task), owners))
+        first = owners[0] if owners else None
+        items.append(ActionItem(task, first, due, owners[1:]))
 
     # Dated items first, soonest first; undated ones keep the model's order.
     items.sort(key=lambda item: (item.due is None, item.due or date.max))
@@ -90,6 +99,18 @@
 
 def _key(text: str) -> str:
     return " ".join(text.split()).casefold()
+
+
+def _parse_owners(text: str, by_name: dict) -> Tuple[str, ...]:
+    """Attendees named in `text`; people who were not in the meeting are left out."""
+    if _key(text) in by_name:  # the whole field is one name, e.g. "Ruiz, Ana"
+        return (by_name[_key(text)],)
+    owners: List[str] = []
+    for part in _OWNER_SEP.split(text):
+        name = by_name.get(_key(part))
+        if name is not None and name not in owners:
+            owners.append(name)
+    return tuple(owners)
 
 
 def _clean_task(text: str) -> str:
--- a/test.py
+++ b/test.py
@@ -93,6 +93,21 @@
         items = run("Approve the budget | Marta Olsen | none")
         self.assertEqual(items, [ActionItem("Approve the budget", None, None)])
 
+    def test_shared_task_stays_one_item_with_every_owner(self):
+        for field in ("Ana Ruiz; Tom Becker", "ana ruiz and Tom Becker", "Ana Ruiz, Tom Becker"):
+            items = run(f"Draft the supplier shortlist | {field} | 2026-03-12")
+            self.assertEqual(len(items), 1)
+            self.assertEqual(items[0].owners, ("Ana Ruiz", "Tom Becker"))
+            self.assertEqual(items[0].owner, "Ana Ruiz")
+
+    def test_shared_task_keeps_the_known_owner_when_the_other_was_not_there(self):
+        items = run("Check the contract | Ana Ruiz; Marta from legal | none")
+        self.assertEqual(items, [ActionItem("Check the contract", "Ana Ruiz", None)])
+
+    def test_repeated_name_is_listed_once(self):
+        items = run("Check the contract | Ana Ruiz; ana ruiz | none")
+        self.assertEqual(items[0].owners, ("Ana Ruiz",))
+
     def test_explicit_none_owner(self):
         self.assertIsNone(run("Find a caterer | none | none")[0].owner)
 

````

## 5. The agent's final answer

````
A shared task now stays one item and carries every owner who was in the meeting. All 20 tests pass, including three new ones for this case.

**What changed in `seam.py`**
- **Prompt:** the model is told to write shared owners separated by `;`, e.g. `Ana Ruiz; Tom Becker`.
- **Parsing:** the owner field is also split on `,`, `&`, `/` and `and`, since models don't always follow the format. Each part is matched against the attendee list, so names come back spelled as the caller gave them, and a name repeated within the field is listed once.
- **Unknown names:** `Ana Ruiz; Marta from legal` keeps Ana Ruiz and drops Marta. If nobody known is left, the item is unowned, as before.
- **`ActionItem`:** it keeps `owner` (the first owner) and gains `co_owners` (the rest) and an `owners` property returning all of them. Existing callers and the existing `ActionItem(task, owner, due)` constructor keep working.
- **Dedupe:** de-duplication now compares the task plus the full set of owners, so "Ana + Tom" and "Ana alone" on the same task are distinct, as they were before for single owners.

**Other changes**
- `README.md` and `test.py` are updated.
- One limitation: if the model writes the free-text phrase "Ana and Marta from legal" as the owner field, Ana is not recognised. The prompt asks for attendee names, so this should be rare.

Consumers that show or export the owner column need to switch to `owners` to display both names. Anything still reading only `owner` will show just the first person.
````
