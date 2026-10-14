I haven't changed any code. Getting complete reasons within 80 characters means moving a line the charter sets, so that decision is yours.

**The line:** `evals/recommend_products/charter.md` (Constrained) says the reason is "cut to 80 characters by a plain slice (may end mid-word)" and that "Code truncates rather than asking the model to shorten, so no extra call is needed." The cut happens in `seam.py:56`. The model writes the reason text and doesn't know about the limit, so a cut is the only thing that makes a long reason fit.

**Why the smaller fixes don't work:**
- **Cut at a word boundary:** stops the mid-word break, but the reason still ends as a fragment ("…the battery easily lasts a whole"). It also changes the charter's stated behaviour.
- **Blank the reason when it's too long:** avoids fragments, but the pick shows with no reason, and that also changes the charter's stated behaviour.
- **Ask the model for a shorter reason, or a second call to shorten:** the only route to complete thoughts. The prompt approach adds a length instruction, which moves the "code truncates, not model" line. The second call also breaks the "exactly one model call, no retry" line.

**What I'd recommend:** add a length instruction to the prompt (`seam.py:10`) asking for one complete sentence of at most 80 characters, and keep the `[:80]` slice as a backstop. The backstop means a rare long reply still gets cut, so it's not a guarantee. It also costs nothing extra per search. Because it moves the line, the charter needs updating, and you'd make that change. Quality can only be checked with paid eval runs, so I'd need your approval and a spending budget for the ticket before running any.

The unit tests pass (13 of 13, no model calls). Tell me which option you want. If it's the prompt change, I'll make it once the charter says so, and I'll agree a budget with you before any paid check.