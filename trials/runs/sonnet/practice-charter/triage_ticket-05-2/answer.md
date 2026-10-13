`triage_ticket` now says whether the model actually judged a ticket, so the list can flag the ones it didn't. All 13 tests pass.

**What changed**

The result dict has two new keys:
- `judged`: `True` only when the model gave a usable queue, urgency and summary.
- `fallback`: the fields that code had to default, from `queue`, `urgency` and `summary`. It is empty when `judged` is `True`.

Your "Help!!" ticket would have come back as `queue: general`, `urgency: normal`, `summary: "Help!!"`, `judged: False` and `fallback: ["queue", "urgency", "summary"]`.

A ticket the model really judged as general and normal comes back with `judged: True`, so the two kinds are now distinguishable. If only one field was defaulted, `fallback` names it (for example `["queue"]`).

**Limits**

- **List display:** the ticket list isn't in this repo, so it still has to show or sort on `judged`. Filtering on `judged == False` and putting those first is what gets a person onto them straight away.
- **Summary check:** a model that really answered and happened to echo the subject still counts as judged. Only an empty or missing summary counts as defaulted.
- **Charter and policy:** I left the charter unedited, as the rules require, so its "Not yet in code" line on this item is now out of date; that edit is yours to make. The change doesn't touch the SLA mapping, the tier raise, the one-call-per-ticket rule or the model's free decisions.

I also updated `README.md` and the existing test expectations in `test.py`, and added two tests for the new fields.