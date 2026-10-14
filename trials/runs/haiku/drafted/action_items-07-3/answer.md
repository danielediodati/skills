I haven't changed any code, because the change you want moves a line the charter constrains. Your example is what the code currently does: with the notes you gave, the model's line `Approve the budget | Marta Olsen | 2026-03-10` becomes `ActionItem('Approve the budget', owner=None, due=2026-03-10)`. The unit tests still pass (17 of 17). I made no paid calls.

**Why I stopped:** The charter (`evals/action_items/charter.md`) lists owner matching as constrained: an owner must be on the attendee list, otherwise it becomes `None`, and "the name list is the only source of truth for owners." The prompt in `seam.py` also tells the model to write "none" when the owner is not in the list. Showing Marta as owner means letting an unchecked name through, which is the line the charter fixes. Only you can move it, and I can't edit the charter either.

**Options, each of which moves a line:**

1. **Allow named owners outside the attendee list.** Keep the name the model gives, marked as not in the meeting. This changes the owner rule in the charter, the prompt wording, and the test `test_owner_who_was_not_in_the_meeting_is_dropped_but_item_kept`. Risk: a hallucinated name would then appear as a real owner. The charter's stated reason for the check.
2. **Keep the owner check, but add a separate field**, for example `named_in_notes`, holding the raw name for items with no attendee owner. The owner stays checked, and Tom's "unowned" reading goes away. The field is still unverified, so this also moves the line, just less far.
3. **Keep the code as it is and use a different workflow.** You or Ana can add "Marta Olsen (absent)" to the follow-up list by hand for items like this. Nothing in the code changes.

Option 1 gives you what you asked for. Option 2 is the smaller move. Tell me which you want. I'll make the change once you've updated the charter, or I can draft a proposed charter change for you to review.