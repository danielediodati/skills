# entrance charter

Input: one user message appended to the thread's whole conversation (`heard`), or one situation the machine names (`relayed`: `HELLO`, `QUEUED`, `PRESCRIBED`, `KEPT`, `SUPERSEDED`, `NO_PLAN`, `LOGGED`, `NOT_LOGGED`).
Output: `answer`, the model's sentence for the chat, and `handoff`: `todays_workout`, `plan_mesocycle`, `log_workout` or empty.

## Free
- What a user turn is (today's workout, a new mesocycle, a report, a question, anything else): the entrance is a conversation, not a classifier; a router's branches answer from constants (ADR-0006).
- Whether to answer a turn itself, with no tool: hello, how-it-works and remarks are its own to answer.
- Which engine reads to call and with what arguments, out of the eight offered: a question about training is answered here without entering a subgraph.
- The words of every reply, including every situation: what reaches the chat is the model's sentence, never a constant; a situation with fixed words is the router this replaced (ADR-0006, `RELAYING`).
- Whether to offer a mesocycle when there is none to serve, and to plan only once the user says yes: asked in the prompt (`NO_MESOCYCLE`), not checked.

## Constrained
- The tool surface is a closed list: eight reads (`TOOLS`) and three handoffs (`HANDOFFS`); `admissible_set`, `remaining_budget` and `allocate` are left out: the entrance does not plan (ADR-0006 item 4).
- Reads come only through the shared surface (`tools.registered`, `tools.execute`): a misspelled name is a `SurfaceError`, never a quietly shorter surface.
- An exercise in a read result keeps only `id`, `name`, `equipment`, `primary_muscles` (`KEEPS`): the entrance answers in prose, and it needs the name.
- A tool the model was not offered, or bad arguments, comes back as a failed `ToolMessage`, not an exception: the model's mistake, not the machine's.
- Handoffs take no arguments: what is due, what is planned against, and what the logger reads are derived by code; the model never retells the user's words.
- The logger gets the user's message exactly as typed, never the model's version: a paraphrase is the system's reading of the report (`bot._logging`).
- Which workout is due is read by code (`reading_today`, the rotation off the mesocycle); the model is told only `SERVING`, `NO_MESOCYCLE` or `UNREADABLE`, never the workout. The workout is rendered and sent by code after the model's sentence.
- One handoff per turn: the first call wins, any later one in the same reply is answered `ONE_AT_A_TIME` and not started: one run is one thing pursued (ADR-0007).
- A turn that has handed off, or that was opened to say a situation, is bound to no tools: the only thing left is to speak; a tool there would be a second handoff or a call answering nobody.
- A handoff call is answered with fixed instructions to the model (`STARTED`), not words for the user: it has not seen the plan or the reading, so it must not describe them.
- Whether a plan fits is not asked of the entrance: the validator judges it (ADR-0006 item 4).
- A message that answers the logger's pending question never reaches the entrance: code routes it to the logger by the graph's own state (`bot.talking`).
- No training fact without a tool (no load, sets, volume, last session, exercise, id, date): asked in the prompt, guarded by `test_the_entrance_states_no_training_fact_it_did_not_get_from_a_tool`; the engine/agent split is what makes a talking entrance safe (ADR-0006 item 4).
- Italian, one or two sentences, never a list or a form: fixed in the prompt (`TALKING`, `RELAYING`), not checked in code.
- An empty reply is answered in the chat with the constant `FAILED`, and an exception with `FAILED` too, with the run recorded as failed: the model is absent or not to be trusted there, and nothing raised leaves the machine (ADR-0006 item 5).
- `BLOCKED` (today's workout unreadable when served) and `FAILED` stay fixed Italian lines: the two cases ADR-0006 item 5 keeps out of the model.
- The system prompt is prepended on every call, never stored: the history is never cleared, and a stored prompt would freeze it at the thread's first day.
- The conversation (`messages`, `said`) outlives every run; everything else is reset at the start of a run (`_beginning`): the entrance is the only node that remembers the turn before.
- A turn that hands to `plan_mesocycle` or `log_workout` stays open and is carried on by the subgraph as one run (`carried`); every other turn closes its run at `answer`.
- The model's provider and name are settings, not code: `ENTRANCE_BACKEND` and `ENTRANCE_MODEL`, falling back to `LLM_BACKEND` and to `llama3.1` on Ollama (`GROQ_MODEL`'s on Groq); latency is felt on this node (ADR-0006 item 3). On Ollama no reasoning setting is sent: `llama3.1` refuses it with a 400.

## Budget
- Reads: 12 per run (`tools.CALL_BUDGET`), today's value of a budget, raised with `--call-budget`. Past it the reads are no longer offered and a read still called is answered `SPENT` and not run. Handoffs do not count. Reads called beside a handoff in the same reply are run and counted without the check.
- Model calls: no cap of its own. A user turn is at least two (decide, then speak); each read round adds one; only LangGraph's recursion limit ends a runaway loop. "One call per turn is enough" is in the prompt, not in code.
- Latency: measured about a minute per user turn on `llama3.1` on the dev laptop (~2.7k input tokens, mostly tool definitions) and about 6 s to say a situation, which binds no tools (ADR-0006). Not enforced; the levers are `ENTRANCE_MODEL` and `ENTRANCE_BACKEND`.
- Output: 1000 tokens per call on Groq (`GROQ_MAX_TOKENS`, the free-tier ceiling, raisable on a paid tier); none set on Ollama.
- Context: the whole conversation is sent every call, with no trimming; on Ollama `num_ctx` is `OLLAMA_CONTEXT_LENGTH`.
