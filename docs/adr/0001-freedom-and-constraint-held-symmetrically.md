# 1. Freedom and constraint are held symmetrically

## Context

The plugin grew out of one skill, `edd`, whose rule ran one way. It guarded the model's side only:

> A model seam becomes deterministic code only when an eval shows the deterministic version scores at least as well on the same eval set, beyond the noise floor.

Code that checked the model's output (limits, permissions, budgets) was "deterministic by design" and needed no eval and no decision. The rule matched the failure that had been seen: a coding agent, left alone, moves decisions out of the model and into code, a constant, a default, a closed menu, a canned reply.

## Decision

Where there is freedom, freedom stays; where there is a constraint, the constraint stays. How a seam splits between the two is decided on purpose and written in its charter. The line moves in either direction only by the user's decision, measured on the same cases run on both versions. Neither side is the default.

## Why not the one-way rule

- **A constraint is a decision too.** That a value comes from a list, that arithmetic is done in code, that a customer's tier never reaches the model: each was chosen, for reliability, cost, latency or an answer that is easy to check. A rule that protects only freedom lets a constraint dissolve into model judgement (over-delegation) without anyone deciding it.
- **A one-way rule gives the agent a side to lean on.** Told that code taking over is the fault, an agent in doubt hands the decision to the model. The plugin does not claim that more model is better. It claims that the line stays where the user put it.
- **One question covers both directions.** "Does this change move a decision across the line?" is asked the same way of a new constant and of a loosened check. Two rules, one per direction, would need a ranking between them.

## Considered

- **Keeping the one-way rule.** Simpler, and it is the drift that has been observed. Set aside because it leaves half of the charter unprotected.
- **Constraint as the default,** since it is cheaper and easier to check. Set aside: it is programmatic drift made into policy.

## Consequences

- A charter lists both sides, each line with its reason, including decisions nobody took on purpose.
- The rule in `AGENTS.md` and the diff check in `edd` read a change in both directions.
- A move in either direction is decided by an eval and recorded in an ADR.
- The evidence is not symmetric. Drift toward code is what the trials measure; over-delegation has no real episode behind it yet (`CONTEXT.md`, Known limits).
