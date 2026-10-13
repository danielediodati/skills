Owners are now kept when the notes name them, even if they weren't at the meeting. All 19 tests pass.

**What changed** (in `seam.py`, `test.py` and `README.md`):

- **Prompt:** the model is told the owner need not have been present. If the notes say a named person will do it, it writes that person's name as the notes do.
- **Owner check:** an owner is kept if they are an attendee (spelled as you gave it) or if their name appears in the notes as whole words. Previously anyone outside the attendee list was turned into `None`, which is what stripped Marta off the list.
- **`None` now means "nobody took it":** the model can't invent a name, because a name that isn't in the notes is dropped. So the items with no owner are the ones you need to chase.

For your 3 March meeting, "Approve the budget" comes out as `Marta Olsen`, due 2026-03-10. There are new tests for that case and for the fallback to `None` when the name isn't in the notes.

**Things to know:**

- **Absent owners:** an `ActionItem` doesn't mark them separately. To find tasks owned by someone who wasn't there, and so needs sending the list, check `item.owner not in attendees`.
- **Name spelling:** if the notes say only "Marta" and the model writes "Marta Olsen", the name isn't found and the owner falls back to `None`. The prompt asks for the name as the notes write it, so this should be rare. If your notes often use first names for absentees, I can loosen the check to accept a match on the first name alone.