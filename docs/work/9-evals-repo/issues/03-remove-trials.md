# Remove `trials/` from `skills`

Status: ready-for-agent
Blocked by: 1, 2

## What it produces

`skills` without `trials/` and without the tests that moved, in an ordinary commit: history is not rewritten, since a plugin installed from the marketplace comes as a shallow clone. Every link to a trial in the README, `a4a/README.md`, `CONTEXT.md` and the ADRs points to `skills-eval` at a tag.

## Done when

- The tests left in `skills` pass.
- Every link to `skills-eval` resolves at its tag.
