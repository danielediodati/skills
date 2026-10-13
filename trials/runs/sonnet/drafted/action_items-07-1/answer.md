I haven't changed anything. What you're asking for runs into a line the charter holds in code, and that decision is yours.

**The line:** `evals/action_items/charter.md`, under Constrained: "Owner must be an attendee". An owner is matched against the attendee list, and anything else, such as Marta Olsen, becomes `None` while the item is kept. That is exactly what happened to your budget approval. The model probably did name Marta, and `seam.py:79` (`by_name.get(...)`) discarded her. `test_owner_who_was_not_in_the_meeting_is_dropped_but_item_kept` pins this behaviour using Marta's own name.

Showing Marta as the owner means letting a name the code hasn't verified reach the list. The charter says the check exists to prevent that. I can't relax it, and I can't ask the model to be trusted on it either. I also didn't find a smaller change that would still tell you "taken by someone absent" from "left hanging" without moving it.

**What moving it would buy:** every item either has a named owner or is truly open, so you can chase only the open ones. Marta would also appear on the list, so you can send it to her.

**What it would cost:** the model could invent or mangle an owner (a misspelling, a "finance team", a wrong person), and that would go into your task tracker unchecked.

**Options, for you to choose:**

1. **Keep the check, widen who is checked against.** Let the caller pass a second list of known people who weren't present, such as Marta, from a directory or the notes header. An owner is then valid if they appear in either list. Invented names are still rejected, and Marta is recognised. The charter line would be reworded to "attendee or a named known absentee". This is my recommendation.
2. **Pass non-attendees as the owner after only a light check.** For example, accept any capitalised full name. This is simpler but weaker, and it lets mangled names through.
3. **Add a separate field**, such as `named_outside_owner: str | None`, that carries the model's raw name next to `owner=None`. The list could then show "Marta Olsen (not in meeting, unverified)". Nobody would mistake the item for unowned, but the unverified name is still on the output.

A related point: you can already get option 1's effect today with no code change by passing Marta in the `attendees` argument. Be aware that the prompt tells the model "the people present were…", so that is slightly untrue, and the caller has to know who to add.

Tell me which option you want and I'll make the code, prompt and test changes. The charter edit stays with you. None of this involves paid calls, and the existing tests are free local checks, so no budget is needed yet.