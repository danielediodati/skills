# triage_ticket charter

Input: a support ticket (`subject`, `body`, optional `tier` of free/pro/enterprise) and a model callable (prompt string in, string out).
Output: dict with `queue`, `urgency`, `summary` (one line, at most 120 chars) and `respond_within_hours`.

## Free
- Which queue the ticket belongs to: reading free text and judging what it is about is what the model is for; code only checks the answer against the list.
- How urgent the ticket is on its own merits (before any tier raise): the cues are in the wording and context of the ticket, and no rule in code could list them.
- What the summary says and how it is phrased: the prompt asks only for "one sentence saying what the customer needs"; wording is the model's, code only cleans and caps it.

## Constrained
- Empty ticket (no subject and no body after stripping) raises `ValueError` before any model call: there is nothing to judge, and a call would cost money for a made-up answer. Hard rule.
- Queue is one of `billing`, `technical`, `account`, `shipping`, `general`: downstream routing needs a closed set. Changing the list is a routing change for the desk, not a tuning.
- Urgency is one of `low`, `normal`, `high`, `urgent`: the deadline table only knows these four. Closed set.
- Any queue outside the list becomes `general`, any urgency outside it becomes `normal`, each field on its own: an unusable answer must still produce a routable ticket and must never raise. The defaults are fixed choices (a safe middle), not model judgement.
- Enterprise tier raises urgency one level, capped at `urgent`, applied after the model's answer: it is a contractual promise, so the model must not be able to skip it or be asked to apply it. Tier is never shown to the model. Free and pro get no change.
- `respond_within_hours` comes from a fixed table (low 72, normal 24, high 8, urgent 1) computed from the final urgency: it is a service commitment, never model output. The numbers are policy, not a tunable budget.
- Answer format is three lines `queue:`, `urgency:`, `summary:`; the parser tolerates decoration (bullets, bold, backticks, case, trailing dot), takes the first occurrence of each field, and ignores everything else: this makes the answer cheap to check and tolerant of chatty models. Values are matched exactly after stripping, with no fuzzy matching or synonyms.
- Missing summary falls back to the ticket subject (empty if no subject): the agent list must never show a blank line.
- Summary is whitespace-collapsed to a single line and cut at 120 characters: it is shown in the agents' list, which has a fixed width. The cut is hard, with no second model call to shorten it. 120 is a display limit, tied to the list.
- Only the first 2000 characters of the body are sent to the model: bounds cost and latency, and the start of a ticket carries the request. The 2000 is a budget that may be raised; it is not a rule about meaning. The subject is sent whole.
- One model call per ticket, with no retry, no repair call and no second opinion: an unusable answer takes the defaults above instead.

## Budget
- Budget: one model call per ticket; at most 2000 body characters plus the subject and a short fixed prompt in the context; no other cost. 2000 is today's value of a budget, 120 and the hour table are product limits.
