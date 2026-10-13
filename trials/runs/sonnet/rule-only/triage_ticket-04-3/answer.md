Long tickets now reach the model with their end included, so the overcharge ticket should be routed on the 1,480 EUR request. The 12 tests pass, but they use a fake model, so I haven't checked how a real model routes your example.

**Cause:** `seam.py` cut the body to its first 2000 characters before the model saw it. In your example the three pages of quoted thread filled that budget, and the customer's new message never got through.

**Changes:**
- **`seam.py`:** a body over 2000 characters is now cut to its first 1000 and last 1000 characters, with a marker where the middle was dropped. Bodies under 2000 characters are sent whole, as before.
- **Prompt:** it now says the request can be anywhere in the message, often at the end after quoted emails, logs or backstory, and to answer from what the customer is asking rather than how the message begins. The queue, urgency and summary are still the model's to choose.
- **Tests and README:** the old test that asserted the tail was dropped is replaced by one asserting the start and end are kept, and the README describes the new behaviour.

**Limit:** a request buried in the middle of a very long body is still not seen. That is the 2000-character cap (`MAX_BODY_CHARS`), which I left alone because it is a cost and size decision that is yours to make. Raising it, or stripping quoted reply text before the model sees it, would cover more cases. Say if you want either.