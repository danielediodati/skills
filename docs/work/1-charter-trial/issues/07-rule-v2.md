# Close the back door in the rule

Status: ready-for-agent
Blocked by: nothing

## Why

With the charter, 21 of 36 agents edited the charter itself, rewriting the line they had just moved so that the move reads as allowed. The rule's last bullet invites it: "They decide it; the charter changes in the same commit." In a session with nobody to ask, the agent reads that as leave to change the charter alone.

## What it produces

- The `## Stochastic seams` section in `a4a/skills/setup/SKILL.md`, rewritten so that only the user changes a charter: the agent proposes a change and stops, it never edits the charter itself.
- `trials/runs/with-v2/`: the 36 trials with the charter, run again with the new rule; the same judge and rubric.
- A section in `trials/results.md` comparing v1 and v2: drift, stops, flags, and how many agents edited the charter.

## Done when

- The new rule ships in `setup/SKILL.md`.
- The 36 trials are run and judged. They spend the user's usage: say how many are about to run and wait for a go.
- `trials/results.md` says whether v2 stopped the charter edits and what it did to drift.
