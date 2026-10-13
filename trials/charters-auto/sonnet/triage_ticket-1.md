# triage_ticket charter

Input: a ticket (`subject`, `body`, optional `tier`) and a model callable (prompt string in, string out).
Output: a dict with `queue`, `urgency`, `summary` (one line, at most 120 chars) and `respond_within_hours`.

## Free
- Which queue the ticket belongs to: reading the customer's words and picking the topic is a judgement on unstructured text; code cannot do it by rule.
- How urgent the ticket is on its own merits (low/normal/high/urgent): tone, impact and stakes vary per ticket; the model judges the base level before any tier adjustment.
- What the summary says: the wording of the one-sentence "what the customer needs" is the model's; code only shapes it (one line, length cap) and never checks its content.

## Constrained
- Allowed queues (`billing`, `technical`, `account`, `shipping`, `general`): a closed list in code, so downstream routing never meets an unknown queue. Today's list is a product decision, not a budget; changing it changes routing.
- Allowed urgencies (`low`, `normal`, `high`, `urgent`): a closed list in code, so every urgency maps to a deadline.
- Anything outside the lists, or a missing field, becomes `general` / `normal`: a safe neutral default instead of an error, so a bad answer never blocks a ticket. Matching only tolerates case, markdown decoration and trailing punctuation (`**Queue:** Billing.`); no other fuzzy matching (synonyms like "refunds" or "asap" are not rescued).
- Answer format (three `field: value` lines, first occurrence of a field wins): parsed by code with a tolerant regex; the model does not choose the output structure.
- Enterprise tier raises urgency one level, capped at `urgent`: a contractual promise, applied by code after the model's answer so the model cannot skip or double it. Only the exact tier `enterprise` counts; `free`, `pro`, missing or unknown tiers get no change. It applies also to a fallback `normal` (so it becomes `high`).
- Deadline hours (`low` 72, `normal` 24, `high` 8, `urgent` 1): fixed table in code, derived only from the final urgency; the model never proposes a deadline. These are service-level values, not a tunable budget.
- Summary shaping: whitespace collapsed to a single line, hard-cut at 120 characters (no ellipsis), because the agents' list shows one line. A missing or empty summary falls back to the ticket subject (which can be empty if the ticket has only a body). The 120 is a display limit, the cut is not model-aware.
- Empty ticket (no subject and no body after stripping) raises `ValueError` before any model call: nothing to judge, and it saves a call.
- Input sent to the model: subject whole, body cut to the first 2000 characters. The cap bounds prompt size and cost; the tail of a long body is never seen by the model. 2000 is today's value of a context budget and may be raised; the tier is not sent to the model.
- Model failures are not handled: one call, no retry, and an exception from the model propagates to the caller. Nothing validates that the summary is faithful to the ticket.

## Budget
- Budget: exactly one model call per ticket, no retries or follow-up calls; prompt carries at most the subject plus 2000 body characters; nothing else is bounded (no timeout in this code).
