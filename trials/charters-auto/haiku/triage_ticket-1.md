# triage_ticket charter

Input: a ticket dict with "subject", "body" and optional "tier" ("free", "pro", "enterprise"), plus a model callable (prompt string in, string out).
Output: a dict with "queue", "urgency", "summary" (one line, at most 120 chars) and "respond_within_hours".

## Free
- Queue choice: the model reads the ticket and picks the queue, because routing needs the meaning of the text, which no rule can read.
- Urgency choice: the model judges how urgent the ticket is from its wording, for the same reason as the queue.
- Summary wording: the model writes the one sentence saying what the customer needs; code cannot paraphrase a request.

## Constrained
- Prompt wording and the two closed lists (queues, urgencies) are sent to the model: they fix the answer vocabulary, so the model's judgement lands on a value code can route on.
- Ticket is refused before any model call when subject and body are both empty (after strip): raising `ValueError` costs nothing, while asking the model about nothing wastes a call and yields a meaningless route. Tests pin this.
- Body is cut to the first 2000 chars before it reaches the model (`MAX_BODY_CHARS`): a size cap on context and cost, so long bodies cannot blow up a call. Tests pin it. Tight-ish: a budget that can be raised, not a rule about content; the tail is never seen.
- Subject is not cut: it is short by convention and is also the summary fallback.
- Field lines are parsed by code: only lines starting with `queue`, `urgency` or `summary` (ignoring leading/trailing non-word characters, case-insensitive) count; the first occurrence wins. Reason: code must find the three values in a model answer that may be decorated (bold, bullets, backticks), and the first-wins rule keeps a repeated or echoed line from overriding the first answer.
- Value cleanup: surrounding spaces, dots, asterisks, backticks, quotes are stripped and the value is lowercased before matching. Reason: tolerates decoration without accepting new words.
- Queue must be exactly one of the five queues; no synonyms or fuzzy match ("refunds" becomes `general`, not `billing`). Reason: a closed list keeps routing predictable and checkable; the cost is that near-miss answers fall to `general`.
- Queue fallback is `general` when the value is missing or not in the list. Reason: a ticket with no clear queue should land in the catch-all, where a person will look.
- Urgency must be exactly one of `low`, `normal`, `high`, `urgent`; no fuzzy match. Same reason as queue.
- Urgency fallback is `normal` when missing or invalid. Reason: an unknown urgency should not be promoted or demoted; `normal` is the middle default and the 24-hour promise. This value is a choice made in code, not a measured optimum.
- Enterprise raises urgency exactly one level, capped at `urgent`: the contract promises a faster answer, which is a business rule the model must not decide. Tier match is exact and case-sensitive (`"Enterprise"` is not enterprise); no other tier changes anything. Tier is never shown to the model.
- Respond-within-hours is a fixed table (`low` 72, `normal` 24, `high` 8, `urgent` 1): the promised deadline is a service rule, so it is set by code from the final urgency, after the enterprise raise.
- Summary: the model's text is whitespace-collapsed to one line and cut to 120 chars (`MAX_SUMMARY_CHARS`). Reason: the agents' list shows one short line per ticket. Note: the cut is hard, with no ellipsis, and sentence count is not checked (only the prompt asks for one sentence).
- Summary fallback is the stripped subject when the model gives no summary; the subject is cut to the same 120 chars. Known gap: a body-only ticket with no usable summary gets an empty summary, because there is no subject to fall back on.
- Model failures (exceptions from the callable) are not caught: they propagate to the caller. Reason: no fallback routing is invented when the model did not answer at all; the caller decides. Note: an answer that parses to nothing is different and falls back as above.
- Whole-answer fallback: a reply with no usable fields gives `general`, `normal`, the subject as summary and the 24-hour deadline (pinned by tests). Reason: the ticket still gets routed to a person without a model retry.

## Budget
- Budget: exactly one model call per ticket, no retry, no second pass; body sent at most 2000 chars; summary at most 120 chars. No time limit or cost limit is set in code. Of these, the one-call rule and the body cap are the constraints most likely to be relied on; the 2000 and 120 values are current choices that may be raised.
