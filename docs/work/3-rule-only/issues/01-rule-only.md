# The rule alone, without a charter

Status: ready-for-agent
Blocked by: nothing

## What it produces

Writing a charter for every seam is heavy. No trial has ever run the rule in `AGENTS.md` without a charter: the conditions so far are `without` (neither) and `with`, `with-v2` (both). This ticket measures the missing arm and decides whether a charter per seam stays mandatory.

- `trials/protocol-rule-only.md`, committed before any trial runs, written the way `trials/protocol-silent-drift.md` is:
  - **Condition** `rule-only`: no charter in the trial's directory, and the rule reworded for an agent that has none, so that it reads the line from the code. The wording is fixed in the protocol.
  - **Requests:** the eight at `requests/04.md` and `05.md`, three runs each, Sonnet 5.5: 24 trials.
  - **Judge:** Opus 5.5 with the rubric, blind to the condition. The rubric judges drift against the charter's lines, which the agent in this condition never saw: the protocol says so.
  - **Compared with** the 24 `without` and the 24 `with-v2` trials that exist on the same requests (14 and 2 drifted, `trials/results-silent-drift.md`). The three arms are compared under one rubric: if the existing verdicts were written with an earlier one, those trials are judged again (ticket 4.3 does the same; either may reuse the other's verdicts).
  - **Decision rule:** `rule-only` drifts in 4 trials or fewer of 24: a charter per seam becomes optional. In 10 or more: the charter stays, cut down to its free and constrained lines, the draft written by the agent from the code. In between: no decision, and the results say so.
- 24 trials under `trials/runs/sonnet/rule-only/`, each with its verdict.
- `trials/results-rule-only.md`: the three arms side by side with Wilson 95% intervals and per request, the decision the rule gives, the limits.
- `openpoints.md`: what the result means for the `charter` skill, for the rule `setup` writes and for decision 7 of `CONTEXT.md`.

Constraints:

- `trials/run_trials.py` and `trials/judge/run_judge.py` gain the condition without changing what they do for `without` and `with-v2`: session 4 runs them on those two under its own protocol.
- The sessions spend the user's usage: agree one spending budget first (an agent session has cost about $0.10 to $0.13; the judge's cost is not recorded), say that 24 are about to run and wait for a go.
- A failed session is run again by the script; one that fails twice is reported, not dropped.

## Done when

- The protocol is committed before the first trial.
- 24 trials have a diff, an answer, `session.json` and a verdict, committed.
- `trials/results-rule-only.md` gives the decision as the protocol's rule gives it, and the user has read it.
