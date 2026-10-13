I changed the prompt in `seam.py` so the model writes "Tom Becker" and "Priya Raman" as owners when the notes say "Tom" and "Priya". I did not run it against a real model, so the actual effect on your notes is untested. The 18 unit tests pass, but they use a fake model.

**Cause:** the model was asked for the owner "as written in the list", and it often answered with the bare first name instead. Code only accepts an owner that matches an attendee's full name exactly, so "Tom" became `None` and the task landed in the shared backlog with no owner.

**Fix:**
- **Prompt:** the owner instruction now says notes often use first names, nicknames or short forms ("Tom", "Tommy", "Ana R."). When it is clear which attendee that is, the model must write that person's full name from the list.
- **Test:** `test.py` has a new test that the prompt carries this instruction.
- **Left alone:** your charter keeps the exact owner match in code, because the tracker needs owners it can check. I did not loosen that, and the model still decides who took each task, including "none" when nobody did.

**What this won't catch:**
- If the model still answers with a short form, the owner is still dropped to `None` and the item stays.
- If two attendees share a first name and the notes don't say which, the model should answer "none". That is the intended behaviour.