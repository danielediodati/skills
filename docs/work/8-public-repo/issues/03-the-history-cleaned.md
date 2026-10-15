# The history cleaned

Status: ready-for-agent
Blocked by: 02

## What it produces

One rewrite of `main` and `session-7-reps` before anything is public, while rewriting costs nothing.

- In every commit, the author's local paths become what ticket 02 made of them, and so does the test ticket 02 rewrote without a commit, with the messages of the commits that touched it.
- The `Claude-Session` trailers leave every message; `Co-Authored-By` stays.
- Every commit keeps its author, its dates and its order.
- The version tags point to the rewritten commits; the backup tag and the rewrite's own refs are deleted.
- The private remote's `main` replaced by the rewritten one: until then it still holds the old history.

## Done when

- No commit on either branch, and no tag, names the author's home directory, a Claude session, or anything of the author's own git configuration.
- Every commit's dates match the commit it replaces.
- The full test suite is green at the tip of both branches.
- The remote's `main` is the local `main`.

## 2026-10-15

Rewritten locally: both branches and the tags, the first three criteria checked, with 65 of 65 tests on main and 80 of 80 on session-7-reps. Left: the remote's `main`, still at the old history up to `v0.1.0`, replaced by a force push in the evening.
