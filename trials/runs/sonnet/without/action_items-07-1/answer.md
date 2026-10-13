Tasks owned by someone who wasn't in the meeting now keep their owner. All 18 tests pass, including a new one built on your 3 March notes.

**Cause:** `extract_action_items` threw away any owner who wasn't in the attendee list and set `owner` to `None`. That made "Marta will approve the budget" look the same as a task nobody took.

**Changes**
- **Prompt (`seam.py`):** the model is now told to give the full name as written in the notes when a task belongs to someone who wasn't present. It writes `none` only when the notes name nobody.
- **Owner handling (`seam.py`):** attendees come back spelled as you gave them. A non-attendee is kept, with a new `ActionItem.owner_absent=True` flag, if the notes actually mention that name.
- **Unowned tasks:** `owner is None` now means the notes name nobody, so those are the ones to chase. For 3 March the item comes out as `ActionItem("Approve the budget", "Marta Olsen", 2026-03-10, owner_absent=True)`.
- **Guard against invented owners:** a name that isn't in the notes at all (a model hallucination) still becomes `None`. The cost is that if the notes say only "Marta" and the model writes "Marta Olsen", the item falls back to unowned.
- **Tests and README:** I renamed the old "dropped owner" test to say it applies when the name isn't in the notes, added the new test, and updated the README rule.

**Not covered:** your follow-up list is built by whatever consumes `ActionItem`. It should show `owner` and use `owner_absent` to include absent owners, such as Marta, in the send-round. That code isn't in this directory, so I didn't touch it.