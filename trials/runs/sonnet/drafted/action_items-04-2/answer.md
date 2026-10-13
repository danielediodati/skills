I changed the prompt so the model writes the owner's full name, but I haven't confirmed that your 3 March notes now come out with owners. That needs a real model call, and I won't spend one without your approval. The local tests pass (18, free, no model).

**Cause:** the model was writing "Tom" and "Priya" as the owner. The code only accepts a full attendee name and turns anything else into `owner=None`, so the item kept its task but lost its owner. The prompt said only "as written in the list above" and never mentioned that the notes use first names or nicknames.

**Change** (`seam.py`, the `owner` line of `PROMPT`): the prompt now tells the model that the notes often use first names or nicknames ("Tom", "Tommy", "Ana R."). It asks the model to match them to the person in the attendee list, write that person's full name, and write "none" only when the notes don't make clear who took it. I also added a test in `test.py` that the prompt carries this instruction.

**What I left alone:** the code check that rejects first names. The charter lists that as a constraint, so having code resolve "Tom" to "Tom Becker" would move that line. The model's decision about who owns an item stays with the model, and the charter is untouched.

**What this can't guarantee:**
- The model still decides who took each item. If the notes are ambiguous, or the model answers "Tom" anyway, the item still comes out unowned.
- A first name shared by two attendees is the model's call to make from the notes.

If you want it confirmed, I'd propose one call on your 3 March notes with the model you use. Please give me a spending budget for this ticket and I'll run it and show you the result against it.