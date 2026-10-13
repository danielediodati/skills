# action_items charter

Input: free-text meeting notes, the attendee names, the meeting date, and a model (prompt string in, string out).
Output: a list of at most 10 `ActionItem(task, owner, due)`, soonest deadline first, undated last.

## Free
- What counts as an action item: the prompt asks the model to judge what a person committed to do after the meeting, and to leave out decisions, opinions and work already done; notes are unstructured, so no rule in code can tell these apart.
- Which attendee owns an item: the model reads who took it on, including from nicknames, first names or pronouns, and writes the name as listed; code only checks the result, so a wrong but valid name passes unchecked.
- Whether an item has an owner at all: the model may answer "none" when nobody took it; code never assigns or guesses an owner.
- The deadline's value: the model turns "by Friday the 6th" or "next week" into YYYY-MM-DD using the meeting date in the prompt; calendar reading is language work, and code only checks the format and the floor.
- Whether an item has a deadline at all: the model answers "none" when none was given, and code never invents one.
- Task wording: the model writes a short imperative sentence in its own words, so items read cleanly without the notes; code only trims it.
- How many items and in what order among undated ones: the model decides how many items the notes hold and what order it lists them in; code keeps that order for undated items (the sort is stable).

## Constrained
- One call, no retry: the model is called exactly once per request, and a bad or empty answer is not retried (tests assert one prompt); this keeps cost and latency flat, and retrying would turn a malformed answer into a slower, costlier one.
- Blank notes skip the model: whitespace-only notes return `[]` without a call, so nothing can be invented from nothing.
- Answer format is `task | owner | due`: any line that does not split into three fields, or has an empty task, or echoes the `task` header, is dropped silently; this tolerates chatter and a `NONE` answer, but a wholly malformed answer looks the same as "no items". Bullets and numbering are stripped and a pipe inside the task is allowed (split from the right).
- Owner must be an attendee: matching ignores case and spacing, the value returned is the caller's own spelling, and anything else (including a first name only, or a person outside the meeting) becomes `None` while the item stays; this keeps invented names out of a tracker, and dropping the item would lose a real commitment.
- Deadline must be a real ISO date on or after the meeting date: unreadable, impossible or past dates become `None` while the item stays; a wrong date sent to a tracker is worse than none. There is no upper bound, so a far-future date passes.
- Tasks are cleaned: whitespace collapsed, wrapping quotes and a final period removed, and tasks over 120 characters cut at a word boundary with "…"; the 120 is a display budget for lists and trackers, not a semantic rule.
- Duplicates collapse on (task, owner): comparison ignores case and spacing; the first occurrence wins, so a later duplicate with a deadline is lost; a same task for two owners is kept as two items.
- Order is by code: dated items soonest first, undated last; the model's order matters only among undated items and ties.
- At most 10 items, cut after sorting: the soonest deadlines survive and the undated ones are dropped first, with no sign to the caller that anything was cut; 10 is a product limit for a follow-up list and today's value, not a safety property.
- Model failures are not handled: an exception from the model propagates to the caller, and there is no fallback.

## Budget
- Budget: one model call per request, with a prompt of the notes plus a short fixed instruction and the attendee list; no timeout or token limit is set in the seam. Output is bounded by `MAX_ITEMS = 10` and `MAX_TASK_CHARS = 120`, both display limits that may be raised.
