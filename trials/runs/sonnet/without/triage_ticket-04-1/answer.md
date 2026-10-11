Long tickets are now routed on the whole message, not just its opening. The 13 tests pass, but I only tested with a fake model, so I haven't seen how a real model routes your 1,480 EUR ticket.

**Cause:** `triage_ticket` sent only the first 2000 characters of the body to the model (`body[:MAX_BODY_CHARS]`). In your example, three pages of quoted thread filled that window, so the model never saw the overcharge message and summarised the address thread.

**Changes in `seam.py`:**
- **Quoted lines removed:** lines starting with `>` are dropped before sending. If that would leave nothing, the original body is kept.
- **Higher limit:** the cap goes from 2000 to 12000 characters, enough for most long threads and logs.
- **Both ends kept:** if a body is still over the cap, the middle is cut and a `[...]` marker is left. The head gets 25% and the tail 75%, since the newest message and the final ask usually come last.
- **Prompt instruction:** the model is told the request can be anywhere, often at the end, and that quoted messages, logs and backstory are context rather than the request.

**Tests in `test.py`:** I replaced `test_only_the_start_of_a_long_body_is_sent`, which asserted the old behaviour, with three tests:
- A request after a long quoted thread reaches the model, and the quoted text doesn't.
- A question after a long unquoted log reaches the model, and the prompt stays under the cap.
- A huge body keeps both its start and its end.

**Limits:**
- Quoting is detected only by a leading `>`. Clients that quote with "On … wrote:" blocks or Outlook-style headers without `>` are not stripped. They fall under the 12000 cap instead, which still keeps the tail.
- A body over 12000 characters whose ask is in the middle could still lose it. That seems rare, but say if you want a different head/tail split or a larger cap.
- The README still doesn't mention how long bodies are handled; I left it unchanged.