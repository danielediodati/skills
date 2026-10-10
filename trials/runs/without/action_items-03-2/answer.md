A task taken by two people now stays one line with both owners on it, each spelled as in the attendee list. All 22 tests pass, including the new ones.

For your example, "Draft the supplier shortlist" comes back as a single item with `owners=("Ana Ruiz", "Tom Becker")`.

**Changes in `seam.py`**
- **New field:** `ActionItem` gains `owners: Tuple[str, ...]`, listing everyone who took the task in the order named.
- **`owner` unchanged:** it still exists and holds the first owner, or `None`, so code and tests that read it keep working. Passing only `owner` also fills `owners`.
- **Prompt:** the model is now told to write all names separated by semicolons on the same line.
- **Parsing:** the owner field is also split on `and`, `,`, `&`, `/` and `+`, because the model may not follow the semicolon instruction. A field that is exactly one attendee's name is matched whole first, so it is never split.
- **Unknown co-owner:** "Ana and Marta from legal" gives `owners=("Ana Ruiz",)`. If no one in the field is an attendee, `owners` is empty and `owner` is `None`, as before.
- **Duplicates:** a repeated task is now identified by its task text plus the full set of owners.

**Tests and README**
- `test.py` has a new `SharedOwnerTest` covering two owners, the other separators, an unknown co-owner, only unknown owners, and a repeated name.
- `README.md` documents `owners`.

**One thing to check:** if your follow-up email or tracker export reads `owner`, it will still show only the first person. It needs to read `owners` to show both.