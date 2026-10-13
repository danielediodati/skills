# action_items charter

Input: meeting notes as free text, the attendee names, the meeting date, and a model (a callable that takes a prompt string and returns a string).
Output: a list of at most 10 `ActionItem(task, owner, due)`, soonest deadline first, undated items last.

## Free
- Which commitments count as action items (not decisions, opinions or things already done): only a reader of the notes can tell a commitment from a remark; the prompt asks the model to judge it.
- Wording of each task: phrasing is judgement; code only collapses whitespace, strips surrounding quotes and one trailing period.
- Which attendee owns an item: the model reads who took it on; code only checks that the name is on the attendee list.
- Whether an item has an owner at all: the model writes "none" when nobody took it; code maps that to `None` (see Constrained).
- Whether an item has a deadline, and what date it names: the model reads phrases such as "Friday the 6th" and converts them to YYYY-MM-DD; code only checks the result is a real date on or after the meeting.
- Whether there are any items: the model answers `NONE` or lists them; code needs no special case for `NONE`, it is just a line without pipes and is skipped.
- Order of undated items: the model's order is kept; code does not re-rank them.

## Constrained
- Answer form: only lines `task | owner | due` are read; any other line (chatter, header, `NONE`, malformed rows) is skipped. Why: free prose cannot be checked; a fixed row shape lets every field be validated.
- Field split: split from the right at the last two pipes, so a task may contain `|` but owner and due may not. Why: keeps tasks such as "Rename the A|B report" intact.
- Bullets and numbering (`-`, `*`, `•`, `1.`, `1)`) are stripped before parsing. Why: tolerance for the model's list style, no meaning is lost.
- Task must be non-empty and must not be the literal header `task`. Why: stops an echoed header becoming an item.
- Owner must match an attendee, ignoring case and extra spaces, and is returned as the caller spelled it; otherwise `owner` is `None` and the item is kept. Why: a tracker needs a real person, but a task nobody can be named for is still worth keeping. Tight: the attendee list is the constraint; accents or hyphen differences (e.g. "José" vs "Jose") do not match.
- Due must parse as an ISO date and be on or after the meeting date (the meeting day is kept); otherwise `due` is `None`. Why: an impossible or past deadline would mislead whoever loads the list. Tight: the on-or-after rule is the constraint itself; there is no upper limit on the date. Note: the parser is `date.fromisoformat`, which on Python 3.11+ also accepts forms such as `20260306`; the prompt asks only for YYYY-MM-DD.
- Placeholder words (`none`, `n/a`, `-`, `?`, `tbd`, `unassigned`, empty) in the due field become `None` without parsing. Why: the model uses these for "no deadline".
- Duplicates: the same task (after the cleaning above) for the same owner is listed once, first occurrence kept; the comparison ignores case and extra spaces. Why: models often repeat an item in two phrasings.
- Task cleaning: whitespace collapsed, surrounding `"` or `'` stripped, one trailing period removed. Why: normalises the display and makes duplicate detection work.
- Task length: at most 120 characters, cut at a word boundary and ended with `…`. Why: tracker field limit. Tight: a field limit, so it changes only if the tracker's field changes.
- Ordering: dated items soonest first; undated items keep the model's order (stable sort). Why: the list is read from the top, and the deadline is what matters.
- Cap: at most 10 items, applied after dedupe and sorting, so the soonest 10 survive and an undated item can be dropped when there are more than 10. Why: the README's output contract for a short follow-up list. Tight: the README states it as a contract; raising it is a product decision, not a tuning one.
- Blank notes (whitespace only) return `[]` without calling the model. Why: saves a call with nothing to read.
- Notes are stripped, and the prompt text, its attendee list, its meeting date and its answer format (`task | owner | due`, `none`, `NONE`) are fixed in code. Why: the parser depends on the exact answer format the prompt asks for.

## Budget
- Budget: one model call per invocation with non-blank notes, zero for blank notes. No retry, no timeout and no cap on input length: the whole notes text goes into the prompt. No output token limit is passed to the model. Cost and latency scale with the length of the notes and depend on the callable. A failing model call raises to the caller; nothing catches it.
