Tasks now get an owner when the notes use a name that fits only one attendee. All 20 tests pass, including three new ones for this case.

**Cause:** the prompt asks the model for the owner "as written in the list", but it sometimes answers with just "Priya". The code then only accepted an exact full-name match, so "Priya" was dropped to `None`. That is why the same people gave different results from one meeting to the next.

**Fix (`seam.py`):** a new `_resolve_owner` handles the owner name.
- A full name (any case or spacing) matches as before.
- Otherwise, the words given ("Priya", or a surname) must belong to exactly one attendee, and that attendee is the owner.
- If two attendees fit (two Toms, notes say "Tom"), the item stays in the list, unassigned.
- If the model writes the full name ("Tom Alvarez"), it still resolves even when first names collide.
- Names that are not attendees, and "none", still give no owner.

Your Tuesday example would now give Priya Raman for the badges and Tom Becker for the room.

I did not touch the charter or the prompt. The model still decides who owns each task; the code only matches its answer to an attendee.

The charter says owner is free text and flags that the code currently keeps only attendees. I left that as is, so someone who is not in the meeting still comes out unassigned. Moving that line is your call.