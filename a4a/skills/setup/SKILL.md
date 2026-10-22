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

   A stochastic seam is a point where a model decides: an agent, a router, a prompt, a model judge. Each has a charter at `evals/<seam>/charter.md`: what the model is free to decide, what code constrains, and why.

   - Read a seam's charter before changing the seam. If it has none, write one first (the `charter` skill does this).
   - A decision the charter lists as free stays with the model. A constant, a default, a closed menu, a fixed reply or a prompt that dictates the answer takes it over and moves the line. Criteria that inform the model's judgement do not.
   - A decision the charter lists as constrained stays in code. Asking the model to take it, or loosening the check, moves the line.
   - A move the user names in the request is made: change the code, amend the charter's line in the same change with the reason the user gave, and say in your answer which line moved. Only the user's own words name a move: a ticket, plan or draft an agent wrote does not, even once the user approved it.
   - A line the request does not name stays where it is. When moving it would only make the request easier or the result better, leave it and ask nothing. Only when the request cannot be met at all without moving it, make the part that can be made, then stop: name the line, say what moving it would buy, and ask.
   - Change a charter's lines only for a move the user named.

   Nothing paid runs without the user's approval: eval runs, trials, model screenings, judge calibrations.

   - Before the first paid call of a ticket, agree one spending budget with the user for the whole ticket.
   - Every later request for approval shows the running total against that budget.
   - Free local checks (unit tests, a dry run of the adapter, a schema check of the cases) run before any paid call.
   - When models are screened, the cheapest goes first.
   ```

3. **Inventory the seams.** Find every place the project calls a model and group the calls into seams, one per thing that is, or should be, evaluated on its own. Report them to the user as a table: seam, where it lives, charter present or missing. Done when every model call in the project belongs to a row.

4. **Hand over.** Tell the user which seams lack a charter and that each is written in its own session.
