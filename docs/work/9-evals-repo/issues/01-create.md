# Create `skills-eval`

Status: ready-for-agent
Blocked by: nothing

## What it produces

A public repository `danielediodati/skills-eval` holding `trials/` with its history extracted, so every protocol keeps the date it was committed before its first paid call. Beside it, the tests of the trials' scripts (`test_run_trials`, `test_tally`, `test_triage_adapter`, `test_charter_skill`). The plugin it measures is a submodule `skills` pinned at `v0.9.0`; every script and test that read `a4a/` from the same repository read it from the submodule.

Nothing is created on GitHub or pushed without the user's yes, and pushes wait for the evening.

## Done when

- A fresh clone of `skills-eval`, with its submodule, runs the moved tests green.
- `git log` on a protocol in `skills-eval` shows the date it had in `skills`.
- The tally, run from that clone, gives the numbers the plugin's README cites.
