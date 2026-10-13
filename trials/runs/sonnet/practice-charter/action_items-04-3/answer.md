I changed the prompt in `seam.py` so the model names the owner in full, as listed. I haven't run it against a real model, so I can't yet confirm that "Tom looks into the venue" now comes out owned by Tom Becker. The existing tests pass, and they use a fake model, so they don't exercise this.

**Cause:** the prompt only said "as written in the list above". The model often wrote the owner the way the notes did ("Tom", "Priya"). The code accepts only an exact attendee name, so those items became `None`. The first item came out right because the model happened to write "Ana Ruiz".

**Fix:** the owner instruction now tells the model:
- to copy the full name from the attendee list;
- that the notes may use first names, nicknames or initials ("Tommy", "Ana R."), and it should work out which attendee is meant and write that attendee's listed name;
- to answer "none" only when the notes don't make clear who took the item.

**Not changed:** the code's check that the owner is an attendee. Adding fuzzy matching there would loosen a constrained decision. The charter says a bare first name becoming `None` is fixed in the prompt, which is where I made the change.

If an item still comes out unowned, the model has answered "none" or a name that isn't in the list, so the next step would be to look at the model's raw answer for that note.