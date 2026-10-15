# The history cleaned

Status: ready-for-agent
Blocked by: 02

## What it produces

One rewrite of `main` and `session-7-reps` before anything is public, while rewriting costs nothing.

- In every commit, the author's local paths become what ticket 02 made of them.
- The `Claude-Session` trailers leave every message; `Co-Authored-By` stays.
- Every commit keeps its author, its dates and its order.
- The version tags point to the rewritten commits; the backup tag and the rewrite's own refs are deleted.

## Done when

- No commit on either branch, and no tag, names the author's home directory or a Claude session.
- Every commit's dates match the commit it replaces.
- The full test suite is green at the tip of both branches.
