I made half of this. The list can now tell "someone outside the room has it" from "nobody took it", but it still can't show Marta's name. Showing her name would move a line in the charter that only you can change.

**What changed (no paid calls, 19 local tests pass)**
- **`ActionItem.owner_elsewhere`:** this new field is `True` when the notes name someone who wasn't at the meeting. `owner` stays `None`. Your 3 March item comes out as `("Approve the budget", None, 2026-03-10, owner_elsewhere=True)`. A task nobody took has `owner_elsewhere=False`, so those are the ones to chase.
- **Prompt:** it now tells the model to write the absentee's name as the notes give it. Before, it said to use only names from the attendee list, so the model was likely to write "none" for Marta.
- **Guard against false flags:** a bare first name of an attendee, such as "Tom", is not flagged as an absentee.
- **Tests and README:** I updated both to match.

**The line I didn't cross**
The charter's constrained section says an owner must be an attendee, because an absent person must not be assigned work. A non-match becomes `owner=None`. Putting "Marta Olsen" in the owner slot, or in a parallel name field, would assign work to a name that code can't verify, and it's the same move under another label.

**What moving it would buy**
- The list would show "Approve the budget – Marta Olsen – 10 March".
- You could address the follow-up to Marta, who currently gets nothing.
- The cost is that a name the model invents or misreads would show up on the list as an owner, and no check would catch it.

**Your options**
1. Keep it as is. The flag says "someone has it" but you still reread the notes to see who.
2. Change the charter to allow a model-named outsider as a separate, clearly unverified field, for example `named_owner`, without making it a real owner. If you want that, you'd edit the charter, and then I'd implement it.

I also touched one thing you didn't ask for: the prompt's owner wording. It informs the model's judgement and doesn't dictate the answer, so I read it as within the charter's free zone. Say if you'd rather I back it out.