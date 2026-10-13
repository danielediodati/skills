# triage_ticket charter

Input: a ticket (`subject`, `body`, optional `tier` of `free`, `pro` or `enterprise`) and a model callable taking a prompt and returning text.
Output: a dict with `queue`, `urgency`, `summary` and `respond_within_hours`, always valid, or `ValueError` for an empty ticket.

## Free
- Which queue the ticket belongs in: reading what the customer needs is open-ended judgment on free text, which code cannot enumerate.
- How urgent the ticket is on its merits: weighing outage, money, deadlines and tone is judgment; code must not second-guess it with keywords.
- What the summary says: writing a one-sentence statement of the customer's need is prose the model does well.

## Constrained
- Allowed queues (`billing`, `technical`, `account`, `shipping`, `general`): the desk's routing is a fixed set that downstream systems depend on.
- Allowed urgencies (`low`, `normal`, `high`, `urgent`): a fixed scale that the deadline mapping and consumers depend on.
- Value outside the allowed list becomes `general` or `normal`: model output is untrusted, and the output must always be valid.
- Enterprise tier raises urgency one level, capped at `urgent`: this is a contractual promise, so it is code's policy, and the tier is never shown to the model to weigh.
- Urgency to `respond_within_hours` (72, 24, 8, 1): an SLA promise made to customers, fixed and auditable, never chosen by the model.
- Summary is one line, whitespace collapsed, at most 120 characters: the agents' list display needs it; code cuts it as the backstop.
- Empty summary falls back to the subject: the list must never show a blank line.
- Empty ticket (no subject and no body) is refused with `ValueError` before any model call: nothing to judge, and no call is spent.
- Body sent to the model is cut at 2000 characters, head only: context and cost are code's budget.
- Answer format of three labelled lines, and the tolerant parse of it (case, decoration, first occurrence wins): form is code's to demand and to forgive, content is checked afterwards.
- Prompt wording, with the allowed lists filled in from the code constants: the prompt and the validation must name the same sets.
- Value comes from the model, not a retry: one call per ticket, no retry on an unusable answer; the fallback is the answer.
- Caller can tell a fallback from a real model answer: Not yet in code, which returns the same dict whether the model answered or the queue and urgency were defaulted, so a ticket the model failed on looks like a judged `general`/`normal`.

## Target and budget
- Budget: one model call per ticket, at most 2000 characters of body plus the subject in the prompt; no call for an empty ticket.
