# action_items charter

Input: meeting notes as free text, the attendee names, the meeting date, and a model (prompt string in, text out).
Output: a list of at most 10 `ActionItem(task, owner, due)`, dated items soonest first, undated items last in the model's order.

## Free
- Which notes count as an action item: the model separates commitments from decisions, opinions and things already done, because that judgement depends on the wording of the notes and code cannot read it.
- The task wording: the model writes a short imperative sentence, because rewording a commitment in context needs language understanding. Code only tidies it (see Constrained).
- Which attendee owns an item: the model reads who committed to it, including pronouns and "we", and picks a name from the list. Code only checks the name it picked.
- Whether a deadline was given and what date it means: the model resolves phrases like "by Friday the 6th" against the meeting date, which needs judgement that a parser cannot provide.
- Whether there are no items at all: the model answers `NONE` when nothing was agreed, so an empty result comes from its reading of the notes.
- Owner or deadline left unknown: the model writes `none`, which code turns into `None`.
- Order of undated items: the model's order is kept, because it reflects the order the notes were read in.

## Constrained
- Prompt text: fixed template with the meeting date, attendee list and notes filled in. Keeps the answer format and the rules stable across calls, so the parser can rely on them.
- Answer format `task | owner | due`, one per line, `NONE` for no items: the parser only accepts lines in this form, because free-form text cannot be checked.
- Blank notes: return `[]` without calling the model. Saves a call and avoids asking for items that cannot exist.
- Line handling: bullets and numbering stripped; the line is split from the right into exactly three fields, so a `|` inside the task is kept; any other line is skipped. Keeps chatter and malformed lines out without rejecting the whole answer.
- Header echo: a task that reads `task` is skipped, because it is the template header repeated back.
- Task text: whitespace collapsed, surrounding quotes and a final period removed; an empty task is skipped. Keeps tracker entries uniform.
- Task length: at most 120 characters, cut at a word boundary with `…`. Fixed output limit so each entry fits a tracker or a sent list; the 120 is a display choice, not a model limit.
- Owner: must match an attendee exactly after case and whitespace normalisation (`casefold`, collapsed spaces), and is returned with the caller's spelling; otherwise `None`, and the item is kept. Stops invented people from getting tasks; the attendee list is the real constraint. Matching is not fuzzy, so a first name alone gives `None`.
- Due date: `none` and similar placeholders (`n/a`, `tbd`, `-`, `?`, `unassigned`) give `None`; anything else must parse with `date.fromisoformat`, or `None`. Keeps the date field machine-readable. On Python 3.11+ `fromisoformat` also accepts compact forms such as `20260306`; that is accepted as is.
- Due date floor: a date before the meeting day is `None`; the meeting day itself is kept. A deadline before the meeting is almost always a model error, so it is dropped rather than shown.
- Due date ceiling: none. Any future date is accepted, since notes can set long deadlines.
- Duplicates: same task (normalised) and same owner, listed once; the first occurrence wins, including its due date. Stops the model repeating an item; a later copy with a date does not replace an earlier undated one.
- Sort: dated items ascending by date; undated items keep their order (stable sort). Puts the most urgent first, as the list is meant to be acted on from the top.
- Cap: at most `MAX_ITEMS = 10`, applied after sorting so the soonest survive. Stated output contract in the README; the cap is what the consumer expects, not a cost measure.
- Model failures: an exception from the model is not caught and reaches the caller; a non-text answer is not handled either. Errors are left to the caller, who can see the failure.

## Budget
- Budget: 1 model call per request with non-blank notes, no retry, no timeout in code. Prompt size is the template plus the attendee list plus the full notes, with no truncation; model output is read in full and only the first 10 sorted items are returned. Cost and latency are whatever one call of the caller's model costs.
