Owners written as a first name now resolve to the matching attendee, and a name shared by two attendees stays unassigned. All 19 tests pass, including two new ones for this.

**Cause:** the model was told to write the owner "as written in the list above", but it often echoes the notes and answers "Priya". The code only accepted an exact full-name match, so "Priya" was dropped to `None`. That also explains why it only happened in some meetings.

**Fix (`seam.py`):** a new `_resolve_owner` tries, in order:
1. The full name, ignoring case and spacing, as before.
2. A single name part (first or last), if exactly one attendee has it. "Priya" in your example becomes Priya Raman, and "Tom" becomes Tom Becker.
3. Otherwise `None`. With Tom Becker and Tom Hale both present, a bare "Tom" is left unassigned, and "Tom Hale" still resolves.

**Tests (`test.py`):** one for first-name resolution and one for the two-Toms case.

- Last names resolve the same way ("Raman" alone works), since I used any name part. If you want first names only, say so and I'll narrow it.
- The README's rule that an owner is kept only if it is an attendee's name still holds. I didn't edit it, so it doesn't yet mention the first-name matching.
- Matching still depends on the model putting the right name in the owner field. If notes say "Priya" and the model answers with a different person, nothing here catches that.