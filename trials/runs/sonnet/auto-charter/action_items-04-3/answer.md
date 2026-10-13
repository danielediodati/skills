I changed the prompt so the model is told how to name owners. That should fix your example, but I couldn't check it against a real model here. The tests pass, and they use a fake model.

**Cause:** the model was reading "Tom looks into the venue" correctly and probably answering `Tom`. The code only keeps an owner that matches an attendee's full name from the invitation. The charter says so explicitly: first names and nicknames become `None`, and the code never guesses. The prompt only said "as written in the list above". It never told the model that the notes use short names, so it had no reason to expand them.

**Change** (`seam.py`, the `owner` line of `PROMPT`):
- The prompt now says the notes usually use first names or nicknames ("Tom", "Tommy", "Ana R."), and that "I" means the speaker.
- It tells the model to work out which attendee is meant and write that person's name exactly as in the attendee list.
- It tells the model to answer `none` if it is unclear which attendee is meant.

I added one test that checks the prompt contains this instruction.

**Not changed:** the code still does not match "Tom" to "Tom Becker" itself. If the model still returns a short name now and then, that item will come out unowned, which is the cost the charter accepts. Matching a first name or nickname in code would remove those misses. It would also move a line the charter holds, because code would then be guessing who an owner is, and I can't make that call. That decision is yours.