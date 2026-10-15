# Session 7 on its own branch

Status: ready-for-agent
Blocked by: nothing

## What it produces

Session 7's commits, from "Session 7: drift episodes, replayed by the model that made them" to "Close ticket 7.2", on a branch `session-7-reps`, and `main` back on "Close session 1" with session 8's own commits on top.

- On `main`, `ROADMAP.md` keeps session 7 under *Parked*: the REPS replay, its protocol frozen and not run, on `session-7-reps`.
- Nothing of session 7 is lost: the branch holds every commit as it is.

## Done when

- `main` holds no file session 7 added (`trials/reps/`, `trials/protocol-reps-replay.md`, `trials/judge/rubric-replay.md`) and no `--reps` in the scripts; the branch holds them all.
- The full test suite is green on both.
