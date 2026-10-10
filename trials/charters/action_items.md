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
