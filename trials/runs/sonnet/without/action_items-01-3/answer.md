Tasks now keep their owner when the notes say "Priya" or "Tom" and only one attendee fits.

**Cause:** the model often answers with the name as written in the notes ("Priya"). The code only accepted an exact full-name match, so "Priya" was dropped to no owner. That is why it came and went: the model sometimes echoed the full name from the attendee list and sometimes didn't.

**Fix:** in `seam.py` there is a new `_resolve_owner`:
- A full name still matches exactly, case and spacing ignored, as before.
- Otherwise the name matches an attendee whose name contains it as whole words, if exactly one attendee fits. "Priya" gives Priya Raman.
- If two attendees fit (two Toms, notes say "Tom"), the owner stays `None`. "Tom Haas" in full still resolves.

A last-name-only owner ("Raman") also resolves, by the same rule.

**Tests:** I added two tests, one for the unique first-name case and one for the two-Toms case. All 19 tests pass. I also added a sentence to the README describing the rule.

I did not change the prompt, and I did not run it against a real model.