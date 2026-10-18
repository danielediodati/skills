# entrance charter

Input: a message from the owner on a Telegram thread (`heard`), or a situation the machine names (`relayed`: `HELLO`, `QUEUED`, `PRESCRIBED`, `KEPT`, `SUPERSEDED`, `NO_PLAN`, `LOGGED`, `NOT_LOGGED`, `NEXT_MESOCYCLE`, `ONBOARDED`, `DECLARED`), on top of the thread's kept conversation.
Output: one sentence or two for the chat (`answer`), and at most one handoff (`handoff`, `asked`) that `bot._handed_on` runs after the turn has been answered.

## Free
- What reaches the chat: the words are always the model's, for a message and for every relayed situation alike. A sentence written in advance is the router ADR-0006 replaced, and `test_the_situations_are_instructions_and_not_the_words_the_user_reads` holds it.
- Which handoff a message gets, or none: serve, plan, adapt, change, declare, log, set up, read, or answer directly. A message has no closed form, and a classifier ahead of the model is what ADR-0006 removed. Measured against the `adapt` suite's `routed` bar (80%).
- This workout, the mesocycle, or the declaration: how long a change lasts is read from the words. The prompt gives examples, not rules.
- Whether to ask instead of acting: when "today" against "from now on" is unclear, for a dislike with nothing asked, or for an ache or a pain. The prompt asks for one question and no call, and code does not check it.
- Whether to read `due_workout` before it serves or adapts, and which engine reads answer a question: the model picks among the `TOOLS` offered, inside the budget.
- What is worth remembering, and the `conclusion` line: lasting against true only today is "no rule tells the two apart; you do".
- The `said` of `adapt_this_workout` and `change_mesocycle`: "their words", as the model passes them on. The planner reads it and decides the rest.
- Language, length and tone (Italian, one or two sentences, a coach texting): asked in `TALKING` and `RELAYING`, checked by no code.
- What happens to a mid-plan message (`MID_PLAN`): the model reads it as a correction, a new ask, a question, or a report. Code then acts on which handoff it called.

## Constrained
- The owner only: `Turns._answers` drops any other user id before the model sees anything. One owner per installation is the bot's premise.
- When the entrance is not asked: an open interview, a logger question that is waiting, or nothing declared sends the message straight to the interview or the logger (`bot.talking`). That is graph state, "not something the entrance is asked to work out".
- The closed tool surface: the seven `HANDOFFS`, the nine reads named in `TOOLS`, and `remember` only when a store exists. `admissible_set`, `remaining_budget` and `allocate` are left out because the entrance does not plan (ADR-0006 item 4).
- Handoffs take no arguments, except `said` on the two `CHECKED` ones (`test_no_handoff_takes_an_argument_from_the_entrance`). Which workout is due comes from the rotation (`todays_workout`, `mesocycles.today`). What a report says reaches the logger as the user's own text, never a retelling.
- What a read returns is projected to `KEEPS` (`id`, `name`, `equipment`, `primary_muscles`): an id read out loud is not an answer.
- One handoff per turn: after the first, any further handoff in the same reply gets `ONE_AT_A_TIME` and does not start. Two subgraphs on one turn are two runs for one ask (ADR-0007).
- A handed-off turn and a relayed turn bind no tools. The turn that follows them only speaks, so a call there would be a second handoff, or a call that answers nobody.
- `CHECKED` handoffs are put together by `startable` before they start. A misread (`MISREADS`, or an unknown catalog value with the valid values listed) goes back to the model as `MISREAD`, so the user is never promised minutes of work that a state then refuses.
- When a mesocycle is waiting, `todays_workout` and `plan_mesocycle` (and a `CHECKED` handoff refused as `NO_MESOCYCLE`) turn into `PREPARED`, and that proposal is offered again. The model cannot start a second next mesocycle.
- While a plan is being written, a `PLANS` handoff stops it and its replacement goes to the front of the queue. A `WRITES` handoff waits for the plan (`AFTER_THE_PLAN`). Anything else runs at once. The model picks the handoff, and code fixes what that handoff does to the run in flight (ADR-0006, amended in 15b).
- What a handoff call is answered with is a fixed instruction (`STARTED`, `SERVING`, `NO_MESOCYCLE`, `WAITING_MESOCYCLE`, `UNREADABLE`, `REPLACING`): words to the model, never to the user.
- `remember` keeps only a `quote` found word for word in the user's messages on the thread (`conclusions.admitted`). Anything else is refused, and the model is told so. Nothing inferred is kept.
- The entrance writes nothing to the training database and plans nothing. Every write belongs to a subgraph that the caller runs after the turn (ADR-0006 item 6).
- An empty answer, or a turn that raised, reaches the chat as the constant `FAILED`. A precondition that fails behind a handoff reaches it as `BLOCKED`. Neither line is generated (ADR-0006 item 5): nothing raised leaves the machine, and no path is quoted into Telegram.
- The system prompt is put in front of each turn, never stored in the history: a thread keeps the prompt as it is today, not as it was on the day the thread began.
- One entrance turn at a time per thread (`Graphs.talking` lock). `/start` and `QUEUED` skip the work queue, but not the lock.
- The model: `deepseek/deepseek-v4-flash`, high effort, on `parasail` (ADR-0011, the cheapest choice that clears the `adapt` bars). `ENTRANCE_MODEL`, `ENTRANCE_REASONING` and `ENTRANCE_HOST` override it, and there is no fallback host. Changing it means adding a row to ADR-0011's matrix.
- The prompt says "one call per turn is enough", but code holds only one *handoff* per turn. Reads are bounded only by the budget below.

## Budget
- Tool calls: `tools.CALL_BUDGET` = 12 per run, shared with the logger and the CLI, and adjustable (`--call-budget`). It is the current setting of an adjustable budget, not a fixed constraint. Reads, `remember` and refused `CHECKED` calls count against it. Once it is spent, `talk` stops offering reads and `CHECKED` handoffs, and `read` answers any call it still gets with `SPENT` without running it. The unchecked handoffs are always offered.
- Model calls: one per pass through `talk`, which is a reply plus one per round of reads or handoffs. Nothing caps the count apart from the call budget and LangGraph's recursion limit.
- Seconds: one model call may take `models.TIMEOUT_S` = 180 s, with `RETRIES` = 1 and waits of 5, 15 and 45 s on rate limits. Measured at 1–6 s a turn.
- Cost: measured at $0.0003–0.001 a turn, about $0.10–0.30 a month (ADR-0011). There is no cap in code.
