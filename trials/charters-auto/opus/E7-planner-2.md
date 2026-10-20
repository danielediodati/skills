# planner charter

Input: a `plans.Request` (one workout: equipment, minutes, groups, allocation, exclusions, preferences, refusals, optional `adapting`) or a `plans.MesocycleRequest` (one `Request` per slot, refusals, optional `changing`), plus the user's accept / turn-down answer at the interrupt.
Output: a validated `WorkoutPlan` or `Mesocycle` offered at the interrupt; once accepted, a prescribed workout, an adapted serving or a kept mesocycle in SQLite. A run the validator refuses to the end closes as `refused` with no plan.

## Free
- Which exercises, inside the admissible set: ADR-0001, the engine says what is possible and the agent what is good.
- The workout's structure: number of blocks and exercises, straight sets / superset / circuit, their order. No cap beyond "at least one block" and the clock; ticket 11.2 (needs-info) waits on the user's methodology before anything here is fixed.
- Rounds, the unit (reps or seconds) and the amount per exercise: method, ADR-0001.
- Rest per block: the 3 min / 90-120 s / 60 s bands are in the prompt "as a reference, not a rule" (ADR-0001 rules out a fixed rest).
- Each block's `reason`: "the part of the plan only you can supply"; code only requires it non-empty.
- How the minutes divide over the groups: the even `allocation` is offered "as a starting point and not an instruction", and nothing checks the plan followed it.
- Covering each requested group with an exercise whose primary muscle is in it, and covering all before doubling one: asked in the brief, never validated (ADR-0001 rules out coverage rules; degeneration is measured by the eval suite, not refused).
- Which tools to call, in what order and how many, within the call budget: the prompt asks it not to explore for its own sake.
- Proposing an exercise the user would rather not do, with a `despite` row saying why: TRAINER.md's fourth invariant, "says so and asks".
- How a new proposal differs from the ones turned down: code refuses only an identical one (ADR-0007 item 5); "how different" is the agent's business.
- In an adaptation, what of today's mesocycle slot to keep; in a change, what to rewrite for the cycles left: asked in the brief, not checked against the original.
- How many cycles a mesocycle runs, with a one-sentence `why`: ADR-0008 item 2, like a block's rest.

## Constrained
- Every `exercise_id` is in `admissible_set` for the request (exclusions, equipment, minutes, groups): enforced twice, as an `enum` in the emit schema and by the validator, which reads the set itself so the two cannot disagree. For a mesocycle the enum is the union over slots; which slot admits which id is the validator's.
- Standing exclusions as of today are folded into a single-workout request once, at the first turn, so schema and validator describe the same space. The minutes are refused, never clamped, above `duration_cap_min`.
- An exercise appears at most once per workout; the same exercise may sit in two mesocycle workouts.
- The plan is never trimmed: one over the minutes is refused whole and goes back to the model with the reason (ADR-0001, "an automatic cut" ruled out).
- A plan lands within 5 minutes either side of the minutes asked for (`plan.TOLERANCE_MIN = 5`), with separate messages for over and under: decided by the user in ticket 11.3. Not yet in code, which refuses only over and accepts any plan under.
- `despite` names only exercises in `request.preferences`; a preference prescribed without a row is refused: an invented refusal would be printed back to the user as their own words.
- A plan identical to one the negotiation turned down is refused: the newest compared whole, older ones by exercise ids in order (all that ADR-0007 item 4 keeps of them).
- Mesocycle: exactly one workout per slot, in the split's order; `cycles >= 1` with a non-blank `why`; in a change, `cycles` is the total and at least the current cycle.
- Shape: strict JSON schema, `extra="forbid"` everywhere, `Prescription` as unit + amount so "both or neither" cannot be written, units of `rest` and `rounds` spelled out in the schema (an observed `rest: 60000` cost a run). A document that does not parse is a `shape` violation and spends an attempt.
- Violations are returned in a fixed order (duplicates, admissibility, then the clock only if both passed, then preferences, then refusals), all at once, as one feedback message.
- `ATTEMPTS = 3` validated emissions per run, then the run closes as `refused`: the prompt states the number to the model.
- The tool surface is a closed, named list of ten (`prescribed_workout` left out): named, not derived, so no tool arrives without someone deciding it.
- Exercise records reach the model cut to `id`, `equipment`, `primary_muscles` (`KEEPS`): shown `name`, a model copied it into `exercise_id`.
- A bad tool call (unknown tool, arguments that do not fit, an engine error) returns as a failed tool result, never an exception: the model can correct it next turn.
- A provider refusing a turn is fed back as `REFUSED_TURN` (strict JSON, no arithmetic): up to `REJECTIONS = 2` in a row, reset by the first accepted turn, then raised. A spent quota is raised at once: every retry would be refused the same way.
- Order of the graph: plan with tools, then one structured emit, then validate, then propose; nothing is written until the user accepts (ADR-0005). An accepted mesocycle is kept and nothing is prescribed until a slot is served (ADR-0008 item 4).
- Turning a plan down closes the run and starts a fresh one in the same negotiation: messages cleared, brief rewritten with every refusal; a shorter time the user gives replaces the minutes and drops the allocation. A mesocycle refusal ignores `minutes`.
- The number of refusals a negotiation can take is unbounded in code.
- Reasoning effort `models.REASONING = "low"` on every planning model: chosen for latency on the dev laptop (296 s against 39 s at `high`); ticket 11.2 notes it was never measured in plan quality, so it reads as today's value, not a principle.

## Budget
- Tool calls: `tools.CALL_BUDGET = 12` per run (not per attempt), overridable with `--call-budget`, so a default budget that may be raised. Checked between turns: all calls of the turn that crosses it still run. When it is spent, tools are unbound and the model is asked to emit with what it knows.
- Model calls per run: one turn per tool round plus one per validator refusal, one structured emit per attempt (at most 3), plus provider-refused turns (at most 2 in a row, no total cap).
- Seconds, tokens, cost: no cap in code; per-node timings are recorded in the state.
