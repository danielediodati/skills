I made the part of the fix the charter allows. It is only partly verified, and a full fix needs a decision from you.

## What was wrong
`seam.py` sent the model only the first 2000 characters of the body. In your Pro-plan ticket the quoted address thread filled that window, so the model never saw the overcharge request. The same would happen with a long pasted log followed by the question.

## What I changed
- **`seam.py`, prompt:** it now tells the model that the request can be anywhere in the message, with quoted history or logs first, and to judge by what the customer is asking for now. This only informs the model's judgement. Queue, urgency and summary are still its own decisions.
- **`seam.py`, `MAX_BODY_CHARS`:** raised from 2000 to 12000. The charter lists this cut as a raisable budget, so the change stays inside it. A three-page quoted thread should now fit.
- **`test.py`:** the existing "only the start is sent" test now uses the constant instead of a literal 2000. I added a test that a request after a long quoted thread reaches the model, and one that the prompt carries the new hint.

All 13 unit tests pass. That is a free local check only, with no model calls.

## What this does not cover
- **Not confirmed on a real model.** The unit tests show the billing request now reaches the model. They don't show the model routes it to billing. That needs a paid eval run, which I haven't started.
- **Still not "wherever in the message".** A body longer than 12000 characters loses its tail, which a huge pasted log could do. Fixing that means changing the charter's constraint that the model sees only the first N characters. For example, it could send the head plus the last N characters, or the full body. That moves a line, so it is your decision.
- **Cost.** Long tickets now send up to about 6x the body text per call. 12000 was my estimate, not a measured number, so adjust it if you want a different trade-off.
- **The charter is now stale.** It still says 2000 in the "Context sent to the model" and "Budget" sections, and I can't edit it. Please update those numbers if you keep 12000.

## Next steps
1. Decide whether to keep 12000 or move to head+tail or the full body.
2. If you want a real-model check on the example ticket and a few long-log cases, tell me a spending budget for this ticket, and I'll show a cost estimate before the first paid call.