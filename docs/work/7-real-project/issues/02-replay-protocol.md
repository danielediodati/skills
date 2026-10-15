# Freeze the replay protocol

Status: ready-for-agent
Blocked by: 7.1

## What it produces

A protocol for replaying REPS's episodes, written and frozen before any paid call, as `trials/protocol-silent-drift-3.md` was for the synthetic seams.

- The rubric and the judge of sessions 4 to 6 (`trials/judge/`), changed only where seams in cascade need it: a move made in one seam that shows only in the next.
- The cases, chosen by the user from `trials/reps/`: the episodes E1, E2 and E7, E5 stopped at its ticket, and the declared moves D3 and D4.
- Each replay starts a fresh session at the case's `from` commit, with its `request.md` alone.
- A drift written in a plan counts (`CONTEXT.md`, *Drift episode*): a replay that drifts in a ticket, a draft or a proposal is judged there, without waiting for the code. E2 and E5 are judged on what the agent writes.
- The agent is the model that made the episode: Opus 5 or Opus 5.5. Where Opus 5 can no longer be called, Opus 5.5 runs it and the result says so. This reverses, for REPS only, session 6's choice to keep Opus out as an agent for its cost: the comparison is with the drift that really happened, so the model is the one that made it.
- Two conditions on each episode and each declared move, 3 runs each: without a charter, then with one. The charter is the one the plugin produces: the agent drafts it alone from the code at the parent commit, nobody reads it, and the rule is in `AGENTS.md`.
- An episode whose drift shows in none of the 3 runs without a charter is reported as not reproduced, and its runs with a charter are not made.
- Two numbers come out: on the episodes, in how many runs with a charter the line holds against the runs without; on the declared moves, how often the charter stops the agent on a move the user wanted, against the runs without.
- The rule that reads the result is fixed here, before any run.

Writing the protocol costs nothing.

## Done when

- The protocol is in `trials/`, with its rule for reading the result, and the user has read it.
