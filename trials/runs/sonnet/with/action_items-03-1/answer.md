A task taken by several people now comes back as one item carrying all of its known owners. All 19 tests pass, including new ones for the shared-task cases.

For your example, the shortlist is one item with owners `("Ana Ruiz", "Tom Becker")`, each spelled as in the attendee list. If one of the names isn't an attendee, as in "Ana and Marta from legal", the known owner is kept and the unknown one is dropped.

- **Prompt:** it now tells the model to separate co-owners with `;`.
- **Parsing:** the owner field is split on `;`, `,`, `&` and `and`, each part is matched to the attendee list, and duplicates are removed. Matching is on full attendee names, so the model still has to write "Ana Ruiz", not "Ana".
- **Dedup:** the same task is now treated as a duplicate when it has the same set of owners.

**API change:** `ActionItem.owner` (a string or `None`) is now `owners`, a tuple that is empty when nobody took the task. This breaks callers that read `.owner`. I updated the existing tests and the README for it.

**Charter:** `evals/action_items/charter.md` already lists "one person or several" as free for the model, so I only replaced the "not yet in code" note on owners with what the code now does. Nothing moved between free and constrained.

The edits are in `seam.py`, `test.py`, `README.md` and the charter.