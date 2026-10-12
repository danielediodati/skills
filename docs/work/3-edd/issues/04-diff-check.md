# `edd` checks the diff against the charter as it was

Status: ready-for-agent
Blocked by: 01

## What it produces

A step in `edd`, before a change is accepted: the diff is read against the seam's charter **as it was before the change** (from git, never the working tree, since an agent that moved a line can rewrite the charter in the same diff). Each free decision taken over by code (substitution, templating) and each constraint handed to the model (over-delegation) is named with the line it moves, and the change waits for the user. A score never clears this check (decision 8).

The step names the drift session 1 found agents do not see as a move: input cleaned by code before the model reads it, a parsing rule that also catches a free field, a missing field defaulted instead of refused.

## Done when

- On two diffs from `trials/runs/` judged as drift and one judged clean, following the step names the moved line in the first two and nothing in the third.
