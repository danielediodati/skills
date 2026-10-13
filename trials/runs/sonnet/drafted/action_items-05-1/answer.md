Your list can no longer be shortened without saying so, but it is still capped at 10 and still drops undated items first. All 20 local tests pass; nothing paid was run.

**Cause:** the charter caps the list at 10 and applies the cap after sorting, so undated items are cut first. Your 14 items became 10, and the four undated ones (the venue contract, the legal question and two others) were the ones lost. The code gave no sign that anything was cut.

**What I changed** (`seam.py`, `test.py`, `README.md`):
- **New function:** `extract_with_report(...)` returns the same capped list plus `omitted`, the number of valid items the cap removed. For your planting day that would have been `omitted = 4`.
- **Unchanged:** the model call, the sort and the cap are as before, and `extract_action_items` still returns a plain list.
- **Counting:** duplicates collapsed by deduplication are not counted as omitted.
- **Tests:** three new tests cover the count, the no-cut case and duplicates.

**Still to do:** the tool that builds the message you send round has to call `extract_with_report` and add something like "4 more follow-ups were left out" when `omitted > 0`. I can't see that tool from this repo.

**Your decision:** getting all 14 in front of you means moving a line the charter holds, so I stopped short of it. Two ways to do that:
1. **Raise the cap** (for example to 20 or 30). The charter calls 10 a budget that may be raised, but it is your call. It buys a complete list for typical long meetings, at the cost of a longer list to send round.
2. **Return the dropped items** alongside the list, in a separate "also agreed, not listed" section. This keeps the 10-item list short but puts every follow-up in front of you.

Tell me which you prefer, or both, and I'll make the change. I will not edit the charter, so its text will need to be updated by you.