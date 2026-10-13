Long tickets are now read much further, so a request that comes after a quoted thread, a pasted log or a long story reaches the model. All 12 tests pass, but I haven't run it against a real model, so I can't yet say your 1,480 EUR ticket would land in billing.

**Cause:** only the first 2000 characters of the body were sent to the model. In your ticket, three pages of quoted address discussion filled that window, so the model never saw the overcharge request.

**Changes in `seam.py`:**
- **Body limit:** `MAX_BODY_CHARS` goes from 2000 to 12000, roughly 3,000 tokens per call. The charter describes this number as a budget that can be raised, so this stays within it.
- **Prompt:** I added a short instruction that the request can be anywhere in the message, after quoted emails, logs or a story, and that the ticket should be judged on what the customer is asking now. It only informs the model's judgement. The model still chooses queue, urgency and summary, and the queue and urgency lists, fallbacks, enterprise uplift and deadlines are unchanged.

**Tests:** I added one test that puts a request after about 3,000 characters of quoted thread and checks it reaches the model. The existing truncation test now uses `MAX_BODY_CHARS`.

**Remaining gaps:**
- **Charter is stale:** it still says 2000 characters. I can't edit the charter, so please update that line to match the new budget.
- **Very long tickets:** a message over 12,000 characters, such as a huge log, can still have its final paragraph cut off. Sending the start and end of the body instead of only the start would fix that, but it changes the charter's rule that only the first N characters reach the model. That is your decision. Say so if you want it and I'll make it once the charter allows it.