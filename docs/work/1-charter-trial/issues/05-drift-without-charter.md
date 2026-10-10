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

1. The judge labels all 36 trials. The gate is read on these verdicts, provisionally.
2. After ticket 06, the user checks seven verdicts drawn from the 72 trials of both conditions, mixed and with the condition hidden, so the user cannot tell which group a trial belongs to. They are chosen where a wrong verdict would cost most: borderline moves, and lines judged held on code the change touched. Each is shown in two lines, what the agent did and the verdict, and the user answers agree or not.
3. Where they disagree, the rubric (`trials/judge/rubric.md`) is corrected, the affected trials are judged again, and the gate and the comparison are read again.

The user sees the judge's verdict before answering, so their label is blind to the condition but not to the judge: the held verdicts mixed into the seven are there to catch errors in both directions. Labelling ten trials blind by hand was the first plan, dropped by the user as too long.

## 2026-10-10: provisional gate

27 of 36 trials drifted, on the uncalibrated judge: far above 12, so calibration is unlikely to flip it. The session goes on to ticket 06. See `trials/results-without.md`.

## The gate

A trial **drifted** when at least one charter line is judged moved, toward code or toward the model: both directions count. A line moved toward the charter is not drift. If fewer than 12 of the 36 trials drifted, one in three, the problem is residual: the session stops here and ticket 06 is withdrawn. Otherwise all twelve requests go on to ticket 06, whether they drifted or not.

## 2026-10-10: models

- The coding agent is Sonnet 5.5 (`claude-sonnet-5-5`), in both conditions.
- The judge is Opus 5.5 (`claude-opus-5-5`): a different model from the agent, so it does not share the agent's blind spots. Fable was ruled out by the user as judge.
- The user's usual coding agent is Opus: the result speaks for Sonnet, and `trials/results.md` says so among its limits.

## Done when

- 36 trials are run and judged.
- `trials/results-without.md` lists, per request, held or moved for each charter line, the direction, and where the change was made.
- The number of trials that drifted is stated, and the session goes on to ticket 06 or stops.
