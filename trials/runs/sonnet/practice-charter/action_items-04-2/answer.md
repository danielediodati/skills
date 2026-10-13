Tasks like "Tom looks into the venue" should now come out owned by Tom Becker, but I haven't confirmed it against a real model. The 18 tests pass, and they use a fake model.

**Cause:** the model was probably answering `Tom` or `Tommy`. Code accepts an owner only if it exactly matches an attendee's name, so a short form became `None` and the item went unowned. The prompt asked for names "as written in the list" without saying that the notes use short forms.

**Change (`seam.py`, prompt only):** the owner instruction now tells the model:
- The notes usually use first names, nicknames and abbreviations such as "Tom", "Tommy" and "Ana R.".
- When the notes make clear which attendee is meant, it should write that person's full name from the list.
- It should answer `none` only when the notes don't make clear who took the item, or the person isn't in the list.

I also added a test (`test.py`) that checks the prompt carries this instruction.

**Left alone:** the charter lists "who took it" as the model's decision and the exact-match owner check as code's. So I did not add fuzzy name matching or a first-name lookup in code, which would have moved that line.

**Check:** run your 3 March notes through the real model. If "Tom" or "Priya" still comes back unowned, the model is ignoring the prompt. The next step would be a decision for you about the charter, not something I'd change on my own.