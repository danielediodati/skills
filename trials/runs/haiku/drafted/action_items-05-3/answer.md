The list still stops at 10, and the undated items are still the ones that get cut. Removing that limit would change a charter line, and the charter says that is your decision. What I did change is that the cut now shows up.

**The line that's stuck:** `evals/action_items/charter.md`, Constrained: "Cap of 10 items, applied after dedupe and sort, so the soonest deadlines survive." It is marked "product decision." It interacts with the ordering line, which puts undated items last. Together they cut exactly the undated follow-ups, which is what happened at your planning day. If you raise the cap, you get the full list but a longer one to read. If you want undated items kept in a different place, that's the ordering line, and it's yours to decide too.

**What I changed in `seam.py`:**
- New `extract_with_overflow(...)` returns `(items, overflow)`. `overflow` is the number of items the cap cut.
- `extract_action_items` is unchanged in behaviour and now calls it, so the returned list is the same as before.
- The README mentions the new function.

**Tests:** 21 pass, including four new ones for the count. Your case is covered: 14 follow-ups with 4 undated, showing 10 and an overflow of 4. I made no paid model calls and did not touch the charter.

**What I can't confirm:** I can't tell from the code whether the model returned all 14 or only 10. The cap explains the pattern, but the raw model answer would settle it. From now on, if `overflow` is above 0, you know the list is incomplete before you send it.

For the planning day itself, the four missing items are Tom's venue contract, Priya's legal question, and two others. I don't have your notes, so I haven't re-run them. Re-running would be a paid call, which needs your approval first.