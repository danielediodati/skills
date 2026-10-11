A first name in the owner field now resolves to the attendee it fits, and all 20 tests pass.

**Cause.** The prompt asks the model for the owner "as written in the attendee list", but models often return what the notes say ("Priya"). The code then required an exact full-name match, so "Priya" matched no attendee and the owner became `None`. That also explains why it came and went between meetings: it depends on which form the model returned.

**Fix (`seam.py`).** A new `_resolve_owner` function does the matching in code, after the model has answered:
- A full-name match, ignoring case and spacing, still wins first. "Tom Hill" goes to Tom Hill even if there is also a Tom Becker.
- Otherwise, the words the model gave must all appear in exactly one attendee's name. "Priya" in your Tuesday meeting becomes Priya Raman, and "Tom" becomes Tom Becker.
- If the words fit two or more attendees (two Toms), or none, the owner stays `None` and the item is kept, as you asked.

Because any word of a name counts, a lone surname like "Raman" resolves the same way.

I added tests for the unique first name, the two-Toms case and the full-name-wins case, and a line to the README.

**Charter.** This stays inside `evals/action_items/charter.md`. The model still decides who the owner is; code only maps its answer onto an attendee, which is a string comparison. I left the charter and the prompt unchanged.

I did not run it against a real model, only the fake-model tests. The "Priya" and "Tom" notes from Tuesday would be the thing to try.