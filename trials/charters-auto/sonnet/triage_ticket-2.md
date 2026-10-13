# triage_ticket charter

Input: a ticket dict (`subject`, `body`, optional `tier`) and a model callable (prompt string in, string out).
Output: dict with `queue`, `urgency`, `summary`, `respond_within_hours`, shown to agents and used to route the ticket before a person opens it.

## Free
- Which queue fits the ticket: needs reading the customer's words, which code cannot do; code only checks the answer against the list.
- How urgent the ticket is, before the tier adjustment: a judgement of tone, impact and stakes in free text; code only maps the label to a deadline.
- What the summary says and how it is worded: the prompt asks for one sentence on what the customer needs; the content is the model's, code only shapes the form.
- How to read an ambiguous, mixed or odd ticket: the model picks one queue and one urgency for it, with no rule in code for ties.

## Constrained
- Whether the ticket is processed at all: a ticket with no subject and no body (after strip) raises `ValueError` before any model call; no cost spent on nothing to triage.
- Allowed queues: closed list `billing, technical, account, shipping, general`; downstream routing needs a known value. Anything else becomes `general`. The list is a contract with the support desk, not a tuning value.
- Allowed urgencies: closed list `low, normal, high, urgent`; anything else becomes `normal`. Queue and urgency fall back independently, so one bad field does not discard the other.
- Parsing of the answer: line-based `queue:/urgency:/summary:` fields, tolerant of markdown, bullets, case, and trailing punctuation or quotes; first occurrence of a field wins. Tolerance is deliberate (test covers decorated answers); the model is not asked for JSON and no retry is made on a malformed answer.
- Enterprise tier raises urgency one level, capped at `urgent`: a contractual promise, not a judgement, so the model must not decide it. It applies after the fallback, so an enterprise ticket with an unusable urgency ends at `high`. Only the exact value `enterprise` triggers it; `free`, `pro`, missing or unknown tiers get no change. The model is not told the tier.
- Response deadline: fixed table `low 72h, normal 24h, high 8h, urgent 1h`, derived from the final (post-tier) urgency in code. These are service-level numbers, not model output; the table is the constraint itself.
- Summary form: whitespace collapsed to a single line and hard-cut at 120 characters (may cut mid-word), because the agents' list has a fixed width. The 120 is a display limit.
- Summary fallback: if the model gives no summary, the stripped subject is used (cut to 120 too). It can be empty only if the subject is empty and the model gave nothing.
- Context sent to the model: subject whole, body cut to the first 2000 characters (`MAX_BODY_CHARS`); bounds cost and latency, on the bet that the start of a ticket carries the request. Today's value of a budget that could be raised; the tail is never seen by the model.
- Prompt shape: the fixed instruction with the allowed lists filled in from the same constants used to validate, so prompt and checks cannot drift.
- Number of model calls: exactly one per ticket, no retry, no second opinion. Model exceptions are not caught and reach the caller.

## Budget
- Budget: one model call per ticket; prompt holds at most the subject plus 2000 body characters plus the fixed instruction. No timeout, retry or cost cap in code. The 2000-character cut is a raisable budget; the 120-character summary cap, the lists and the hour table are contracts.
