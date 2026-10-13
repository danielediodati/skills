The prompt now tells the model the limit, so it should write reasons that fit. This does not guarantee every reason is complete, and I stopped short of the part that would.

**What I changed**
- `seam.py`: the prompt now says each reason is shown on one line of at most 80 characters and is cut off after that. It asks for a complete thought written to fit, not a longer one trimmed. The number comes from `MAX_REASON_CHARS`, so the two can't drift apart.
- `test.py`: added a test that the prompt states the limit. All 14 tests pass.

**Why this works, and where it falls short**
Until now the model was only asked for "one short reason" and never told about the 80-character display limit, so it wrote natural sentences that code then chopped. Telling it the limit is information for its judgement, which the charter allows, and wording stays the model's call. Your space budget is unchanged.

The code-side hard cut remains as a backstop, so if the model still overruns, that reason will still be cut mid-word. Stopping that for certain would mean moving a line the charter fixes, and only you can decide that. The options:

1. **Trim at a word or sentence boundary in code.** This avoids mid-word cuts but can still leave a clipped thought, and the charter explicitly says "may cut mid-word".
2. **Drop or blank over-length reasons.** Nothing broken is ever shown, but some products would appear with no reason.
3. **Allow one retry or rewrite call for over-length reasons.** This is the only option that yields a complete thought every time, but it breaks the "exactly one call, no retry" rule and adds latency and cost to the strip.

I'd try the prompt change first and check real results. If truncated reasons still show up, option 3 is the one that meets your goal, at a cost you'd need to accept. Let me know if you want to change the charter.