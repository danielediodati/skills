# entrance charter

Input: one user message on a chat thread (`heard`), with the thread's whole conversation; or one situation the machine names (`relayed`, one of `SITUATIONS`).
Output: one Italian sentence or two for the chat (`answer`), and at most one handoff (`handoff`, `asked`) that `bot._handed_on` runs after the sentence is sent.

## Free
- What a user message is: question, report, request, change, remark: a router's branches were the wooden bot ADR-0006 replaced; only the model reads prose.
- Which handoff a message gets, among the seven: routing is the judgement the `adapt` suite measures (bar 80% routed), not a rule.
- How long a change is meant for (this workout, the mesocycle, the declaration), and whether to ask instead when it cannot tell: the prompt gives examples, no rule; asking costs a turn, guessing costs a plan.
- Answering a hello, a remark or a question about the system itself, with no tool: a turn needs no subgraph to be answered.
- Which engine reads to make, and with what arguments: the reads are the engine's, so any it picks is a fact, never an invention.
- Whether a mid-plan message corrects the plan, asks something new, asks a question, or reports: `MID_PLAN` asks the model; the bot acts on the handoff it chose.
- What is lasting enough to `remember`, and what is true only today: "No rule tells the two apart; you do."
- The wording of every sentence, user turn or relayed situation: what reaches the chat is the model's own sentence, which is the whole of ADR-0006; a situation's text is an instruction, never the line (tested).
- What `said` holds for `adapt_this_workout` and `change_mesocycle`: their words; the planner reads it and decides the rest.

## Constrained
- Language and length: Italian, one or two sentences, no lists or forms (prompt): the user is on a phone, texting a coach.
- The handoff set is closed, seven tools in `HANDOFFS`: each maps to a subgraph `bot._handed_on` knows; a new one is code on both sides.
- No handoff takes an argument except `said`, on the two `CHECKED` ones (tested): what is due, what is planned against and what is logged are derived by code, so the model cannot misstate them.
- `log_workout` sends the user's text as typed, never the model's retelling: the logger reads what was said (ADR-0009).
- The engine reads are the nine named in `TOOLS`; `admissible_set`, `remaining_budget`, `allocate` are withheld: the entrance does not plan or judge a plan (ADR-0006 item 4).
- An exercise read keeps only `KEEPS` (`id`, `name`, `equipment`, `primary_muscles`): the entrance answers in prose and needs the name.
- Which workout is due: never the model's. `todays_workout` takes no arguments and code reads the rotation; another slot goes through `adapt_this_workout`.
- Whether a plan fits: never the model's. The validator judges (ADR-0006 item 4, ADR-0010).
- No training fact, exercise, id or date the tools did not give (prompt, tested on a stand-in): the engine/agent split is what makes a talking entrance safe.
- One handoff per turn: a second is answered `ONE_AT_A_TIME` and not started: one run per ask (ADR-0007).
- A turn that has handed off, or that relays a situation, binds no tools: it only speaks; a call there would be a second handoff or answer nobody.
- A `CHECKED` handoff is assembled before it starts (`startable`); a misread (`MISREADS`, an unknown catalog value with the valid ones listed) goes back to the model as `MISREAD`, a missing mesocycle as `NO_MESOCYCLE`: a refused request costs a retry, not minutes of planning.
- With the next mesocycle waiting, `todays_workout`, `plan_mesocycle` and a refused check become `PREPARED` and the waiting one is offered again: code knows it is there, the model does not.
- Mid-plan, a planning handoff replaces the running plan and a writing one (`WRITES`) waits for it; anything else answers at once (ADR-0006 amended in 15b).
- `remember` is offered only with a store, and its `quote` must be in the user's messages word for word, or it is refused: never remember an inference.
- What the model is told after a call is fixed (`STARTED`, `SERVING`, `NO_MESOCYCLE`, `UNREADABLE`, `SPENT`...): instructions, so it never describes a plan it has not seen.
- Code, not the entrance, takes a message when an interview is waiting, the logger is holding a question, or nothing is declared (`bot.talking`): that is graph state, not something the model works out (ADR-0013).
- A message mid-run on anything but a user-asked plan is queued, not read (`bot.interjecting`).
- `BLOCKED` and `FAILED` stay constants; an empty answer or a raised turn says `FAILED`: the model is absent or not to be trusted, and nothing raised leaves the machine (ADR-0006 item 5).
- Only the owner's messages reach it (`Turns._answers`); two entrance turns on a thread never overlap (`Graphs.talking` lock).
- Model: `deepseek/deepseek-v4-flash`, high effort, pinned to Parasail (`models.NODES`), overridable by `ENTRANCE_MODEL`, `ENTRANCE_REASONING`, `ENTRANCE_HOST`: the cheapest that cleared the adapt suite's bar (ADR-0011); a change is a new matrix row, not an edit.

## Budget
- Calls: `tools.CALL_BUDGET` = 12 tool calls a run, overridable by `--call-budget`; a budget, not a limit the design rests on. Past it, reads and `CHECKED` handoffs are taken off the table and answered `SPENT` if called anyway; the unchecked handoffs stay offered. The prompt asks for one call per turn; code allows several reads.
- Model calls: one per graph step; a turn is usually two (decide, then speak), more with reads. LangGraph's recursion limit is the backstop.
- Cost: $0.0003–0.001 a turn, 1–6 s (ADR-0011); ~300 turns a month, $0.10–0.30.
- Bar: `adapt` suite, 80% routed, 90% of adapted plans holding their row (`docs/adapting/eval-set.toml`).
