Long tickets are now sent to the model in full, so a request at the end of the message, like the 1,480 EUR overcharge, is no longer cut off. All 11 tests pass. I haven't run it against a real model, so I haven't confirmed that your ticket now lands in billing.

**Cause:** `triage_ticket` only sent the first 2000 characters of the body. In your example the three pages of quoted address thread filled that budget, so the model only saw the delivery-address exchange and routed on that.

**Changes in `seam.py`:**
- **Truncation:** I removed the 2000-character cap (`MAX_BODY_CHARS`), so the model reads the whole body.
- **Prompt:** I added a short note that the message may open with quoted history, a log or a long story, and that the real request can be anywhere, often at the end. This is guidance only. The model still picks the queue, urgency and summary, and the code's validation and fallbacks are unchanged.

**Test:** `test.py` previously asserted that the tail of a long body is not sent. It now asserts the tail is sent.

**Decision for you:** with no cap, a very large body (a huge log, say) goes into the prompt as is, which affects cost and context limits. If you want a ceiling, the options are:
- a much larger cap that keeps the start and the end, so the middle is what gets dropped;
- a separate step that strips quoted reply text before triage.

Either one means code decides what the model doesn't see, so I left that choice to you.