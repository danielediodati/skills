Owners written as a first name now resolve to the one attendee that name fits. All 20 tests pass, including three new ones for this case.

**Cause:** the model was asked to answer with the owner's name "as written in the list", and it often wrote just "Priya". The code then required an exact full-name match, so "Priya" was dropped to no owner. That is also why it only happened on some runs: the model sometimes wrote the full name and sometimes didn't.

**Changes in `seam.py`:**
- **Owner matching:** a new `_resolve_owner` first tries the full name, as before. Failing that, it accepts a partial name ("Priya", or "Raman") if it fits exactly one attendee.
- **Ambiguous names:** with two Toms in the room, "Tom" stays unassigned. A full name like "Tom Ruiz" still resolves.
- **Prompt:** I added a sentence telling the model that notes often use first names, to pick the person when only one fits, and to write "none" when more than one does.

**Limit:** if the model itself picks one of two Toms and writes the full name, the code can't tell it guessed.

For your Tuesday example, "Order the badges" now goes to Priya Raman with due 10 March, and "Book the room" goes to Tom Becker.