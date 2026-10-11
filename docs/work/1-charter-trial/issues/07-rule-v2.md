# Close the back door in the rule

Status: ready-for-agent
Blocked by: nothing

## Why

With the charter, 21 of 36 agents edited the charter itself, rewriting the line they had just moved so that the move reads as allowed. The rule's last bullet invites it: "They decide it; the charter changes in the same commit." In a session with nobody to ask, the agent reads that as leave to change the charter alone.

## What it produces

- The `## Stochastic seams` section in `a4a/skills/setup/SKILL.md`, rewritten so that only the user changes a charter: the agent proposes a change and stops, it never edits the charter itself.
- `trials/runs/with-v2/`: the 36 trials with the charter, run again with the new rule; the same judge and rubric.
- A section in `trials/results.md` comparing v1 and v2: drift, stops, flags, and how many agents edited the charter.

## 2026-10-11: where it stands

- The rule v2 ships in `setup/SKILL.md`; the 36 trials ran in `trials/runs/with-v2/` and were judged: 18 drifted (v1: 19), 0 charter edits (v1: 21).
- The user then moved the rubric's line on the prompt: a general rule the model still applies by reading each input (a requirement the user stated, a definition of a phrase) is a criterion, not drift. The trials that changed the prompt are judged again in all three conditions: done for `without` (11) and `with` (13); the 16 of `with-v2` failed when usage ran out and still hold their verdicts under the old rubric. To finish:

  ```
  uv run --no-project python trials/judge/run_judge.py with-v2 --redo --only action_items-02-1 action_items-02-2 action_items-02-3 action_items-03-1 action_items-03-2 action_items-03-3 extract_invoice-02-1 extract_invoice-02-2 extract_invoice-02-3 recommend_products-01-1 recommend_products-01-2 recommend_products-03-1 recommend_products-03-3 triage_ticket-01-1 triage_ticket-01-2 triage_ticket-01-3
  ```

- Then: count all three conditions again and rewrite `trials/results.md` with v1 and v2.

## Done when

- The new rule ships in `setup/SKILL.md`.
- The 36 trials are run and judged. They spend the user's usage: say how many are about to run and wait for a go.
- `trials/results.md` says whether v2 stopped the charter edits and what it did to drift.
