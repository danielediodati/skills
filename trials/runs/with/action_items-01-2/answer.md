A first name in the owner field now resolves to the one attendee who has it, and an ambiguous name stays unassigned. All 19 tests pass, including two new ones for this.

**Cause:** the model often writes the owner as it appears in the notes ("Priya"), and the code only accepted an exact, case-insensitive match against the full attendee names. "Priya" matched nothing, so the owner became `None`. It was intermittent because the prompt asks for the name "as written in the list", and the model only sometimes follows that.

**Change in `seam.py`:** a new `_match_owner` replaces the exact-name lookup.
- A full name still matches as before, case-insensitively.
- Otherwise, the words the model wrote must all appear in exactly one attendee's name. "Priya" becomes Priya Raman.
- With two Toms in the room, "Tom" stays unassigned, while "Tom Fischer" still resolves.
- The owner returned is always the attendee's name as the caller spelled it.

**Tests in `test.py`:** one covers a unique first name resolving, and one covers a shared first name staying unassigned.

**Charter:** the owner is still the model's call, and the code only maps the model's answer onto an attendee. That seemed to keep the line where it was, so I added one line to the Constrained section of `evals/action_items/charter.md` describing the matching rule.

The prompt is unchanged.

The match also accepts any whole word of a name, so a surname alone ("Raman") resolves too. If you want first names only, that is a small tightening.