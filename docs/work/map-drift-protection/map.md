# Map: drift protection that holds

Label: wayfinder:map

## Destination

The plugin's protection against drift holds: `setup`, `charter` and `edd` agree with each other and with `CONTEXT.md`, a seam created during development gets a charter too, and the final text, measured in `skills-eval`, holds on REPS's cases and on the synthetic seams: milestone `1.0.0` in `ROADMAP.md`. Only then does it ship.

## Notes

- Domain: `CONTEXT.md` (glossary and decisions) and `docs/adr/`. Measurements live in `skills-eval`; a measurement ticket here points to its feature there and does not restate it.
- Every grilling ticket uses `/grilling` and `/domain-modeling`.
- Standing preferences: the user decides trajectory (what a practice does, where it lives, what it costs), questions open with a concrete example; skills state the general rule, never the cases trials found (decision 16); a change to what the skills tell an agent ships only once it is measured (`AGENTS.md`, Release); paid runs stop at 80% of the usage window.
- This map decides: its tickets are decision tickets, questions whose answer is a decision. Building what they decide goes to `ROADMAP.md` as features, whose tickets are work.

## Decisions so far

- Destination narrowed to drift protection: `eval` and `setup`'s eval scripts wait for a later map, since without a protection that holds they have nothing to stand on (`CONTEXT.md`, Status).
- `ROADMAP.md` stays, for building and history; this map holds the decisions toward the destination.
- `openpoints.md` is retired in both repositories: a question toward the destination is a ticket or fog here; one beyond it is parked in `ROADMAP.md`.
- The rule does not name the moves agents do not see as moves, and `edd`'s diff check stops naming them: decision 16 in `CONTEXT.md`.
- One measurement at the end: `skills-eval`'s feature `drafted-again` waits for every change to the rule and to `edd`, and measures the final text.
- `v0.11.0` stays published; it is withdrawn if the measurement of 0.11.0 does not hold.
- [Measure the rule of 0.11.0](issues/01-measure-0.11.0.md): it holds; asked moves made in 6 of 6, episodes drift in 2 of 15; E1 still drifts. `v0.11.0` stays.

## Not yet specified

- The README once the protection holds, and the version it ships as.

## Out of scope

- The `eval` skill, and `setup` copying the eval scripts and creating `evals/`: the next map, once this one closes.
- Hosts other than Claude Code; the candidate skills `budget`, `agent-topology`, `failure-triage`, `context-budget`; the author's personal `roadmap` skill.
