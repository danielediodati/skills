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
