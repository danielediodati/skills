A task taken by two people now comes back as one item listing both owners, each spelled as in the attendee list. All 19 tests pass.

**What changed**
- **`seam.py`**
  - `ActionItem.owner: Optional[str]` is now `owners: Tuple[str, ...]`.
  - `_parse_owners` splits the model's owner field on `;`, `,`, `&`, `/` and the word "and". It keeps only attendees, each in the caller's spelling, with no duplicates.
  - In "Ana and Marta from legal", Marta isn't an attendee, so the item keeps `("Ana Ruiz",)`.
  - If nobody is a known attendee, `owners` is `()`, so the item stays in the list as unassigned.
  - A name that itself contains a separator is matched whole first, so it isn't split.
- **Prompt:** the owner line now says that if several people took it together, the model gives each name separated by `;`. This only tells the model how to write several owners; it doesn't tell it who they are.
- **Tests and README:** existing tests were updated for `owners`, and I added tests for shared tasks (three separator styles) and for a shared task with a non-attendee.

**Charter:** I didn't touch it. It already lists "one person or several, attendee or not" as the model's free decision about owners and notes that code didn't yet support it. Keeping attendee names only stays as it was.

**Breaking change:** `item.owner` is gone, so any caller reading it needs to switch to `item.owners`. For a single-owner task the value is now a one-element tuple. If you'd rather keep `owner` as a string (for example `"Ana Ruiz, Tom Becker"`), say so and I'll change it.

**Still open:** the charter also marks two other gaps as "not yet in code": the cap of 10 items and rejected due dates becoming `None`, which looks the same as no date given. I left both alone since they weren't part of this request.