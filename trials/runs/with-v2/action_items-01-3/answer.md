A first name in the owner field now resolves to the attendee who has it, if only one attendee does. All 19 tests pass, including two new ones for this.

**What was wrong:** the prompt asks the model for the owner "as written in the list", but the model sometimes writes just "Priya". The code only accepted an exact full-name match, so those items were thrown away as non-attendees. That is why it came and went with the same people.

**The change (`seam.py`):**
- `Priya` becomes `Priya Raman`, and `tom` becomes `Tom Becker`, case-insensitively.
- If two attendees share a first name, a bare `Tom` stays unassigned, as you asked. A full name such as `Tom Weiss` still resolves normally.
- Only first names are handled. A bare surname like `Raman` is still unassigned.

**One gap I left alone:** the charter says the owner should be free text as the notes give it, including non-attendees, and that the code's attendee-only filter is "not yet in code". I didn't touch that. Changing it is your decision, and it would change what every caller gets back. This fix stays inside the current attendee-only behaviour and only stops dropping names that clearly identify one attendee. The charter and prompt are unchanged.