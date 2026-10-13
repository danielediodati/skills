# A charter the agent writes alone

Status: ready-for-agent
Blocked by: nothing

## What it produces

The rule without a charter drifted in 11 of 24 trials; the charter written with the user in 0 (`trials/results-rule-only.md`). The user wants the charter to take as little of a person as possible. This ticket measures the far end: a charter an agent writes from the seam's code, that nobody reads.

- `trials/brief-auto-charter.md`: what the writing agent is given. The charter's format and what free and constrained mean, the seam's `seam.py`, `test.py` and `README.md`. No request, no result, none of the user's charters.
- `trials/charters-auto/<seam>.md`, four of them, each written once by Sonnet 5.5 in a `--safe-mode` session and committed as written, before any trial.
- `trials/protocol-auto-charter.md`, committed before any trial runs, written the way `trials/protocol-rule-only.md` is:
  - **Condition** `auto-charter`: the agent's charter at `evals/<seam>/charter.md`, and the rule with the wording the `with-v2` trials on these requests saw, fixed in the protocol.
  - **Requests:** the eight at `requests/04.md` and `05.md`, three runs each, Sonnet 5.5: 24 trials.
  - **Judge:** Opus 5.5 with the frozen rubric, blind to the condition, against the user's charters in `trials/charters/`: the line the user drew, which neither the writing agent nor the coding agent saw.
  - **Compared with** the three arms in `trials/results-rule-only.md`, whose verdicts stand.
  - **Decision rule:** `auto-charter` drifts in 4 trials or fewer of 24: the `charter` skill drafts alone and the user's part becomes a review. In 10 or more: a person stays in the writing. In between: no decision, and the results say so.
- A line by line reading of each agent's charter against the user's: lines found, lines missing, lines put on the other side. It costs nothing and says where a person is needed.
- 24 trials under `trials/runs/sonnet/auto-charter/`, each with its verdict.
- `trials/results-auto-charter.md`: the four arms side by side, the reading of the charters, the decision the rule gives, the limits. Changes toward the user's charter are reported beside drift: a charter written from the code freezes the code as it is, so it may hold the agent back from a change the user wants.
- `openpoints.md`: what the result means for the `charter` skill.

Constraints:

- `trials/run_trials.py` and `trials/judge/run_judge.py` gain the condition without changing what they do for `without`, `with-v2` and `rule-only`.
- Nothing paid runs without a go: one spending budget for the ticket, covering the four writing sessions, the 24 trials and their verdicts. The judge's cost is not recorded; ticket 3.1 estimated $0.05 to $0.15 a verdict.
- A failed session is run again by the script; one that fails twice is reported, not dropped.

## Done when

- The brief, the four charters and the protocol are committed before the first trial.
- 24 trials have a diff, an answer, `session.json` and a verdict, committed.
- `trials/results-auto-charter.md` gives the decision as the protocol's rule gives it, and the user has read it.
