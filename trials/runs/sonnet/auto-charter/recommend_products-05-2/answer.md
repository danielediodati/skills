I made part of the fix. Cut-off reasons can still appear, because the one change that would guarantee complete reasons needs your decision.

**Cause:** the model never knew about the 80-character limit. It wrote reasons of any length, and the code then cut each one at 80 characters, even mid-word (`seam.py`, `MAX_REASON_CHARS`).

**What I changed:**
- **Prompt:** it now tells the model the reason is shown in a space of 80 characters, that longer text is cut off, and to write one complete sentence that fits. The limit comes from `MAX_REASON_CHARS`, so the prompt and the cut can't drift apart.
- **Test:** `test.py` has a new test that the prompt states the limit. All 14 tests pass.
- **Space:** the reason's space stays at 80 characters, so it doesn't grow.

**What remains:** this makes cut-offs much rarer, but it cannot guarantee them away. The model can still overrun, and when it does the code still cuts at 80 characters. The charter fixes that cut as a display limit that "may cut mid-word", so I haven't touched it.

**The decision for you:** to guarantee that no reason is ever cut mid-sentence, the charter's reason-shape line would need to change. These are the options, each of which only you can choose:
- **Trim at a word boundary or add an ellipsis:** no broken words, but the thought can still be incomplete. This is the cheapest option.
- **Drop an over-length reason and show none:** the product is still shown, with no text under it. This guarantees no partial sentence appears.
- **Ask the model to rewrite an over-length reason:** this gives complete thoughts but needs a second model call. That breaks the "exactly one call" rule, which keeps latency and cost fixed.

Tell me which of these you want (if any) and amend the charter, and I'll implement it.