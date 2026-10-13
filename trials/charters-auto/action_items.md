# action_items charter

Input: free-text meeting notes, the attendees' names, the meeting date, and a model (prompt string in, string out).
Output: a list of at most 10 `ActionItem(task, owner, due)`, soonest deadline first, undated last. Owner is an attendee or `None`; due is a date on/after the meeting or `None`.

## Free
- Which statements in the notes are action items: the model separates commitments from decisions, opinions and things already done, which no rule can do over free text.
- How many items it finds and in what order it lists them: code only dedupes, sorts and caps afterwards; the model's order is the tie-break among undated items (and so decides which undated ones survive the cap).
- Wording of each task: the model writes a short imperative sentence in its own words; code only trims it.
- Who owns an item: the model reads who took it, resolving "I", first names and nicknames to an attendee name as written in the list, or says `none` if nobody took it.
- What the deadline is: the model turns "Friday the 6th", "end of next week" and similar into a `YYYY-MM-DD` using the meeting date given in the prompt, or `none` if no deadline was given.
- What to do with a pipe, bullet, quote or stray spacing it emits: tolerated by the parser, not asked of the model.

## Constrained
- Number of model calls: exactly one, no retry, no repair, no second pass; a bad answer degrades to fewer or emptier items rather than costing another call. Model exceptions are not caught.
- Blank notes: return `[]` without calling the model, so nothing is billed and nothing can be invented from an empty input.
- Answer format: only lines of the form `task | owner | due` count (after stripping bullets/numbering, split from the right so a task may contain `|`); chatter, the echoed header, lines with the wrong field count and empty tasks are dropped silently, so the output is machine-loadable. `NONE` yields an empty list.
- Owner: kept only if it matches an attendee after whitespace/case normalisation, and then returned as the caller spelled it; anything else (absent person, `none`, nickname, first name only) becomes `None` but the item is kept. Code never guesses a closer match, so a task is never assigned to a person who was not named, and the caller can rely on the owner being one of their strings. The cost is that a sloppy but correct owner is lost, not the task.
- Due date: kept only if it parses as an ISO date (`date.fromisoformat`) and is on or after the meeting date; empty-like values (`none`, `n/a`, `-`, `?`, `tbd`, `unassigned`) and invalid or past dates become `None`, item kept. The code never repairs or infers a date, so a hallucinated or impossible deadline never reaches a tracker. There is no upper bound; a far-future date is accepted.
- Task length: at most 120 characters, cut at a word boundary with an ellipsis; surrounding quotes and a trailing period are stripped. The 120 is a display limit for the follow-up list, today's value of a tunable.
- Duplicates: the same task (case/whitespace-insensitive, after cleaning) for the same resolved owner is listed once, the first one wins, including its due date. Two items with unknown owners collapse together because both resolve to `None`. Same task for different owners is kept.
- Order: dated items by ascending deadline, then undated items in the model's order (stable sort).
- Cap: 10 items, applied after sorting so the soonest deadlines are kept and undated items are dropped first. The 10 is a budget on how long a follow-up list may be, not a structural limit; it can be raised, but the cut must stay after the sort.
- Prompt inputs: attendees are passed as a comma-joined list and notes are stripped; the prompt fixes the three-field format and the YYYY-MM-DD / `none` conventions that the parser depends on, so changing one means changing the other.

## Target and budget
- Budget: one model call per meeting, with the notes plus a short fixed prompt as context; no retries. Output of at most 10 items of at most 120 characters each; 10 and 120 are tunable budgets, the other rules are the contract.
