Summaries longer than 120 characters now end on a whole word or sentence and are marked with `…`. All 15 tests pass.

**Behaviour** (`seam.py`, new `_shorten`):
- A summary that fits is left alone.
- If it doesn't fit, the leading whole sentences that fit are kept, followed by ` …`.
- If no whole sentence fits, it is cut at the last whole word that fits and ends in `…`, so it still fits in 120 characters.
- Your first example becomes "…seats used by the design team but wants to cancel the…".
- A single unbroken 200-character token is hard-cut with `…`, since there is no word boundary to use.

**Charter:** the 120-character cap and who decides what the summary says are unchanged. The model is still not asked to write shorter; code does the shortening. I added one sentence to the summary line in `evals/triage_ticket/charter.md` recording the new rule.

**Tests:** I changed `test_summary_is_one_line_and_capped`, which expected a mid-word cut, and added tests for the mid-word case, whole sentences, the unbroken token and a summary that already fits.

Note that `test_unknown_queue_goes_to_general` and the other default tests still pass, but the charter says defaults should be `null`. That is a separate, pre-existing gap and I left it alone.