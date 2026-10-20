# entrance charter

Input: one user message on a thread (`heard`), with the thread's whole conversation; or one situation the machine names from `SITUATIONS` (`relayed`)
Output: `answer`, the model's own sentence for the chat; plus at most one `handoff` with the `asked` arguments for the subgraph the caller runs next

## Free
- What a turn is (answer it, read, hand off, or ask back): the entrance is a conversation, not a classifier (ADR-0006 item 1). A router's branches can only speak in constants. The prompt guides the choice and code does not check it.
- Whether a change is for this workout, the mesocycle or the declaration, or whether to ask which: only the model can read the duration in prose. The prompt says to ask in one sentence and call nothing when the duration is unclear.
- Every word the user reads, relays included: `answer` is the model's sentence and never a constant. `RELAYING` and `STARTED` are instructions to the model, not the text sent. Written words would bring the router back (ADR-0006, `test_the_situations_are_instructions_...`).
- Register and length (Italian, one or two sentences, no lists): held by the prompt only, with no check in code.
- The arguments of `adapt_this_workout` (`minutes`, `equipment`, `leave_out`, `ask_for`, `workout`), read from what the user wrote: the constraint lives in their prose, which is the entrance's to read. Code checks the arguments and does not choose them.
- `said` on `adapt_this_workout`, `change_mesocycle` and `change_declaration`: the user's request in their own words, for the subgraph to read.
- Which exercise the user means: the model resolves it with `search_exercises`, or asks the user. It may never invent an id.
- Which engine reads to make, and how many within the budget: questions about training are answered here, without entering a subgraph (ADR-0006 item 2).
- After a `MISREAD`, whether to call again with the error fixed or ask the user: the error says what was wrong, and only the model knows what the user meant.
- What is lasting enough to `remember`, and the `conclusion` line: the prompt says "No rule tells the two apart; you do".
- Handling a dislike or an ache (ask one question, start nothing): prompt only.

## Constrained
- The read surface is the 8 named `TOOLS`, all read-only, with no `admissible_set`, `remaining_budget` or `allocate`. Those are planning arithmetic, and the entrance never plans or judges a plan (ADR-0006 item 4, test). The list is named explicitly and not derived by subtraction.
- What a read returns about an exercise is trimmed to `KEEPS` (`id`, `name`, `equipment`, `primary_muscles`). The entrance answers in prose, and `name` is what it needs.
- Training facts come only from tool results. Structurally, the reads are the only source. The rule against stating any other fact is enforced by the prompt, plus a stand-in test.
- `todays_workout`, `plan_mesocycle`, `log_workout` and `set_up` take no arguments. Which workout is due belongs to the rotation, and a report reaches the logger exactly as it was typed. A parameter would be a place to invent one (test).
- `change_mesocycle` and `change_declaration` take only `said`. `adapt_this_workout` names no workout content, only a cycle slot number (test).
- Code answers `todays_workout` by reading the mesocycle, with one of `SERVING`, `NO_MESOCYCLE` or `UNREADABLE`. The workout's content goes to the chat after the model's message and never through it.
- When the next mesocycle is already waiting (`prepared`), `plan_mesocycle`, a `NO_MESOCYCLE` read and a `NO_MESOCYCLE` refusal are all turned into `WAITING_MESOCYCLE` / `PREPARED`. This stops a second mesocycle from being planned beside the one on offer.
- One handoff per turn: every handoff after the first is answered `ONE_AT_A_TIME` and is not started. The user asked once, so one run follows (ADR-0007).
- Once a turn has handed off, and on every relayed turn, no tools are bound. The only thing left to do is speak, and a call there would be a second handoff or a call answering nobody.
- `adapt_this_workout` and `change_mesocycle` (`CHECKED`) are assembled by `startable` before they start. A misread (`MISREADS`, or an unknown filter value with the catalog's own values listed) goes back as `MISREAD` to be retried. `plans.Excluded` goes back as `REFUSED`, with the instruction not to retry. The other handoffs always start.
- A single value where a list belongs is read as a one-item list (`_listed`). `minutes` and `workout` are coerced with `int()`, and a value that fails is a `MISREAD`.
- `remember` is offered only when a store is given. Its `quote` must appear word for word in one of the user's messages on the thread, or it is refused. A conclusion is kept as provisional and keyed on its own content, so a re-run writes it once.
- Nothing here writes training state or plans. Everything else goes to a subgraph that the caller runs after the turn is answered (ADR-0006 item 6).
- The system prompt is put in front on every turn and is never stored. The thread is never cleared, and a stored prompt would freeze the day the thread started.
- An empty or non-AI last message leaves `answer` empty. No fixed fallback reply exists here.
- `BLOCKED` and `FAILED` stay constants outside this seam. Those are cases where the model is absent or not to be trusted, and a generated apology would be a way for an exception to leak out (ADR-0006 item 5).
- The run is closed here unless the handoff is in `CARRIED`. `todays_workout` and `PREPARED` end with the entrance's turn.

## Budget
- Calls: `tools.CALL_BUDGET` = 12 tool calls per run, which is today's value and not a hard limit (`build(budget=...)`, `--call-budget`). The budget is shared by reads, `remember` and `CHECKED` handoffs the engine refused. Handoffs that started, and the unchecked handoffs, cost nothing.
- Past the budget: reads and `CHECKED` handoffs are no longer offered, and are also not run if called anyway (each answered `SPENT`). The unchecked handoffs stay offered. Without the second guard, only LangGraph's recursion limit would end the run.
- Model calls: one per graph pass, with no counter of their own. They are bounded by the call budget plus the turn that speaks. The prompt asks for one call per turn.
- Model: `openai/gpt-oss-120b`, low effort, on Cerebras via OpenRouter (`ENTRANCE_CHOICE`), and `llama3.1` on Ollama. These are settings, not code (`ENTRANCE_MODEL`, `ENTRANCE_BACKEND`). Measured at 0.3-1.2 s and $0.001-0.002 a turn (ADR-0011). Latency is this node's constraint, because the user waits on it.
- Bar: none yet. The entrance has no eval suite, and the bar belongs to a later session (ADR-0011).
