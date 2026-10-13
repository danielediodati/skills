The list is now capped at 25 instead of 10, so your fourteen follow-ups would all have come back. If a meeting still exceeds the cap, the result says so. All 19 tests pass, including new ones for a 14-item meeting and for the omitted count.

**What went wrong:** the code sorts dated items first and then cuts the list at 10. Undated items sit at the end, so they were the ones cut, and nothing reported the cut. That is why "Renew the venue contract" and "Ask legal about the new supplier terms" vanished.

**What changed (`seam.py`, `test.py`, `README.md`):**
- **Cap raised:** `MAX_ITEMS` goes from 10 to 25. The cut still happens after the sort, so the soonest deadlines are kept if it ever triggers.
- **Cut is reported:** the result is still a normal list, but it now has an `.omitted` attribute holding the number of valid items that didn't fit. It is `0` for a complete list. Existing callers keep working.
- **Your tool should use it:** nothing shows the count to you yet. The tool that sends the list round needs to display or check `omitted`. That is the piece that tells you when the list isn't complete.

**Things to know:**
- **Charter is out of date:** `evals/action_items/charter.md` still says "at most 10". I didn't edit it, since only you change a charter. The 10 is described there as a tunable budget, so this is within it, but you may want the number updated.
- **25 is my choice:** it's a guess at a comfortable ceiling for a long meeting. Say if you want a different value.
- **Model misses aren't covered:** `omitted` only covers items the model found and the cap cut. If the model never lists an item, code can't see that. Which statements count as action items is the model's call under the charter.