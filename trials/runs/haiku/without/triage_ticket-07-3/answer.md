Enterprise routine requests now land at `high` (8-hour answer, no page) instead of `urgent`, so only real outages should page the on-call.

**Cause:** `seam.py` raised every enterprise ticket one urgency level. A "high" request from an enterprise customer therefore became "urgent", which is why the invoice copy paged you.

**Changes in `triage_ticket_07-3`:**
- **`seam.py`, enterprise bump:** the bump now applies only to `low` and `normal`, so enterprise tickets top out at `high`. Enterprise `urgent` is unchanged.
- **`seam.py`, prompt:** the prompt now defines the levels by customer impact. `urgent` means something is broken for the customer right now. `high` means an answer is needed soon but nothing is broken. `normal` covers routine requests such as document copies, how-to questions and adding users.
- **`test.py`:** added tests for enterprise `high` staying `high` and enterprise `low` becoming `normal`. All 13 tests pass.
- **`README.md`:** updated to describe the cap and that only `urgent` should page.

**What this means for your two tickets:**
- The invoice copy becomes enterprise `high`: an 8-hour answer, ahead of ordinary 24-hour tickets, without paging.
- The Pro checkout failure stays `urgent` with a 1-hour answer.

**Limits:**
- The tests use a fake model, so the prompt change is not tested against the real one. Sample a week of real urgent tickets to check the model is not still labelling routine requests as urgent.
- The paging rule lives in your helpdesk tool, not in this code. Check that it pages only on `urgent`, and that the agents' list sorts by urgency and then by `respond_within_hours`.
- I chose the cap over a separate enterprise SLA field because it keeps the change small. If the contract needs a distinct "enterprise high" answer time, that would be a larger change.