Long tickets are now read in full, so a request at the end of a message reaches the model. The 11 tests pass. I didn't run it against a real model, so I haven't confirmed that your 1,480 EUR ticket now lands in billing.

**Cause:** `seam.py` cut the body to its first 2000 characters before the model saw it. In your Pro-plan ticket, the three pages of quoted address thread filled that window and the overcharge message was never sent. The model summarised the delivery address because that was all it had.

**Changes**
- **`seam.py`:** I removed the `MAX_BODY_CHARS` truncation, so the whole body goes to the model.
- **Prompt:** I added a short instruction that the request can be anywhere in the message (after a quoted thread, a pasted log or a long story), and that quoted earlier messages are background. This only tells the model where to look. The queue, urgency and summary are still its own decisions, and the queue list, fallbacks and enterprise bump are unchanged.
- **`test.py`:** `test_only_the_start_of_a_long_body_is_sent` asserted the old truncation. I replaced it with a test that a request placed after 500 quoted lines reaches the prompt.

**Decision for you:** with no cap, a very large paste (a multi-megabyte log) goes to the model as is, which costs more and could exceed its context window. If you want a ceiling, the simplest is a high one, such as the model's context limit. A ceiling would reintroduce truncation for tickets beyond it, and I didn't want to pick that threshold for you.