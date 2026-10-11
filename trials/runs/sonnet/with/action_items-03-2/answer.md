A task shared by two people now comes back as one item with both owners, each spelled as in the attendee list. The tests pass.

For your example, the shortlist item comes back as `ActionItem("Draft the supplier shortlist", ("Ana Ruiz", "Tom Becker"), date(2026, 3, 12))`.

- **Owner field:** `ActionItem.owner` is now `owners`, a tuple of attendee names (empty when nobody is known), so any caller reading `.owner` needs updating.
- **Prompt:** the model is asked to give several owners separated by `;` on the same line. The parser also accepts "and", `,`, `&` and `/`, case- and spacing-insensitively.
- **Unknown co-owner:** "Ana and Marta from legal" gives `("Ana Ruiz",)`. Names that aren't attendees are dropped and the known ones are kept.
- **Duplicates:** the same task with the same set of owners is listed once, whatever order the names come in.

I added tests for these cases and updated the README and `evals/action_items/charter.md`. This didn't move the charter's line, since "one person or several" was already listed as the model's free decision. I only reworded the "not yet in code" note to say several attendees are now kept and non-attendees are still dropped.