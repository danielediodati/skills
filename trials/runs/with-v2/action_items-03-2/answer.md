A task taken by two people now stays one item with both attendees on it. All 20 tests pass, including new ones for this case.

**What changed**
- **`ActionItem.owner` is now `owners`, a tuple.** "Ana and Tom will draft the supplier shortlist" gives `owners=("Ana Ruiz", "Tom Becker")` on a single line, each spelled as in the attendee list. An unowned item has `owners=()`.
- **Mixed names keep the known one.** "Ana and Marta from legal" gives `("Ana Ruiz",)`.
- **The prompt asks for all co-owners, separated by `;`.** It previously asked for "the name of the person responsible", which steered the model to a single name.
- **The parser also accepts `,`, `&`, `+`, `/` and "and".** A single full name is matched first, so it is never split.
- **Duplicates compare the task plus the whole owner set**, and a name repeated within one task is listed once.

**Things to know**
- `owner` is renamed, so any caller reading `item.owner` needs to move to `item.owners`. I updated the existing tests and the README to match.
- This matches the charter, which already lists "one person or several" as free and notes that code didn't support several yet. I did not touch the charter.
- The charter's other "not yet in code" gaps are unchanged: the 10-item cap, and rejected dates being indistinguishable from no date.

The changes are in `seam.py`, `test.py` and `README.md`.