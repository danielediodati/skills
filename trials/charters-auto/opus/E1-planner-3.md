# planner charter

Input: a `plan.Request` (equipment, minutes, groups, allocation, exclusions, preferences, refusals of this negotiation) or a `MesocycleRequest` (one `Request` per slot), assembled by `plan.requested` before any model call; then the user's answer to the proposal (`accepted`, or `because` and an optional shorter `minutes`).
Output: a `WorkoutPlan` (blocks with items, rounds, rest, reason; `despite`) or a `Mesocycle` (one workout per slot, `cycles`, `why`), proposed at an interrupt; on acceptance a prescribed workout or a kept mesocycle in SQLite, and a run record in the archive.

## Free
- Which exercises, out of the admissible set: the agent decides what is good, the engine only what is possible (ADR-0001).
- The workout's structure (how many blocks, straight sets / superset / circuit, order): method is the agent's (ADR-0001).
- Rounds and reps-or-seconds amount per item: no schema bound beyond the engine's own (rounds >= 1); a cap would be the engine prescribing method.
- Rest per block: the 3 min / 90-120 s / 60 s bands are given as a reference, not a rule; a fixed rest is ruled out by ADR-0001.
- The block's `reason`: the one part of the plan only the model can supply; code checks only that it is non-empty.
- How the minutes divide over the groups: the even `allocation` is offered as a starting point, `allocate` divides any other way, and nothing checks the plan kept it (`Request.allocation`).
- Covering each group with a primary-muscle exercise before a second block: asked in the brief, refused by no rule; degeneration is measured by the volume deficit, not forbidden (ADR-0001).
- A full workout or a reduced one, as long as it fits the time: ADR-0001.
- Proposing an exercise the user would rather not do, with a `despite` row saying why: a preference is knowledge, not safety, and the user can say no again (TRAINER.md's fourth invariant).
- How a new proposal differs from the ones turned down: only "not the same" is checked; how different is the agent's business (`_not_a_plan_already_refused`).
- Which tools to call, how many per turn, and when to stop and emit: a turn with no tool call goes straight to emit.
- How many cycles a mesocycle lasts, and why: the agent's choice with a reason; code checks `cycles >= 1` and a non-blank `why`, nothing else (ADR-0008 item 2).

## Constrained
- The graph: planner -> tools -> planner ... -> emit -> validate -> propose -> prescribe, fixed edges; a loop the model steered would make cost and the end of a run unpredictable.
- The tool surface is a named list of ten (`TOOLS`), never derived by subtraction; `prescribed_workout` is withheld, a planner has no workout to read back. A renamed tool must not arrive unannounced.
- Tool results are trimmed to `id`, `equipment`, `primary_muscles` (`KEEPS`): the model is not shown a name it could write in place of the id.
- A bad tool call (unknown tool, wrong argument shape, `ToolFailure`) is a failed result back to the model, never a crash: the mistake is recoverable next turn, a traceback loses the run.
- Standing exclusions, the duration cap and the groups are folded into the request once, before the brief (single workout only): the emit schema and the validator must describe the same space. The mesocycle path takes its slots as assembled and does not fold again.
- The emission is strict structured output (`json_schema`), every property required, `extra="forbid"`: a misspelled field silently ignored is a different workout that validates.
- `exercise_id` is an enum of today's admissible ids in the emit schema: an id outside the set cannot be written. For a mesocycle the enum is the union over slots; which slot admits which id is the validator's.
- Prescription is `unit` in {reps, seconds} plus `amount`: both-or-neither cannot be expressed. `rest` is described as seconds in the schema after an observed `rest: 60000`.
- Validation is code, in a fixed order: duplicates, admissibility, then budget only if both passed, then preferences, then refused-already. A shape error is one `shape` violation and no rule runs.
- An exercise appears at most once per workout; the same exercise may appear in two mesocycle workouts.
- A plan over the time is refused whole, never trimmed (ADR-0001): a silent repair hides the arithmetic from the agent.
- A `despite` row for an exercise the user never refused is a violation: the renderer would print it back as the user's own words.
- A preference prescribed without a `despite` row is a violation: silence is the failure, not the choice.
- A plan equal to a refused one is a violation: whole-document equality against the newest refusal, exercise-id sequence against the older ones (ADR-0007 item 4).
- A mesocycle must have exactly one workout per slot, checked first and alone; each workout is then validated against its own slot.
- Every violation goes back to the model in one message naming every rule broken (`FEEDBACK`); there is nobody to argue with.
- A run the validator refuses `ATTEMPTS` times ends as `refused` and offers nothing.
- A provider exception on a planner turn goes back to the model as `REFUSED_TURN` (strict JSON, literal numbers), counted consecutively and reset by the first accepted turn; a quota error is raised at once. A provider error during emit is not caught.
- The brief is written once per run; a refused plan is answered on the same history, a turned-down one starts a new run with the messages cleared (ADR-0007).
- What a turned-down plan leaves behind: the newest whole with the user's words, older ones as ids with words; never a generated summary (ADR-0007 item 4).
- A shorter `minutes` in the answer replans against that budget with the allocation dropped; the cap still applies. A mesocycle refusal ignores `minutes`.
- Nothing outside the state is touched before the interrupt: a resumed node runs again from the top (ADR-0005).
- Only an accepted plan is written: a single workout as prescribed today; a mesocycle is kept and prescribes nothing until served (ADR-0008 item 4).
- The mesocycle brief states exclusions and preferences from the first slot only; the validator checks each slot's own.
- Runs go to the archive only when `build` is given one; Studio uses the home's, the eval suites none.

## Budget
- Tool calls: `CALL_BUDGET` = 12 per run, a default overridden by `--call-budget`; when spent the graph stops offering tools and asks for the plan. A turn's parallel calls all run, so a run can end a little over.
- Plan attempts: `ATTEMPTS` = 3 per run, stated to the model in the prompt; the constraint on how long a refused run may go on.
- Provider refusals: `REJECTIONS` = 2 in a row, the third is raised; a model that fails twice running will not on the third.
- Model calls: one per planner turn plus one emit per attempt; no other model call (no summary, no judge).
- Output tokens: `GROQ_MAX_TOKENS`, default 1000 = Groq's free-tier ceiling, a provider limit rather than a design one. Ollama's context comes from the environment.
- Wall time: no timeout in code; measured per node in the run record.
