# Split the docs by purpose

Status: ready-for-agent
Blocked by: 1

## What it produces

Each repository holds the files of its own purpose: `ROADMAP.md`, `openpoints.md`, `CONTEXT.md`, `docs/adr/`, `AGENTS.md`. An item goes where its closing changes something: a decision about what the plugin does stays in `skills`, even when its evidence is in `skills-eval`, and links to it; a question about how drift is measured goes to `skills-eval`.

- `skills-eval`: a `ROADMAP.md` whose *Done* table carries sessions 1-7 as its own history; an `openpoints.md` with what is not yet measured; a `CONTEXT.md` with the trials' vocabulary (trial, condition, run, protocol, calibration, replay, episode, declared move); an `AGENTS.md` with the same issue tracker.
- `skills`: an ADR for the decision: evals in a repository of their own, pinned to a plugin tag; a session that changes the plugin and measures it is two linked sessions, change first, then measure, each closed in its own repository.

## Done when

- Every line of `skills`' `openpoints.md`, `CONTEXT.md` and `ROADMAP.md` is in the repository its purpose names, or left where it is on purpose.
