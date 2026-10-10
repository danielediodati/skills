# Does the charter reduce it?

Status: ready-for-agent
Blocked by: 05

## What it produces

`trials/runs/with/`, and `trials/results.md`: the comparison between the two conditions, which is what the session shows.

## The trials

All twelve requests, whether they drifted in ticket 05 or not. Each is given to a coding agent three times with the charter and the rule: 36 sessions. The trials without are the 36 of ticket 05, kept as they are.

- **With** means: the seam's charter at `evals/<seam>/charter.md` in the trial directory, and the `## Stochastic seams` section in its `AGENTS.md`, read from `a4a/skills/setup/SKILL.md` so that the trial tests the text that ships.
- Skills stay off in both conditions. The trial measures the charter and the rule, not the `charter` or `edd` skills.
- Sessions spend the user's usage. Say how many are about to run and wait for a go.

## Judging

The same judge and rubric as ticket 05, blind to the condition.

## What the result has to say

- Per request and per condition: trials held, trials moved, in which direction.
- How often the agent with the charter flagged the line instead of deciding alone.
- How many lines marked "Not yet in code" moved toward the charter, per condition: an agent closing a gap it was not asked about is the charter at work.
- Whether, with the charter, changes moved into the prompt instead of the code. A decision dictated in the prompt keeps the charter's letter and loses the freedom.
- What the trial cannot show: four seams, twelve requests at most, one coding agent model, seams that are atomic.

## Done when

- `trials/results.md` exists with the table and the limits.
- `openpoints.md` says whether the remaining skills are worth writing, given the result.
