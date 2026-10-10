A task taken by two people now stays one item with both names on it, each spelled as in the attendee list. All 20 tests pass, including three new ones for this case.

For your example, the shortlist comes back as one item with owners `("Ana Ruiz", "Tom Becker")` and due 12 March. The demo room has `("Priya Raman",)`. "Ana and Marta from legal" keeps `("Ana Ruiz",)`, since Marta isn't an attendee.

- **Data model:** `ActionItem.owner` (a string or `None`) is now `owners`, a tuple of attendee names, empty when nobody is known. Any caller that reads `.owner` needs updating. The tests and README are updated to match.
- **Prompt:** the model is told to put all names for a shared task on the same line, separated by `;`.
- **Parsing:** the owner field is also split on `,`, `&`, `/` and the word "and", since the model won't always follow the separator. Names that aren't attendees are dropped, repeats are removed, and attendee order is kept.
- **Duplicates:** the same task for the same set of owners still counts as one item.

I left the attendee name matching as it was, so an owner written as just "Ana" is not recognised. The prompt asks for names as written in the attendee list, but if the model shortens names in practice, say so and I can add first-name matching.

I did not touch `evals/action_items/charter.md`. The change fits it, since it lists the owner as free ("one person or several") and the code was catching up.

Two things the charter flags as "not yet in code" are still open: the cap of 10 items, and an unreadable due date looking the same as one never given. I left both alone since you didn't ask about them.