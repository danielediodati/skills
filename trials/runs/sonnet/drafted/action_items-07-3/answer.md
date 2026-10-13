I haven't changed anything, because fixing this means moving a line in the charter that only you can move.

**The line:** `evals/action_items/charter.md`, under Constrained, "Owner must be an attendee". `extract_action_items` in `seam.py` maps any owner who isn't in the attendee list to `None` and keeps the item. In your 3 March meeting the model can correctly read "Marta Olsen", and the code then discards her name, so the item comes out as "Approve the budget, due 10 March, no owner". That is indistinguishable from a task that was left hanging.

Two things are tangled in that one line:
- The code can't tell "nobody took this" from "someone took this who wasn't present". Both end up as `owner=None`.
- The prompt asks for the owner "as written in the list above", so the model has no place to put a non-attendee's name.

**What moving the line would buy:** items owned by absent people would show their name, and truly unowned items would be the only ones left with no owner. That is the distinction you need to chase the right tasks and to get the list to Marta.

**What it would cost:** the charter keeps this check so that invented names stay out of a tracker. If it loosens, a wrong name from the model (a misread nickname, a person mentioned only in passing) would reach the list with nothing to catch it.

**Options for you to decide:**
1. **Carry the named owner separately (my recommendation).** `owner` stays checked against attendees. A new field, e.g. `named_owner`, holds the name the model read when it isn't an attendee. The list shows "Approve the budget, Marta Olsen (not present), 10 March". This changes the answer format and the `ActionItem` shape, so it needs your approval and a charter update from you.
2. **Allow non-attendees as owners.** Pass the caller an optional list of known people beyond the attendees (e.g. the team directory), and check against that. The invented-name protection stays, but someone has to keep the directory current.
3. **Leave the code alone.** Task wording is free, so the model could be told to write "Approve the budget (Marta Olsen)". I'd advise against it: it would route around the check rather than satisfy it, and a tracker would still see no owner.

Tell me which one you want and I'll implement it, adding tests that cover the 3 March case. I haven't run anything paid, and nothing is needed until you choose. Before the first paid call I'd ask you to agree a budget for the ticket.