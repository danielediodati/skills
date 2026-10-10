Tasks now get an owner when the notes use a name that fits exactly one attendee; all 19 tests pass.

**Cause:** the model correctly answered "Priya" (as the notes say), but the code only accepted an exact full-name match against the attendee list. "Priya" didn't match "Priya Raman", so the owner became `None`. It was intermittent because the model sometimes expanded the name to the full form and sometimes didn't.

**Fix (`seam.py`, new `_resolve_owner`):**
- A full name still matches as before.
- Otherwise, a partial name (first name or surname) resolves to the attendee only if exactly one attendee contains it.
- If two attendees fit, such as two Toms and the notes say "Tom", the item stays unassigned. "Tom Lund" written in full still resolves.

I added tests for the unique first name case and the two-Toms case.

I left the prompt and the charter untouched. The change only decides which attendee the model's owner text refers to; who the owner is remains the model's call. The charter's wish to keep owners who aren't attendees is still not implemented, and this change doesn't affect that.