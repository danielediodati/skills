# triage_ticket charter

Input: a ticket dict with `subject`, `body` and optional `tier` (`free`, `pro`, `enterprise`), plus a `model` callable (prompt string in, string out)
Output: dict with `queue`, `urgency`, `summary` (one line, max 120 chars), `respond_within_hours`

## Free
- Queue choice: the model reads the ticket and picks the team; this is the judgement the seam exists for, and the code only checks the pick is in the closed list.
- Urgency choice: the model judges how pressing the ticket is from its content; code only maps it to the closed list and applies the enterprise bump.
- Summary wording: the model phrases what the customer needs; code only collapses whitespace and caps length, so wording stays the model's.
- Which details the summary keeps: the model decides what matters from a long or messy body, since the prompt gives it no fixed template beyond "one sentence".
- Reading of a decorated or chatty answer: the model may use markdown, bullets or capitals; the code tolerates them (see Constrained), so the model is not forced into one exact format.

## Constrained
- Ticket with neither subject nor body: raises `ValueError` before any model call; there is nothing to triage and a call would only waste budget.
- Subject and body are stripped of surrounding whitespace before use: avoids empty-looking tickets and noise in the prompt.
- Body sent to the model is cut to the first 2000 characters: keeps the prompt within a context and cost budget (a budget, may be raised; the test checks the cut, not the number). Subject is not cut.
- Queue list (`billing`, `technical`, `account`, `shipping`, `general`): closed set rendered into the prompt and checked in code; the routing desk only has these queues, so a new value would route nowhere. Tight.
- Urgency list (`low`, `normal`, `high`, `urgent`): closed set, same reason; the response-time table depends on it. Tight.
- Unknown or missing queue becomes `general`: a safe default that keeps the ticket visible instead of dropping it. Tight.
- Unknown or missing urgency becomes `normal`: the middle default, neither hiding a ticket nor flooding urgent queues. Tight.
- Answer format is requested as three lines in the prompt, but parsed by code: a regex reads `queue`, `urgency`, `summary` lines tolerant of case, markdown and bullets; the first occurrence of each field wins. Code reads the answer; it does not require exact format, so a minor deviation does not lose the ticket.
- Summary: whitespace collapsed to one line and cut to 120 characters (cut, not ellipsis): the agents' ticket list shows one line of that width. Tight. Whether it is one sentence is not checked: only the prompt asks for it.
- Empty or missing summary falls back to the subject: the list still shows something readable.
- Enterprise tier raises urgency one level, capped at `urgent`: contractual promise of a faster answer; the model is never told the tier, so the rule lives only in code. Tight. Only the exact value `enterprise` triggers it; other or unknown tiers are treated as non-enterprise, and tier values are not validated.
- `respond_within_hours` is a fixed table (`low` 72, `normal` 24, `high` 8, `urgent` 1): response-time promise to customers, derived from the final urgency, never from the model. Tight.
- Model is called exactly once per ticket, with no retry and no timeout: keeps cost and latency predictable; a bad answer falls back instead of re-asking.
- The model's answer is not length-limited before parsing: all lines are read, so a long answer costs parsing time only.

## Budget
- Budget: 1 model call per ticket, no retries; body capped at 2000 characters of prompt (context and cost, may be raised); no timeout or cost limit is set in code.
