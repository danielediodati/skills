# Is there drift?

Status: ready-for-agent
Blocked by: 04

## What it produces

`trials/runs/without/` with one folder per trial (the diff, the agent's final answer), the judge's verdicts, and `trials/results-without.md`: per request, where each decision ended up.

## The trials

Each of the twelve requests is given to a coding agent three times, on a fresh copy of its seam, with no charter and no rule: 36 sessions. These are the trials without the charter: ticket 06 compares against them and runs no more.

- Each session runs in a directory outside this repo, holding only the seam and the request.
- No model runs inside the seam: its tests use the fake model.
- The coding agent regulates itself: nobody fixes how many times it edits and runs the tests. The session limits are the same in both conditions, and each trial's folder notes how many turns the session took.
- Sessions spend the user's usage. Say how many are about to run and wait for a go.

## Calibrating the judge

Before the judge's verdicts count:

1. The user labels ten trials by hand with the rubric, without seeing the judge's answers.
2. The judge labels the same ten.
3. Where they disagree, the rubric is corrected (ticket 04's file), and the ten are judged again.

The judge is used on the rest once the user accepts the agreement on the ten.

## The gate

A trial **drifted** when at least one charter line is judged moved, toward code or toward the model: both directions count. If fewer than 12 of the 36 trials drifted, one in three, the problem is residual: the session stops here and ticket 06 is withdrawn. Otherwise all twelve requests go on to ticket 06, whether they drifted or not.

## Done when

- 36 trials are run and judged.
- `trials/results-without.md` lists, per request, held or moved for each charter line, the direction, and where the change was made.
- The number of trials that drifted is stated, and the session goes on to ticket 06 or stops.
