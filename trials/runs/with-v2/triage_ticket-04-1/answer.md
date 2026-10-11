Long tickets are now read much further, so your overcharge example should reach billing. I haven't run it against a real model, only the unit tests (12 pass).

**Cause:** `seam.py` sent the model only the first 2000 characters of the body. In your example, three pages of quoted thread used up all 2000, so the model only saw the delivery address and never reached the overcharge request.

**Changes:**
- **Cap raised** (`seam.py`): `MAX_BODY_CHARS` goes from 2000 to 12000. The charter lists the cap as a budget number that can be raised without moving a line, and it is still one model call per ticket.
- **Prompt addition** (`seam.py`): it now tells the model that the real request can be anywhere in the message, often after quoted threads or logs, and that quoted text and logs are context, not the request. This informs the model's judgement without dictating a queue or urgency.
- **Tests** (`test.py`):
  - The cap test now uses `MAX_BODY_CHARS` instead of a hard-coded 2000.
  - A new test checks that a request placed after a long quoted thread reaches the model.

**Remaining limits:**
- **Very long messages:** a message longer than 12000 characters is still cut at the end, so a request after that point is missed. Raising the cap further is safe under the charter, and costs only more tokens per ticket.
- **Charter and code disagree:** the charter says an invalid queue or urgency should be `null`, not defaulted. The code and its tests still use `general` and `normal`; the charter marks this as not yet in code. I left it alone since you didn't ask for it, but I can implement it if you want.
- **Charter text:** it says "today 2000 characters" for the cap. I didn't edit it, since only you change a charter.