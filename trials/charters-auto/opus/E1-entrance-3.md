# entrance charter

Input: one message the user wrote (`heard`), or one situation the machine names (`relayed`, one of `SITUATIONS`), on top of the thread's whole conversation.
Output: `answer`, the model's own sentence for the chat, and `handoff`, which of `todays_workout`, `plan_mesocycle`, `log_workout` the turn reached for (empty when it answered itself).

## Free
- Which of these a user turn is: answer it directly, run one or more reads, or hand off: a classifier with fixed branches is what ADR-0006 replaced, and the prompt only lists the cases.
- Whether a message is a request for today's workout, a request for a mesocycle, a "yes" to an offer of one, or a report of past training: judged from the conversation, which only the model reads.
- Which reads to call and with what arguments: lets a question nobody foresaw be answered without a subgraph.
- Every word the user reads, for both user turns and relayed situations: a word written in advance is the woodenness ADR-0006 removed (`test_a_situation_is_said_in_the_models_own_words`).
- Offering to plan a mesocycle when there is none, and waiting for a yes before `plan_mesocycle`: asked of the model by `NO_MESOCYCLE`, not checked by code.

## Constrained
- Italian, one or two sentences, no list or form: asked by `TALKING` and `RELAYING` only; nothing checks the reply's language or length.
- No training fact the tools did not give: kept by what the model is shown (system prompt, user's words, its own turns, tool results; `test_the_entrance_states_no_training_fact_it_did_not_get_from_a_tool`) and by the prompt; no check on the reply. A fact folded into the context any other way would be one it could state unsourced.
- A relayed situation is said with no numbers and no exercise names: prompt-only (`RELAYING`).
- The read surface is the closed list `TOOLS` (8 engine reads), resolved through `tools.registered`: the entrance answers questions and never plans, so `admissible_set`, `remaining_budget` and `allocate` stay off it (ADR-0006 item 4).
- Every tool is read-only and the entrance writes nothing: writing happens only in a subgraph or on an accepted button (ADR-0006, `build` docstring).
- Tool results are trimmed to `KEEPS` (`id`, `name`, `equipment`, `primary_muscles`): `name` so the answer is prose, not an id.
- The handoffs are the closed set `HANDOFFS` and take no arguments: which workout is due is the rotation's (`mesocycles.today`), what to plan against is derived from the declared config, and the report reaches the logger as the user typed it, never retold.
- One handoff per turn: the first handoff call wins; any later one in the same reply is answered `ONE_AT_A_TIME` and not started. Two runs from one message are two drafts for a chat that asked once.
- A turn that has handed off, or was opened to relay a situation, is bound to no tools: the only thing left is to speak, and a call there would be a second run nobody asked for.
- A handoff call is answered by code with a fixed English instruction to the model (`SERVING`, `NO_MESOCYCLE`, `UNREADABLE`, `STARTED[...]`), never with words for the user. `todays_workout` reads the mesocycle in code; `UNREADABLE` (machine state) is kept apart from `NO_MESOCYCLE` so it never offers a plan the machine cannot make.
- Today's workout itself is sent by code after the model's message (`bot._serving`), and the model is told to say nothing of its content: it never sees it.
- The situations the machine can relay are the closed list `SITUATIONS` (8), written in English as instructions: each was a fixed Italian line before, and a new one must be added there so a test reaches it.
- `BLOCKED` and `FAILED` are fixed Italian constants in `bot`, never the model's: they are the cases where the model is absent or not trusted, and nothing raised leaves the machine (ADR-0006 item 5).
- An empty answer, or a turn whose last message is not the model's, gets `FAILED`: an empty reply is the model failing, not choosing silence.
- A wrong tool call (unknown name, ill-fitting arguments) comes back as a failed tool result the model may correct next round, and counts against the budget.
- The system prompt is prepended on every turn, not stored: the history is never cleared, and a stored prompt would freeze on the day the thread began.
- A message answering the logger's pending clarifying question bypasses the entrance: the graph's state decides it, not the model.
- The run closes at the entrance (`DONE`) unless `plan_mesocycle` or `log_workout` carries it on: one user request is one run (ADR-0007).
- The model is chosen by settings, not code: `ENTRANCE_BACKEND` / `ENTRANCE_MODEL`, falling back to the coach's provider and on Ollama to `llama3.1` with reasoning off, because this is the node the user waits on (ADR-0006 item 3).

## Budget
- Reads: `tools.CALL_BUDGET` = 12 tool calls per run, shared counting with handoff-turn reads; a budget value, raisable via `build(budget=...)` (the bot uses the default). Past it, reads are no longer offered (`talk`) and no longer run (`read` answers `SPENT`). All reads in one reply run if the count was under budget when it arrived, so one reply can overshoot; reads beside a handoff are counted but not budget-checked.
- Model calls: 1 for a direct answer or a relay, 2 for a handoff (decide, then speak), +1 per read round; no other cap besides the read budget and LangGraph's recursion limit.
- Context: the whole thread history, unbounded; no trimming or summarising.
- Time: no timeout. Measured on the dev laptop with `llama3.1`: about a minute per user turn (~2.7k input tokens, mostly tool definitions), about 6 s for a relay (ADR-0006).
