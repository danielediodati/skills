# triage_ticket charter

Input: a ticket dict (`subject`, `body`, optional `tier`: free, pro or enterprise) and a model callable (prompt string in, string out).
Output: a dict with `queue`, `urgency`, `summary` and `respond_within_hours`.

## Free
- Which queue the ticket belongs to: reading the customer's free text and judging what it is about is the work the model is there for; code cannot match unforeseen phrasings.
- How urgent the ticket is on its own merits (before any tier uplift): urgency is a judgement of tone, impact and context in the text; keyword rules would misfire.
- What the summary says: the wording of the one-sentence statement of what the customer needs is the model's, because only a reading of the ticket can produce it. Code only bounds its shape.

## Constrained
- Queue is one of `billing`, `technical`, `account`, `shipping`, `general`: the closed list is the desk's real routing targets; a free-form queue could not be routed. It is a business constraint, not a budget. Adding a queue means changing the list and the prompt together.
- Urgency is one of `low`, `normal`, `high`, `urgent`: the list is closed because the deadline table is keyed on it. Fixed.
- Anything off-list (or missing, or unparsable) becomes `general` / `normal`; no retry, no repair, no second model call: a bad answer must still route somewhere cheaply and predictably, and `general`/`normal` is the neutral default that sends no ticket to a specialist queue or an urgent deadline by accident. Fallback values are a policy choice.
- Answer format is three `field: value` lines, parsed leniently in code (case, markdown decoration, bullets, trailing punctuation and quotes tolerated; first occurrence of a field wins): the model is not trusted to follow the format exactly, and code absorbs the noise instead of failing. Leniency stops at matching the allowed values: no fuzzy matching or synonyms (`asap` is not `urgent`).
- Enterprise tier raises urgency one level, capped at `urgent`, applied after the model's judgement and in code only: it is a contractual promise, so the model must not be able to waive or vary it, and the tier is not shown to the model. Free and pro are never adjusted. Fixed by contract.
- `respond_within_hours` comes from a fixed table (low 72, normal 24, high 8, urgent 1), computed from the final urgency (after uplift): these are service-level commitments, never the model's to state. The numbers are the desk's SLA values.
- Summary is whitespace-collapsed to a single line, truncated to 120 characters, and falls back to the subject when the model gives none: the ticket list display needs one short line and never an empty one. 120 is a display limit, not a quality target.
- Empty ticket (no subject and no body after stripping) raises `ValueError` before any model call: there is nothing to judge, so no cost is spent and the caller must handle it explicitly rather than receive an invented routing.
- Only the first 2000 characters of the body reach the model: bounds prompt cost and latency; the start of a ticket usually carries the request. This number is a budget that can be raised, at the cost of more context; content beyond it is invisible to the model today.
- One model call per ticket, with a fixed prompt and the answer-format instruction (exactly three lines) owned by code: keeps cost and latency flat and the result checkable. The model is never given tools, history, or tier.

## Target and budget
- Budget: one model call per ticket; body truncated at 2000 characters (adjustable); summary at 120 characters (display limit); no retries.
- Target: a valid, routable result for every non-empty ticket, whatever the model returns; the model's judgement shapes queue, urgency and summary, never the structure, deadlines or tier policy.
