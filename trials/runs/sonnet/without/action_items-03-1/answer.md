A task taken by two people now comes back as one item listing both of them, each by their name as it appears in the attendee list. All 22 tests pass, including new ones for shared tasks.

For your example, the shortlist task is now:

`ActionItem("Draft the supplier shortlist", ("Ana Ruiz", "Tom Becker"), 2026-03-12)`

**What changed**
- **Owner field:** `ActionItem.owner` (one name or `None`) is now `owners`, a tuple of attendee names that can be empty. This breaks anything that reads `.owner` or builds `ActionItem` by position, so downstream code needs updating.
- **Prompt:** the model is told to write shared owners separated by `;`, for example `Ana Ruiz; Tom Becker`.
- **Parsing:** it also accepts `and`, `,`, `&`, `/` and `+` as separators, in case the model ignores the instruction. Names are matched case- and spacing-insensitively and returned as the caller spelled them.
- **Unknown co-owner:** "Ana Ruiz; Marta Olsen" keeps `("Ana Ruiz",)`. If nobody in the field is an attendee, `owners` is `()`, as an unowned task was before.
- **Repeats:** the same person named twice is listed once. Duplicate-line detection now compares the task together with its full set of owners.
- **README:** updated for the new field.

One limit: a partial name like "Ana" is still not matched. That was already true for single owners, and the prompt asks for full names from the attendee list.

The changes are in `seam.py`, `test.py` and `README.md`.