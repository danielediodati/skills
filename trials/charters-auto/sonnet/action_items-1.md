# action_items charter

Input: free-text meeting notes, the attendees' names, the meeting date, and a model callable (prompt string in, string out).
Output: at most 10 `ActionItem(task, owner, due)`, soonest deadline first, undated last; `[]` if nothing was agreed.

## Free
- What counts as an action item: the model judges what is a commitment to do after the meeting versus a decision, opinion or thing already done; notes are unstructured and only judgement can tell them apart.
- Whether an item exists at all, and how many it finds: the model reads the notes and may return none (`NONE`); code only caps the count afterwards.
- Task wording: the model writes a short imperative sentence in its own words; paraphrasing messy notes is what it is there for.
- Who owns an item: the model decides who took it and maps a mention ("Ana", "she", "the sales lead") to an attendee name from the list, or says none; code only checks the result.
- The deadline's value: the model resolves relative or partial expressions ("Friday the 6th", "end of next week") against the meeting date into YYYY-MM-DD, or none if no deadline was given.
- The order of undated items and which of several duplicates comes first: they follow the model's order; no ranking is imposed.

## Constrained
- Number of model calls: exactly one per invocation, no retry, no repair or second pass; keeps cost and latency fixed. A failure or unusable answer yields fewer or no items, not another call.
- Blank notes: return `[]` without calling the model; nothing to extract, nothing to pay for.
- Answer format: only lines of the form `task | owner | due` are used (bullets/numbering tolerated, split from the right so a task may contain `|`); chatter, the echoed header, wrong field counts and empty tasks are skipped. This makes the free-text answer machine-checkable; the form is fixed in the prompt and the parser together.
- Owner must be an attendee: matched by case- and whitespace-insensitive equality with the supplied names and returned as the caller spelled it; anything else (unknown person, `none`, a first name only, a variant spelling) becomes `None` but the item is kept. Prevents invented owners reaching a task tracker; the exact-match rule is strict, so a partial name loses the owner rather than guessing.
- Due must be a real date on or after the meeting date: unparsable, impossible or earlier dates become `None` and the item is kept; a wrong date is worse than none. The meeting day itself is allowed. There is no upper bound on how far ahead a date may be.
- Empty markers (`none`, `n/a`, `-`, `?`, `tbd`, `unassigned`, blank) mean no owner / no due; a fixed closed list.
- Deduplication: same normalised task (case, spacing, quotes, trailing period) and same resolved owner is listed once, first occurrence kept. Matching is textual, not semantic, and happens after owner resolution, so unknown owners collapse together as `None`.
- Task length: cut to 120 characters at a word boundary with a trailing "…"; keeps the list short enough to send round. 120 is a display limit that could be changed, not a correctness rule.
- Ordering: dated items by deadline, undated last, stable in the model's order; fixed so the list reads as a follow-up by urgency.
- Cap of 10 items, applied after sorting so the soonest deadlines survive and undated items are dropped first. 10 is today's size of a list, a budget that may be raised; the sort-then-cap order is the constraint.
- Items are never dropped for a missing owner or date: an item with neither is still a valid output.

## Budget
- Budget: one model call per run; one prompt containing the whole notes (no chunking or truncation of notes, so very long notes are bounded only by the model's context); at most 10 items and 120 characters per task returned.
