# planner charter

Input: a `plans.Request` (one workout, possibly an adaptation) or a `plans.MesocycleRequest` (one request per slot, possibly a change or a continuation), the user's live conclusions, and the user's answer at the interrupt.
Output: a validated `WorkoutPlan`, `AdaptedPlan` or `Mesocycle` offered at the interrupt; on acceptance one prescribed workout (or a kept mesocycle) and a closed run record; on refusal to the end, a run closed `refused` with nothing offered.

## Free
- Which exercises, inside the admissible set: ADR-0001, the engine says what is possible and the agent what is good.
- Block structure: how exercises group into straight sets, supersets or circuits, and their order: ADR-0001 rules out split menus and templates.
- Rounds, reps or seconds per exercise, and the unit for each: the schema only fixes that it is one of `reps` / `seconds`.
- Rest per block: ADR-0001 rules out a fixed rest value; the methodology's bands are a reference.
- Each block's `reason`: "the part of the plan only you can supply" (PLANNING); required but its content is unchecked.
- How the time divides over the groups: `allocation` is offered as a starting point and nothing checks the plan kept it; `allocate` divides on any proportions.
- Where inside the methodology's ranges the plan lands, for the declared goal: the prompt gives ranges, "not a template".
- Which tools to call, in what order, and when to stop calling and emit: the model owns its exploration within the call budget.
- Proposing an exercise the user would rather not do, with a `despite` row saying why: a preference is not an exclusion (TRAINER.md's fourth invariant).
- How a new proposal differs from the ones turned down: only "not the same document" is checked (ADR-0007 item 5).
- How much weight to give the user's conclusions: "none of it is a rule, and the admissible set is the same without it".
- A mesocycle's `cycles` and its `why`: ADR-0008 item 2, the agent's choice like a block's rest.
- In an adaptation: the time, the groups, which slot it `counts_as` among those still to do, and the `note`: the user's words bind it, not the mesocycle (ADR-0008 item 6). The budget and untrained rules are skipped for it.
- In a change: what to keep of the current mesocycle beyond what the user asked to change.

## Constrained
- Every `exercise_id` is in `admissible_set` for the request (exclusions, equipment, time, groups): held twice, by an enum in the strict emit schema and by the validator, because legality is held at 100% (ADR-0010). An adaptation's schema carries no enum (Anthropic refuses an enum of the whole catalog); the validator alone holds it.
- A mesocycle's emit enum is the union over all slots; which slot admits which id is the validator's: the workouts share one item schema.
- The plan runs within `TOLERANCE_MIN` = 5 minutes either side of the budget, never trimmed or padded: ADR-0001 rules out an automatic cut, so the refusal goes back to the agent. 5 is a chosen value, not a law; prompt, brief and `window` read it from one constant.
- No exercise twice in one workout (the same one may appear in two slots of a mesocycle): `duration.check_plan` cannot cost a duplicate.
- Every requested group has an exercise whose **primary** muscles are in it, when today's set can train it: moved into the validator after Haiku left a group untrained (ADR-0011). Not applied to an adaptation.
- A `despite` row only for an exercise the user actually named as a preference, and a preferred exercise only with a row: silence is refused, and an invented refusal would be printed back as the user's words.
- Not a plan the negotiation already turned down: the newest refusal compared as the whole document, older ones by exercise ids in order (ADR-0007 item 4, the weakest reading).
- An adaptation's `counts_as` is a slot still to do this cycle.
- A mesocycle has exactly one workout per slot, in split order; each workout is checked as its slot's single workout; a change keeps `cycles` at least the current cycle; `cycles >= 1` and `why` non-blank.
- Output shape: strict JSON schema with `extra="forbid"` everywhere, `Prescription` as unit plus amount, `rest` in seconds, `reason` non-empty, `despite` as one list on the plan: each shape choice closes a failure an observed run made (both-or-neither reps/seconds, `rest: 60000`, eight invented refusals).
- What the plan is checked against is the request, never the plan: a plan that declared its own budget could declare one it fits.
- Today's persisted exclusions, budget and groups are folded into the request once, in `turn`, before the brief: schema and validator must describe the same space.
- The tool surface is the closed list `TOOLS`, named rather than derived; `prescribed_workout` is withheld because a planner has no workout to read back.
- Tool results keep only `id`, `equipment`, `primary_muscles`, `mechanic` (`KEEPS`): the model is not shown a name it could write in place of the id.
- A wrong tool call (unknown tool, ill-fitting or extra argument, `ToolFailure`) comes back to the model as a failed result, never a crash: the model can correct it next turn.
- The brief's content is fixed by code: equipment, the window, the goal column, groups with primary-muscle coverage and "cover each once before a second block", the allocation, exclusions, preferences, every refusal (newest whole, older as ids), conclusions with their quotes.
- A mesocycle brief reads goal, exclusions and preferences off the first slot only: every slot is assembled from the same declaration today.
- The brief is written once per run, on an empty history; a refusal by the user starts a fresh run with messages cleared and the brief rewritten (ADR-0007): a new proposal, not an argument with the last.
- A user's refusal with `minutes` replans against that shorter budget and drops the allocation; anything else they said travels as words.
- The flow is fixed: plan over tools, then one separate `emit` call under the strict schema, then validate, then propose at the interrupt; nothing is written before acceptance (ADR-0005).
- An accepted workout is written as one prescribed workout; an accepted mesocycle is kept and prescribes nothing (ADR-0008 item 4); an accepted adaptation is served as the slot it counts as.
- A provider refusing a turn goes back to the model as `REFUSED_TURN`; a quota error is raised at once; text that is not JSON from `emit` is asked again without spending an attempt: both are the provider failing, not the model deciding.
- The planner's model is a configuration, not the model's choice: `models.planner()`, Haiku 4.5 on Anthropic by ADR-0011's rule (cheapest that clears the plan suite's 100%).

## Budget
- Tool calls: `CALL_BUDGET` = 12 per run, overridable by `--call-budget`; when spent, tools are no longer bound and the model is asked to emit. Counted after each turn, so one turn with several calls can pass it. A budget that may be raised.
- Attempts: `ATTEMPTS` = 3 validated emissions per run; the third refusal ends the run `refused`. Each attempt is a paid emit plus planning turns.
- Provider refusals: `REJECTIONS` = 2 in a row, reset by the first accepted turn; the third raises (`ProviderFailed` for non-JSON emission).
- User refusals: unbounded; each starts a new run of the same negotiation.
- Cost and time (ADR-0011): ~$0.13 and ~47 s a two-slot mesocycle on Haiku; ~$0.05 a single plan with a cache breakpoint, `emit` the largest call.
