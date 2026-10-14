The summary prompt now tells the model to leave card numbers, security codes, passwords and other typed secrets out of the one-line summary. I haven't yet confirmed that the model obeys it, and I haven't made the stronger code-side fix, because that would move a line in the charter.

**What changed**
- `seam.py`: the prompt's summary line now reads "one sentence saying what the customer needs. The summary is shown to many people, so leave out card numbers, security codes, passwords and any other secret the customer typed." This is a criterion for the model's judgement, which the charter allows. The summary wording stays free.
- `test.py`: one new test checks that this instruction reaches the model.
- `python -m unittest`: all 12 tests pass. These run with a fake model, so they only show the instruction is sent. They don't show the model follows it.

**What I didn't do**
- I made no paid model calls. I haven't run the two example tickets through the real model, so I don't know whether the instruction holds.
- I didn't change the charter, as AGENTS.md requires. It still describes the summary as only length-capped and whitespace-collapsed. You may want to add the new criterion there.

**The line I stopped short of**
A code check would close the gap the prompt can't. A pattern for card-like digit runs (13–19 digits, with spaces or dashes) could be replaced with a fixed token before the summary is stored. That would take part of the summary wording out of the model's hands, which moves the line, so I left it for you. Passwords like `Tulip-Harbour-92` can't be caught by a pattern at all. For those, only the model's judgement or a human check helps.

**Decisions for you**
1. Approve a code-side redaction for card-number patterns? It would catch the card case deterministically, but not the password case.
2. Approve a small paid check of the new prompt against the card and password tickets? If yes, please agree a budget for the whole ticket first. I'd start with the cheapest model.
3. Should I record the new criterion in the charter? Only you can change it.