The list no longer drops items silently. When more than ten items come back, the result now says how many were left out. The cap itself is unchanged, so your planning day would still show only ten items.

**What changed**
- `seam.py`: a new `extract_action_items_report` returns the items plus `omitted`, the count of checked items beyond the cap. `extract_action_items` behaves as before.
- `test.py`: two new tests, one where the cap cuts items and one where it doesn't. All 19 tests pass.
- `README.md`: a short note on the new function.

**The line I didn't move:** the charter lists the cap of 10 as constrained. Removing it would let all fourteen items through, but that is a charter change, and only you can make it. The charter also calls the cap a "display choice", which is the assumption that caused this. If you want the full list, that is the decision to make. Raising `MAX_ITEMS` or dropping the cap would do it, and then you'd update the charter.

**What the count doesn't cover:** it counts only items cut by the cap. If the model left items out of its answer altogether, the count won't show that. I haven't made any model calls, so I can't tell you how often that happens.