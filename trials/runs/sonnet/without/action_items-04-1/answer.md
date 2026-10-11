Tasks now keep their owner when the notes name the person by first name, nickname or initials. All 19 tests pass, including two new ones for this.

**Cause:** the model was told to write the owner "as written in the list above", but it often wrote what the notes said ("Tom", "Priya"). The code only accepted an exact full-name match, so anything else was silently turned into "no owner" while the task itself was kept. That is why your venue and badges tasks came back unowned.

**Changes in `seam.py`:**
- **Name matching:** the owner is now matched to an attendee by full name, first name alone, last name alone, a nickname that shares its start with the real name ("Tommy" → Tom Becker, at least 3 letters), or initials ("Ana R." → Ana Ruiz).
- **Ambiguity:** if a name fits more than one attendee, or none, the owner stays empty rather than guessing. Two Toms in the meeting means a bare "Tom" is not assigned.
- **Returned spelling:** owners come back spelled as you gave them in the attendee list ("Tom Becker").
- **Prompt:** it now asks the model for the full attendee name even when the notes use a first name or nickname.
- **Tests and README:** I added tests for these cases and updated the README rule.

**Limits:**
- Nicknames that don't start with the real name ("Bob" for "Robert", "Liz" for "Elizabeth") won't match. They stay unowned instead of being guessed.
- I tested with a stubbed model, so I haven't seen what your real model returns for your 3 March notes.