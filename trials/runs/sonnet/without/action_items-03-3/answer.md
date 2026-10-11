A shared task now stays one item and carries every owner who was in the meeting. All 20 tests pass, including three new ones for this case.

**What changed in `seam.py`**
- **Prompt:** the model is told to write shared owners separated by `;`, e.g. `Ana Ruiz; Tom Becker`.
- **Parsing:** the owner field is also split on `,`, `&`, `/` and `and`, since models don't always follow the format. Each part is matched against the attendee list, so names come back spelled as the caller gave them, and a name repeated within the field is listed once.
- **Unknown names:** `Ana Ruiz; Marta from legal` keeps Ana Ruiz and drops Marta. If nobody known is left, the item is unowned, as before.
- **`ActionItem`:** it keeps `owner` (the first owner) and gains `co_owners` (the rest) and an `owners` property returning all of them. Existing callers and the existing `ActionItem(task, owner, due)` constructor keep working.
- **Dedupe:** de-duplication now compares the task plus the full set of owners, so "Ana + Tom" and "Ana alone" on the same task are distinct, as they were before for single owners.

**Other changes**
- `README.md` and `test.py` are updated.
- One limitation: if the model writes the free-text phrase "Ana and Marta from legal" as the owner field, Ana is not recognised. The prompt asks for attendee names, so this should be rare.

Consumers that show or export the owner column need to switch to `owners` to display both names. Anything still reading only `owner` will show just the first person.