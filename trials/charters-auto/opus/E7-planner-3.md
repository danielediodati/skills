# planner charter

Input: a `plans.Request` (one workout: equipment, minutes, groups, allocation, exclusions, preferences, an adaptation, refusals) or a `plans.MesocycleRequest` (one request per slot, a change, refusals); then the user's answer at the interrupt.
Output: a validated `WorkoutPlan` or `Mesocycle` offered at `interrupt()`; on acceptance a prescribed workout or a kept mesocycle in SQLite; a closed run in the archive.

## Free
- Which exercises, from the admissible set: choosing what is good is the agent's (ADR-0001); the engine only says what is possible.
- The workout's structure: blocks, straight sets vs supersets vs circuits, order, rounds, reps or seconds and their amount. ADR-0001 rules out split menus and structure rules.
- Rest per block: the 3 min / 90-120 s / 60 s bands are a reference in the prompt, never checked; ADR-0001 rules out a fixed rest.
- How the time divides over the groups: the brief's allocation is "a starting point and not an instruction", `allocate` takes any proportions. The engine has no time ratios (ADR-0001).
- A full workout or a reduced one, as long as it fits: nothing requires the budget to be filled.
- The one-sentence reason on each block: "the part of the plan only you can supply"; only non-empty is checked.
- Proposing a preferred-against exercise anyway, with a `despite` row saying why: a preference is knowledge, not safety (TRAINER.md invariant 4). Only silence is refused.
- How different a new proposal is from a turned-down one: the validator holds the weakest reading, *not the same document* (ADR-0007 item 5); more would be code deciding method.
- What to keep when adapting today's mesocycle slot or changing a mesocycle: the prompt asks to keep what fits and change what was asked, and no code compares against the original.
- A mesocycle's number of cycles and its one-sentence why: the agent's choice, like rest (ADR-0008 item 2); code checks only a number >= 1 and a non-blank reason, and on a change that it is at least the current cycle.
- Which tools to call, in what order, and when to stop and emit: within the call budget, the model decides; a turn without tool calls goes straight to emit.
- Covering each requested group with a primary-muscle exercise, once before any second block: asked in the brief, not validated. A coverage rule is ruled out by ADR-0001; degeneration is measured by the volume deficit instead.

## Constrained
- Exercise ids are held to today's admissible set twice: as an `enum` in the emit schema (ADR-0004 item 3, so decoding cannot invent an id) and by `_every_id_admissible`. A mesocycle's enum is the union over slots, and the validator holds each slot to its own set.
- Standing exclusions, today's budget and groups are folded into a single-workout request once in `turn`, so schema and validator describe the same space. The duration cap is refused, never clamped (`within_the_cap`).
- The plan must fit `budget_min`: over budget is refused whole, never trimmed (ADR-0001). A trim would hide the arithmetic from the agent.
- Each exercise appears at most once per workout (`duration.check_plan`); the same exercise may appear in two mesocycle workouts.
- Shape is fixed by `WorkoutPlan` / `Mesocycle` with `extra="forbid"`: a misspelled field would be a prescription nobody wrote. `Prescription` is one `unit` (`reps` | `seconds`) and an `amount`, so both-or-neither cannot be expressed; `rest` is seconds, told in the schema after a `60000` ms run.
- `despite` may name only exercises the user actually said no to: an invented refusal would be printed back as the user's words.
- A plan or mesocycle identical to one turned down in this negotiation is refused: the newest compared whole, older ones by exercise ids in order (ADR-0007 item 4).
- A mesocycle has exactly one workout per slot, in the split's order.
- What the model is told is fixed text: `PLANNING`, `MESOCYCLE_PLANNING`, `brief`, `FEEDBACK`, `REFUSED_TURN`, `EMIT_PLAN`. The validator's refusal goes back verbatim, naming every rule broken.
- The tools offered are the named tuple `TOOLS`, every shared tool except `prescribed_workout`; named, never derived by subtraction, so no tool arrives undecided.
- Tool answers are cut to `KEEPS` (`id`, `equipment`, `primary_muscles`): `name`, when shown, got copied into `exercise_id`.
- A bad tool call comes back as a failed result the model can recover from, never an exception (`tools.execute`).
- Order is fixed by the graph: planner <-> tools until no tool call or budget spent, then emit (one structured `json_schema` call), validate, propose, prescribe.
- Nothing is written before acceptance: a proposed plan lives in the checkpointer, and `prescribe` writes only after the resume (ADR-0005). The eval never resumes, so it cannot write.
- On acceptance a single workout is prescribed (or `record_adapted` when adapting a slot); a mesocycle is kept and prescribes nothing (ADR-0008 item 4).
- Turning a plan down ends the run and starts a following one in the same negotiation; messages are cleared and the brief is rewritten with every refusal; `said` survives (ADR-0006, ADR-0007).
- A shorter `minutes` in a refusal replaces the budget and drops the allocation, so `turn` divides the new minutes.
- In a mesocycle brief, exclusions and preferences are read from the first slot only.
- A quota error from the provider is raised at once: every retry would be refused the same way.
- Today's date is `date.today()`, for standing exclusions and the written workout.
- The planning model runs at `reasoning: low` on `gpt-oss:20b` by default (`models.REASONING`, `DEFAULT_MODEL`); the provider is configuration (`LLM_BACKEND`, ADR-0004 item 8).

## Budget
- Tool calls: `tools.CALL_BUDGET = 12` per run, a budget overridable by `--call-budget`. Counted per answered call, so one turn can overshoot; past it the model is bound without tools and then asked to emit.
- Attempts: `ATTEMPTS = 3` plans per run before the validator's refusal ends it (`REFUSED`). A budget that shapes the prompt ("You have 3 attempts").
- Provider refusals: `REJECTIONS = 2` in a row, reset by the first accepted turn; the third is raised. Counted in a row so isolated hiccups do not end a recovering run.
- Model calls per run: one per planner turn plus one emit per attempt; no wall-clock limit in the graph. Measured on the CPU: one plan about 4 minutes, a run refused twice about 11 (ADR-0004).
- Runs per negotiation: unbounded; each refusal by the user starts another.
