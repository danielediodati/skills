# Nothing paid runs without approval, and the total is always shown

Status: ready-for-agent
Blocked by: 02, 03

## What it produces

Decision 14 in `edd`, in `run_evals.py` and in the rule `setup` writes into a project's `AGENTS.md`:

- A spending budget for the ticket is agreed with the user before the first paid call.
- Every later request for approval shows the running total against that budget. The runner logs the cost of each run and the total.
- Free local checks (unit tests, a dry run of the adapter, a schema check of the cases) run before any paid call.
- When models are screened, the cheapest goes first.
- When the budget is spent and the runs are still below the target with the charter intact, `edd` stops and puts the ways out to the user, taking none itself: another model, the line moved on purpose (charter change, both versions run, ADR), a lower target, or the failure accepted. A model change is recommended with its evidence: what was tried on the model's side and how it failed.

## Done when

- A run that would pass the agreed budget refuses to start and prints the total and the budget.
- The `AGENTS.md` rule of `setup` carries the spending lines.
