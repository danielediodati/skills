# action_items charter

Input: free-text meeting notes, the attendees' names, the meeting date, and a model (callable prompt -> text).
Output: a list of at most 10 `ActionItem(task, owner, due)`, soonest deadline first, undated last.

## Free
- What counts as an action item: the prompt asks the model to judge what someone committed to do after the meeting and to leave out decisions, opinions and things already done; notes are unstructured and no rule can tell these apart.
- How many items it proposes and in what order it lists them: code only trims the result, and the model's order decides undated items' order and which of them survive the cap.
- The wording of each task: the model rewrites loose notes into a short imperative sentence; code only normalises whitespace, quotes, trailing period and length.
- Who owns an item: the model reads who took it and maps nicknames or first names to an attendee, or says "none" when nobody took it.
- The deadline's value: the model turns "by Friday", "next week" or "the 6th" into a YYYY-MM-DD date using the meeting date given in the prompt; code does no date arithmetic on natural language.

## Constrained
- Notes that are blank never reach the model and return `[]`: nothing to extract, so no call is spent.
- One call, no retry or repair: a bad answer degrades to fewer items or `None` fields instead of costing more calls; a model exception is not caught.
- The answer's shape is `task | owner | due` per line: other lines (chatter, header echo, "NONE", lines without three fields, empty task) are skipped, so unparseable text can never become an item. Bullets, numbering and stray spacing are tolerated; split is from the right so a task may contain "|".
- Owner must be an attendee, matched ignoring case and spacing and returned as the caller spelled it: an invented or absent person must not be assigned work. A non-match (including "none", a first name only) keeps the item with `owner=None` instead of dropping it, so a commitment is not lost.
- Due must be an ISO date on or after the meeting date: an unreadable, impossible or past date is more likely a model error than a deadline, so it becomes `None` and the item stays. Same-day is kept.
- Deduplication on (normalised task, resolved owner): the first occurrence wins and its due date is kept, later ones are dropped. Because it runs after owner resolution, the same task given to different non-attendees collapses into one unowned item.
- Task length is capped at 120 characters, cut at a word boundary with "…": keeps the list short enough to send round or load into a tracker.
- Sorting is by due date with undated last, stable: the list reads as a follow-up in deadline order; code, not the model, owns the order of dated items.
- At most 10 items, applied after sorting so the soonest deadlines survive: bounds the list's size. 10 is a product choice about readability, not a technical limit, and may be raised; extra items beyond it are silently discarded.

## Budget
- Budget: one model call per invocation, with the full notes in the prompt (notes are not truncated or chunked); no retries, no timeouts set by the seam.
