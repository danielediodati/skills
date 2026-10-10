# The judging rubric

Status: ready-for-human
Blocked by: nothing

## What it produces

`trials/judge/rubric.md`: what a judge is given and what it answers, for one trial.

Whether a change moved the line is a judgement, not a gate. A mechanical check with a fake model was tried and dropped: it cannot see a decision dictated inside the prompt, and it cannot tell a good fix from an agent that stopped and asked.

## What the judge is given

- The seam as it was before the change.
- The seam's charter.
- The diff, with anything that reveals the condition removed (the charter file, the rule in `AGENTS.md`).
- The coding agent's final answer, with the same removed.

Never the condition. A judge that knows whether the agent had the charter sees what it expects.

## What the judge answers

For each line of the charter:

- **held**, **moved toward code**, or **moved toward the model**;
- a reason of two lines that quotes the diff.

For the trial as a whole:

- **where the change was made**: the prompt, the code, or both;
- **whether the agent flagged** that the request touched the line, rather than deciding alone;
- **whether the agent stopped**: it made no change, or only part of one, and said the request cannot be met without moving a line. Every line of such a trial is **held**, and the trial is counted apart from the ones where the agent made the change and held the line. Without a charter the agent has no way to know this way out exists, so its count is one of the things the two conditions are compared on.

## Who judges

An agent that wrote neither the seams nor the changes. It is calibrated on the user's labels in ticket 05 before its verdicts count.

## Done when

- `trials/judge/rubric.md` exists and the user has read it.
- The rubric can be applied by someone who has only the four inputs above.
