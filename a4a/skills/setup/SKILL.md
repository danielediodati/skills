---
name: setup
description: Prepare a project that builds on models for work by seam charter. Adds the rule to AGENTS.md and reports which stochastic seams have a charter. Run once per project.
disable-model-invocation: true
---

# Set up an agentic project

A **stochastic seam** is a point where a model decides: an agent, a router, a prompt, a model judge. Its **seam charter**, at `evals/<seam>/charter.md`, says which decisions the model is free to take and which ones code constrains. This setup makes every coding session meet that charter before it touches a seam.

## Steps

1. **Find the instructions file.** Use `AGENTS.md` at the repo root; failing that `CLAUDE.md`; failing both, create `AGENTS.md`.

2. **Write the rule.** Add the section below. If the file already has a `## Stochastic seams` section, replace it with this one.

   ```md
   ## Stochastic seams

   A stochastic seam is a point where a model decides: an agent, a router, a prompt, a model judge. Each has a charter at `evals/<seam>/charter.md`: what the model is free to decide, what code constrains, and why. Only the user changes a charter.

   - Read a seam's charter before changing the seam. If it has none, write one first (the `charter` skill does this).
   - A decision the charter lists as free stays with the model. A constant, a default, a closed menu, a fixed reply or a prompt that dictates the answer takes it over and moves the line. Criteria that inform the model's judgement do not.
   - A decision the charter lists as constrained stays in code. Asking the model to take it, or loosening the check, moves the line.
   - Never move a line, and never edit the charter, not even to record what you did. If the request cannot be met without moving a line, make the part that can be made, then stop: name the line, say what moving it would buy, and leave the decision to the user.

   Nothing paid runs without the user's approval: eval runs, trials, model screenings, judge calibrations.

   - Before the first paid call of a ticket, agree one spending budget with the user for the whole ticket.
   - Every later request for approval shows the running total against that budget.
   - Free local checks (unit tests, a dry run of the adapter, a schema check of the cases) run before any paid call.
   - When models are screened, the cheapest goes first.
   ```

3. **Inventory the seams.** Find every place the project calls a model and group the calls into seams, one per thing that is, or should be, evaluated on its own. Report them to the user as a table: seam, where it lives, charter present or missing. Done when every model call in the project belongs to a row.

4. **Hand over.** Tell the user which seams lack a charter and that each is written in its own session.
