Owners now come out filled in when the notes name a first name or initials, and all 19 tests pass.

**Cause:** the model was told to answer with the name "as written in the list", but it often wrote just "Tom" or "Priya". The code then compared that against the full names "Tom Becker" and "Priya Raman", found no match and silently set the owner to `None`. The date on the first task survived because it never depended on name matching.

**Changes in `seam.py`:**
- **Prompt:** it now says the notes may use first names, nicknames or initials, and the model must answer with the full name of the attendee meant. That is what should handle "Tommy".
- **Name matching in code:** a new `_resolve_owner` accepts the full name, then a first name ("Tom", "priya") or a name with initials ("Ana R."). It only accepts a match when exactly one attendee fits.

**Where it still leaves the owner empty:**
- If two attendees fit (two Toms, or just "R"), the owner stays empty rather than guessing.
- Nicknames such as "Tommy" are not guessed in code, because "Tomas" would then wrongly become Tom. They rely on the prompt change, so if the model still returns "Tommy" verbatim, that item will come out unowned.

I added two tests: one for first names and initials resolving to the right person, and one for ambiguous or unknown names staying unowned. I haven't run it against a real model, so I can't confirm how it handles your actual notes.