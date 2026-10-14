I changed the prompt so the model is asked to write full attendee names. I did not add first-name matching in code, because that would move a line the charter reserves for code. The owner check is still exact, so the Tom and Priya case is not fixed yet.

**What changed**

- `seam.py`: the owner instruction now asks for the full name exactly as it appears in the attendee list, even when the notes use only a first name, a nickname or an initial. The owner rule is still a free decision, so this is a prompt change and not a moved line.
- `test.py`: one new test checks that the prompt carries that instruction.
- Unit tests: 18 pass (17 before, plus the new one). The fake model never runs the prompt, so this does not show how a real model answers.

**Where I stopped**

The charter's Constrained section says an owner must match an attendee "ignoring case and extra spaces" and that the attendee list is the constraint. Turning "Tom" into "Tom Becker" in code, or accepting "Tommy" or "Ana R.", would loosen that check, which the charter reserves for you. I have not made that change, and I have not edited the charter.

**Your decision**

- Option A: keep the prompt change and see whether a real model writes full names. This needs one paid trial, and I have not run one. Before that I would need a spending budget for this ticket from you.
- Option B: allow first-name or nickname matching in code, but only when exactly one attendee fits. This would guarantee the owner for the cases in your notes. It changes the Constrained owner rule, so it is your call and the charter would need updating.