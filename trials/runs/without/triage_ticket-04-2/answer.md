Long tickets are now routed on both their opening and their closing text, so the overcharge ticket's request actually reaches the model. All 12 tests pass.

**Cause:** `triage_ticket` sent only `body[:2000]` to the model. In your Pro-plan example the three pages of quoted thread used up that budget, so the model saw only the delivery-address exchange. Your pasted-log and story-first cases fail the same way.

**Changes in `seam.py`:**
- **Head and tail:** a body over 2000 characters is cut to the first 1000 and the last 1000, joined by an `[... middle of the message omitted ...]` marker. The prompt size is unchanged, and bodies of 2000 characters or less are sent whole.
- **Prompt:** it now tells the model that the real request can be anywhere, often at the end under a quoted thread or log. It is told to route and summarise on what the customer is asking now, not on how the message begins.

**Tests:** I replaced `test_only_the_start_of_a_long_body_is_sent`, which asserted the old behaviour (the tail must not be sent). The new tests check that a long body keeps both ends and that a body exactly at the limit is untouched.

**Limits:**
- **Middle of the message:** a request buried in the middle of a very long message can still be missed. Raising `MAX_BODY_CHARS` is the simple fix if your model and cost allow it.
- **Quoted text:** I did not strip quoted lines (`>` prefixes, "On … wrote:" blocks). That would free more room for the new message, but it could also remove `>` lines from pasted logs, so I left it out. Say if you want it added.
- **Not run against a real model:** the tests use a fake model, so I haven't checked how well the new prompt wording works on real tickets. Run a few real long tickets, including the overcharge one, through it before relying on it.