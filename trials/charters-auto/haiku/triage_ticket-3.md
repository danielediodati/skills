# triage_ticket charter

Input: a ticket dict with `subject`, `body` and optional `tier` (`free`, `pro`, `enterprise`), plus a `model` callable (prompt string in, string out).
Output: dict with `queue`, `urgency`, `summary` (one line, at most 120 chars), `respond_within_hours`. Raises `ValueError` if subject and body are both empty.

## Free
- Queue: the model picks one of the five queues from the ticket's meaning; no code rule can read intent as well as it can, and a wrong guess only costs a re-route.
- Urgency: the model judges how pressing the ticket is from its wording; a keyword rule would miss urgency that is stated indirectly.
- Summary wording: the model writes the one sentence saying what the customer needs; code cannot paraphrase, it can only trim the result.

## Constrained
- Prompt shape: the model is asked for exactly three `key: value` lines, with queue and urgency drawn from the closed lists; this keeps the answer parseable and the output checkable.
- Queue set (`billing, technical, account, shipping, general`): closed list, because agents' queues are fixed and an unknown queue would route nowhere.
- Urgency set (`low, normal, high, urgent`): closed list, because `respond_within_hours` is keyed on it and an unknown value would have no deadline.
- Answer parsing: only lines starting with `queue`, `urgency` or `summary` count, decoration (`**`, `-`, backticks, case) is stripped, and the first occurrence of each field wins; this tolerates model formatting noise without letting later lines override earlier ones.
- Invalid or missing queue becomes `general`; invalid or missing urgency becomes `normal`: safe defaults so every ticket still lands somewhere. Cutting these to a retry would double model calls.
- Missing summary becomes the subject: an agent always sees a line in the list.
- Enterprise tier raises urgency one level, capped at `urgent`: a contractual promise of faster answers, so code must own it. The model never sees the tier. Other tiers change nothing.
- `respond_within_hours` (urgent 1, high 8, normal 24, low 72): an SLA table, fixed in code so the promised deadline is never a model guess.
- Summary normalisation: whitespace collapsed to one line and cut at 120 chars. Constraint, not budget: it is the width of the agents' ticket list. The cut can fall mid-word.
- Body sent to the model: stripped and cut to its first 2000 chars; the tail is never seen. Context/cost cap, and may be raised if prompts allow.
- Subject: stripped but not capped before entering the prompt. Gap: a very long subject is sent in full (summary is capped later, the prompt is not). Left as is; a reader who adds a cap should know it is currently absent on purpose or by accident.
- Empty ticket (no subject and no body after stripping): refused with `ValueError` before any model call. Saves a call and an answer nobody could use.
- Allowed values are checked by code, not trusted: anything outside the lists is discarded, including case and trailing punctuation variants that are normalised first.

## Budget
- Budget: exactly one model call per ticket, no retry, no timeout in code; body capped at 2000 chars and summary at 120 chars. The one-call rule is a cost and latency choice; the 2000-char body cap is a budget that may be raised; the 120-char summary cap is a display constraint and should not be raised without checking the agents' ticket list.
