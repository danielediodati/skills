Marta's name now survives into the follow-up list, and it is marked as belonging to someone who wasn't at the meeting. All 20 tests pass (17 before, plus 3 new ones; I also rewrote the one test that enforced the old behaviour).

**The cause:** `seam.py` set `owner` to `None` for anyone who wasn't an attendee. "Marta Olsen" became an unowned item, the same as a task nobody took.

**The change:**
- `owner` is now `None` only when nobody took the item. A named person who wasn't present keeps their name, as the model wrote it.
- A new field, `owner_present`, is `False` for those people. It defaults to `True`, so existing code that builds items still works.
- The prompt now tells the model that someone named in the notes is the owner even if they weren't present.

For the 3 March meeting, the item now comes out as `Approve the budget`, owner `Marta Olsen`, due 10 March, `owner_present=False`. The "Book the room" and "Find a caterer" cases behave as before.

**Decisions for you to check:**
- **Rendering:** the follow-up list is produced outside this folder, so I haven't changed how it prints. It needs to show `owner_present=False` items as "Marta Olsen (not at the meeting)" or similar, or she still won't see that she's the one who should get the list.
- **Hallucinated owners:** I didn't add a check that a non-attendee's name appears in the notes. If the model invents a name, it will now show up as an absent owner, not as unowned. Checking the name against the notes would catch that, but it would also drop names the notes only give in a shortened form.
- **Scope:** this is a Python project with no git repo, so I didn't commit anything. The README is updated to describe the new fields.