The summary prompt now tells the model to leave card numbers, security codes, passwords and other private details out of the summary. I have not checked this against a real model, so the leak may still happen.

**What changed**
- `seam.py`: the prompt has a new paragraph saying the summary is read by many staff, so the model should leave out card numbers, security codes, passwords and other private details, and say what the customer needs instead.
- `test.py`: a new test checks that the prompt contains that instruction.
- The unit tests pass (12 of 12). They only check the prompt text, not what a model writes.
- `charter.md` and `AGENTS.md` are untouched.

**Why this stays inside the charter:** the charter leaves "which details the summary keeps" to the model. I added a criterion to inform that judgement, not a fixed reply or a template, so I did not move a line.

**Lines I did not move, for you to decide**
1. **The subject fallback leaks.** When the model gives no summary, the code uses the subject as the summary. A customer who types a card number or password into the subject would see it in the list, and the prompt change does nothing for that path. Fixing it means changing a charter constraint ("empty summary falls back to the subject"). A replacement such as "Customer request" or a generic label would be a fixed value, which the charter does not allow without your approval.
2. **No code-side redaction.** A regex that masks card-like numbers, CVC codes or password strings in the summary would be a constraint on summary wording. The charter says code only collapses whitespace and caps length, so this would move the line. It would be the only guarantee that does not depend on the model, so it is probably worth deciding on.

**Not done:** I have not run a real model against the two tickets from your report. That is a paid call. Before I run it, I need you to agree a spending budget for this ticket. The run is about two to four model calls on your two example tickets, plus one on a subject-only leak case if you want to test item 1.