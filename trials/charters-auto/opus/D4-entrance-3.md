# entrance charter

Input: one user message on a chat thread (`heard`), with the thread's whole conversation; or one situation the machine names (`relayed`, one of `SITUATIONS`).
Output: one Italian sentence or two for the chat (`answer`), and at most one handoff (`handoff`, with `asked` for `adapt_this_workout` / `change_mesocycle`) that the bot then runs.

## Free
- What a turn is (serve today, plan, adapt, change the mesocycle, change the declaration, log, set up, read, or answer directly): a conversation, not a classifier (ADR-0006). A router's branches are written in advance, and that woodenness is what the entrance replaced.
- This workout, the mesocycle, or the declaration: the model reads how long a change is meant to last, from the prompt's examples. Held at a bar of 80% routed on the adapt suite (ADR-0010, ADR-0011), not at 100%.
- Asking instead of acting: when it cannot tell this workout from "from now on", it asks in one sentence and calls nothing. An ache gets one question; a dislike with nothing asked changes nothing. These are triage judgements, scored as `ask` / `triage` in the adapt set.
- `said` for an adaptation or a change: the user's words, passed to the planner, which decides the rest.
- Which engine reads to call, and when it has enough: the prompt says one call a turn is enough. The budget below is the only limit.
- Whether something is lasting enough to `remember`, and how to word the `conclusion`: "No rule tells the two apart; you do."
- Every sentence the chat reads, including each situation relayed: the sentence is the model's own, never a constant (ADR-0006). `RELAYING` and `SITUATIONS` are instructions to the model, never user-facing text.
- Whether to answer a mid-plan message, replace the plan, or queue a report or declaration: the model decides from `MID_PLAN`, and code then carries out what it called.

## Constrained
- The handoff set is closed (`HANDOFFS`, seven tools). No handoff takes an argument except `said` on the two `CHECKED` ones. Arguments would let the model decide what code derives, like the due workout and the declaration.
- Which workout is due, and what is in it: read off the rotation by `todays_workout` / `reading_today`, and sent by `bot._serving` with no model call. The model must say nothing about what is in it (ADR-0006 item 4).
- Whether a plan fits: the validator's job. The entrance has no `admissible_set`, `remaining_budget` or `allocate`, and never judges a plan (ADR-0006 item 4, `TOOLS` docstring).
- The reads are a named list (`TOOLS`, nine reads through `tools.registered`). They are named, not derived by subtraction, so a new engine tool does not reach the entrance unasked.
- Exercises are trimmed to `KEEPS` (`id`, `name`, `equipment`, `primary_muscles`), so the model answers with names, not ids.
- No training fact without a tool: the prompt forbids it and a test asserts it. Nothing the entrance can call writes, except `remember`.
- One handoff a turn: a second gets `ONE_AT_A_TIME` and is not started. A turn that has handed off, or a relayed situation, binds no tools at all, so a second handoff cannot happen and no tool call is left unanswered.
- `CHECKED` handoffs are assembled by `startable` before they start. A misread (`MISREADS`, or an unknown catalog value, with the valid values read from the catalog) goes back to the model as `MISREAD` for a retry or a question. A missing mesocycle is `NO_MESOCYCLE`, a state rather than an error.
- The next mesocycle waiting (`prepared`) overrides `todays_workout`, `plan_mesocycle` and a `NO_MESOCYCLE` refusal with `WAITING_MESOCYCLE` / `PREPARED`, so a second one is never planned over it.
- While a plan is being written, a planning handoff replaces it (`REPLACING`), and `WRITES` handoffs wait for it (`AFTER_THE_PLAN`). The bot carries this out by stopping the run, or by queueing.
- What each tool call is answered with is a fixed English instruction (`STARTED`, `SERVING`, `NO_MESOCYCLE`, `UNREADABLE`, `SPENT`, ...). It tells the model what happened so it finds its own words; it is never shown to the user.
- `remember` is offered only with a store, and a `quote` not found word for word in the user's messages on the thread (`conclusions.admitted`) is refused. Only what they said is kept, never what was inferred.
- Messages that never reach the entrance: an interview waiting, a logger question waiting, or nothing declared. Each goes straight to its subgraph (`bot.talking`). That is graph state, not something the model is asked to work out.
- `BLOCKED` and `FAILED` are fixed Italian constants (ADR-0006 item 5). An empty answer becomes `FAILED`, and so does an entrance that raised. Nothing raised leaves the machine, and a generated apology would be a place for it to leak out.
- The system prompt is prepended on every turn and never stored, so a thread always runs on today's prompt.
- The language is Italian and the length is one or two sentences, never a list or a form. Both are fixed in the prompt; nothing in code checks them.
- One entrance turn at a time per thread (`Graphs.talking` lock). `/start` is answered outside the queue.
- The model is fixed per node in `models.NODES`: `deepseek/deepseek-v4-flash`, high effort, `parasail`, OpenRouter only. It changes only through `ENTRANCE_MODEL` / `_REASONING` / `_HOST`, by ADR-0011's rule: the cheapest configuration that clears the bar.

## Budget
- Tool calls: `tools.CALL_BUDGET` = 12 a run, counting reads, `remember` and refused `CHECKED` attempts. It is enforced twice: `talk` stops offering the tools and `read` stops running them (`SPENT`). Handoffs outside `CHECKED` are always offered. 12 is today's value of a budget shared with the other nodes, not a number fixed for the entrance.
- Model calls: one per graph pass, with no cap other than the call budget and LangGraph's recursion limit. A handoff turn is two calls: one to decide, one to speak.
- Cost and latency, as measured (ADR-0011): $0.0003–0.001 and 1–6 s a turn, about 300 turns ($0.10–0.30) a month. These are observations, not limits enforced in code.
- Quality bars (`docs/adapting/eval-set.toml`): routed 80%, held 90%. These are the line a model change must clear.
