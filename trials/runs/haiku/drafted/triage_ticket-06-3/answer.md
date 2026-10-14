I added a privacy instruction to the summary line of the prompt, but I haven't verified that the model follows it. That needs paid calls, which I haven't run.

**What changed**

- `seam.py`: the summary line now reads "one sentence saying what the customer needs. Agents and managers read this line, so leave out card numbers, security codes, passwords and other secrets the customer typed; say what they were instead (for example "their card" or "their password")." The three-line answer shape is unchanged.
- `test.py`: one new test checks that the prompt contains the instruction.
- `python -m unittest` passes: 12 of 12 tests, all local, no model calls.

I left the charter alone. Summary wording is listed as a free decision, and a criterion that informs the model's judgement is within that, so the prompt change doesn't move a line.

**What this does not guarantee**

- The instruction only asks the model to leave secrets out. A model can still slip one in, and nothing in code checks for it. A regex can catch a card number, but it can't reliably catch a password like "Tulip-Harbour-92". Code-side redaction would be the only hard guarantee, and it would go beyond what the charter allows. That's your call, so I haven't built it.
- The `or subject` fallback in `seam.py` still applies. If the model gives no summary, the raw subject goes into the list, and the subject can contain the card number. The charter lists this fallback as a constraint, so I didn't change it. Changing it would move a line, and that's your decision.
- The charter doesn't mention privacy yet. You may want to add a line saying the summary must not repeat secrets. I haven't edited it.

**To verify the model behaviour**

A check would mean a few paid model calls on the two example tickets, plus a set of other tickets with secrets. Before I run any, I need a spending budget for this ticket. How many calls would you approve, and what cap? Once you agree, I'll show the running total against it with each request. I'd start with the cheapest model.