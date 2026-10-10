A shared task now comes back as one item with every attendee on it, and all 20 tests pass.

Your example gives one line, `Draft the supplier shortlist`, owned by Ana Ruiz and Tom Becker, due 12 March. "Ana and Marta from legal" keeps Ana Ruiz and drops Marta.

## What changed
- **`ActionItem.owner` is now `owners`**, a tuple of attendee names spelled as in the attendee list. It is empty when nobody known took the task. Anything that reads `.owner` will need to switch to `.owners`.
- **Prompt:** the model is told to write several names separated by `;` when people took a task together. The model still decides who the owners are.
- **Parsing:** the owner field is split on `;`, `,`, `&` and `and`, so `Ana Ruiz and Tom Becker` also works if the model ignores the separator instruction.
- **Dedup:** the same task with the same set of owners is listed once, regardless of the order the names come in.
- **Docs and tests:** the README and tests are updated, with new tests for the shared case, the non-attendee case and dedup order.

## Charter
`evals/action_items/charter.md` already listed "one person or several" as the model's decision, so this brings the code in line and doesn't move the line. I edited two lines:
- The owner entry now says the code keeps every named attendee and drops non-attendees.
- The dedup rule now reads "same owners".

The non-attendee dropping is still marked "not yet in code".

## Left alone
- The charter also says the 10-item cap and the due-date-rejection distinction are "not yet in code". Those are separate from this request and I didn't touch them.
- There is no git repo here, so nothing was committed.