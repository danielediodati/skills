Long tickets are now read much further, so your Pro-plan example would reach the model with the 1,480 EUR message in view. All 12 tests pass.

**Cause:** only the first 2000 characters of the body were sent to the model. Three pages of quoted thread used up all 2000, so the model only saw the delivery-address conversation. That's why it routed to shipping and summarised the address.

**Changes in `seam.py`:**
- **Cap raised:** `MAX_BODY_CHARS` goes from 2000 to 20000. The charter says the cap is a budget number that can be raised without moving a line. It is still one model call per ticket, with no chunking.
- **Prompt:** it now says the real request can be anywhere in the message, often at the end after quoted emails or logs, and that the model should triage what the customer is asking for now. This only informs the model's judgement. The queue, urgency and summary are still the model's decision.

**Tests:**
- The old test asserting the tail was dropped now checks against the cap constant.
- A new test builds a ticket with a long quoted delivery-address thread followed by the overcharge message, and checks the overcharge text reaches the model.

**What this doesn't cover:**
- **Very long tickets:** anything beyond 20,000 characters is still cut from the end, so a request after a huge log would still be missed. The charter rules out chunking, so a bigger cap is the only in-bounds lever. It costs more tokens per ticket, so tell me if you want a different number.
- **Verification:** the tests use a fake model. I couldn't check that the real model now routes your example to billing, so run a few real long tickets through it.
- **Existing discrepancy:** the charter says an invalid field should be `null`, not defaulted. The code still falls back to `general` and `normal`, and the charter notes this is "not yet in code". I left it alone since it's outside this request.