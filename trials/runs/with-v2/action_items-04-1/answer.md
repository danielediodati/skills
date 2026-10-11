Items should now come out with their owner when the notes name someone, including by first name or nickname. All 18 tests pass, but they use a fake model, so I haven't seen the real model resolve "Tom" to "Tom Becker" on your 3 March notes.

**Cause:** the prompt asked for the owner's name "as written in the list" and said nothing about first names or nicknames. The model often wrote "Tom" or "Priya", which didn't match an attendee exactly, so the code set the owner to `None`.

**Changes**
- **Prompt (`seam.py`):** the model is now told that notes may use a first name, nickname or initials ("Tom", "Tommy", "Ana R."), and to write the full listed name when that clearly means one of the people present. The decision stays with the model; the prompt only describes what to look for.
- **Owner handling (`seam.py`):** an owner is no longer dropped just because it isn't an exact attendee name.
  - An attendee match is still returned spelled as you gave it.
  - Any other name is kept as the model wrote it, which is what the charter lists as free ("attendee or not").
  - "none" and similar still give no owner.
- **Tests and README:** I replaced the test that asserted non-attendees are dropped, added one for the prompt wording, and updated the README line.

**Limit:** the code does no fuzzy matching of its own. If the model returns "Tom", that is kept as "Tom" rather than expanded, because deciding who the owner is stays with the model under the charter.

I left the charter untouched. Two other items it marks as "not yet in code" are still open: the 10-item cap and rejected due dates looking like missing ones. I can take those on if you want.