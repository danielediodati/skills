# action_items charter

Input: meeting notes as free text, the list of attendee names, the meeting date, and a `model` callable (prompt string in, text out).
Output: a list of at most 10 `ActionItem(task, owner, due)`, dated items first (soonest first), undated items last in the model's order.

## Free
- Which items count as agreed commitments: the model reads the notes and judges what someone committed to do afterwards, leaving out decisions, opinions and things already done. Notes are unstructured and this judgement cannot be written as a rule.
- Wording of `task`: the model writes a short imperative sentence. Code only normalises it (see Constrained), so the model owns the meaning and phrasing.
- Which attendee is the owner: the model reads "who said they would do it" from the notes. Code only checks that the name it gives is an attendee.
- Reading a relative deadline ("by Friday the 6th", "end of next week") as a calendar date: the model resolves it against the meeting date it is given. Code cannot parse natural language dates reliably.
- Whether the item has a deadline at all: the model decides from the notes whether a date was given; code only checks the date it writes.
- Owner "none" for an unassigned item and due "none" for an undated one: the model chooses these words, and code maps them to `None`.
- Answer shape beyond the format: the model may add chatter, headers or bullets around the lines; code tolerates them.
- Whether there are no items: the model answers `NONE` or an empty list, which code accepts.

## Constrained
- Blank or whitespace-only notes: return `[]` without calling the model, because there is nothing to read and a call would cost money for nothing.
- Prompt template: fixed text with notes, attendees and date filled in, so the model is always asked the same question in the same form. Changing it changes what the model judges, so it must be a deliberate move.
- Number of model calls: exactly one per invocation, no retry. Retrying on a bad answer would multiply cost and latency; malformed answers are dropped instead.
- Line format `task | owner | due`: only lines with exactly three fields after splitting from the right are kept; others are skipped. Splitting from the right lets a task contain "|". Reason: a line in another shape is not a usable item, and guessing it would invent items.
- Bullets and numbering (`-`, `*`, `•`, `1.`, `1)`): stripped before parsing. Harmless formatting, and tolerating it avoids losing valid items.
- Header echo: a task whose text is exactly `task` is skipped. Reason: the model sometimes repeats the header from the prompt.
- Empty task after cleaning: line skipped. Reason: an item with no task is useless.
- Owner: must match an attendee name after collapsing spaces and case-folding; returned in the caller's spelling; otherwise `None` and the item is kept. Reason: a name outside the meeting is probably a hallucination, and an item with no owner is still worth keeping. The name list is the only source of truth for owners.
- Due date: must be a valid `YYYY-MM-DD` (real calendar date, so `2026-02-30` is refused) and on or after the meeting date; otherwise `None`. Words in the empty set (`none`, `n/a`, `-`, `?`, `tbd`, `unassigned`, etc.) also give `None`. Reason: a wrong or past date would sort the item in the wrong place and be sent round as fact.
- Task cleaning: whitespace collapsed, surrounding quotes and one trailing period removed. Reason: makes duplicates comparable and output consistent for a task tracker.
- Task length: 120 characters maximum, cut at a word boundary and marked with `…`. The limit is the constraint itself (it fits a task-tracker title), not a budget; tests assert it.
- Duplicates: same task (case-folded, whitespace-normalised) and same owner, after owner mapping, is listed once, first occurrence kept. Reason: the model often repeats an item, and a list that shows it twice looks wrong. Same task with a different owner, or with an unknown owner, stays as a separate item.
- Ordering: dated items sorted ascending by due date; undated items keep the model's order (stable sort). Reason: deadlines are what the follow-up list is read for; the order among undated items carries no meaning the code can judge.
- Cap of 10 items, applied after dedupe and sort, so the soonest deadlines survive. Reason: a follow-up list must stay short enough to read; the cap is a product limit, not a cost control, and the test enforces it. Tight: changing it is a product decision.
- Attendee list in the prompt: passed as given, joined by commas. The owner check depends on it matching the list the caller passed.

## Budget
- Budget: 1 model call per invocation, no retry, no timeout in code, no token or output cap passed to the model. Prompt length grows with the notes and the code does not truncate them. Cost and latency are therefore set by the length of the notes and the model used.
