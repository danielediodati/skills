# A charter the agent writes by its own rules

Status: ready-for-agent
Blocked by: nothing

## What it produces

A charter written from the code as it is holds the line and freezes the code, defects included (`trials/results-auto-charter.md`). The user decided how the `charter` skill should work: the agent writes the charter alone, reasons for itself about how work is split between model and code and writes its own rules, marks a line that differs from what the code does, and asks only on a serious doubt, otherwise nothing. No rule drawn from the user's charters goes into the brief: it would test nothing. Before the larger run is built on it, the user wants it tried on the same 24 trials.

- `trials/brief-practice-charter.md`: the brief that asks the agent for its own rules first, with the `Not yet in code` mark and the `Assumed.` mark.
- `trials/charters-practice/<seam>.md`, four of them, each written once by Sonnet 5.5 and committed as written, with the rules the agent gave itself beside it.
- `trials/protocol-practice-charter.md`, committed before any trial: the condition `practice-charter`, the same eight requests three times each, Opus as judge against the user's charters, and a rule that decides on two counts, drift and changes toward the user's charter.
- A line by line reading of the four charters against the user's, with the marks counted: defects found, and things marked as defects that the user keeps.
- 24 trials under `trials/runs/sonnet/practice-charter/`, each with its verdict.
- `trials/results-practice-charter.md`: the five arms side by side, the reading, the decision, the limits.
- `openpoints.md`: what the result means for the `charter` skill and for the brief session 4 uses.

Constraints:

- The scripts gain the condition without changing what they do for the others.
- Nothing paid runs without a go: one spending budget for the ticket. Ticket 3.2 spent $2.07 on the same shape of work, its 24 verdicts not counted.
- No calibration round with the user: the protocol says what stands in its place.

## Done when

- The brief, the four charters and the protocol are committed before the first trial.
- 24 trials have a diff, an answer, `session.json` and a verdict, committed.
- `trials/results-practice-charter.md` gives the decision as the protocol's rule gives it, and the user has read it.
