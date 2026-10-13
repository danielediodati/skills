Tasks owned by someone who wasn't at the meeting now keep their owner. Marta's budget approval comes out as hers, flagged as absent, and `owner is None` now means only that nobody took the task. All 18 tests pass, including a new one for the Marta case.

**What was wrong:** `extract_action_items` in `seam.py` dropped any owner who wasn't on the attendee list. The item stayed but its owner became `None`, so "Marta approves the budget" and "nobody took this" looked identical.

**What changed:**
- **Prompt:** the model is told that if the notes give a task to someone who wasn't present, it should name that person as written in the notes, not say "none".
- **Owner kept when absent:** an owner who wasn't at the meeting is now kept if the notes actually mention that name. This stops the model inventing an owner.
- **New field:** `ActionItem` has `owner_attended`, which is `False` when the owner was named in the notes but wasn't in the meeting. It defaults to `True`, so existing callers are unaffected.
- **Fallback:** an owner who is neither an attendee nor in the notes still becomes `None`, and the item is kept.
- **Docs and tests:** the README and tests are updated to match.

For your 3 March meeting the item now comes out as:

```
ActionItem(task="Approve the budget", owner="Marta Olsen", due=date(2026, 3, 10), owner_attended=False)
```

Two things to know:
- The name is returned as the model wrote it, since there's no canonical spelling for non-attendees. Matching against the notes is case- and spacing-insensitive, and the full name has to appear there.
- This changes the extraction only. When you build the follow-up list, you'll want to use `owner_attended=False` to send it to the absent owner and to mark those lines as already owned.