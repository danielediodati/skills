Tests pass (13). Results now say which of queue, urgency and summary are stand-ins.

**What changed**
- **`seam.py`:** a queue or urgency the model didn't give validly is now `null` instead of `general` / `normal`. `respond_within_hours` is `null` when the urgency is `null`. Enterprise tickets keep a `null` urgency as `null`, since there is nothing to raise.
- **`stand_in`:** the result has a new list naming the fields that are not the model's judgement, e.g. `["queue", "urgency", "summary"]`. A summary that fell back to the subject is flagged too. Your "Parcel arrived smashed" ticket would now come out with `queue: null`, `urgency: null` and `stand_in: [queue, urgency, summary]`. The opening-hours ticket has an empty list, so "check me" is simply `stand_in` being non-empty.
- **`test.py`, `README.md`:** updated to match.

**Things to know**
- **Charter:** this matches `evals/triage_ticket/charter.md`, which already said a field not given validly is `null`, never a default, and that the code didn't do it yet. So the charter doesn't change.
- **Consumers:** anything reading `queue` or `urgency` must now handle `null`. The ticket list may have been filing these under "general" because of the old default, so check that it doesn't break.
- **`respond_within_hours`:** it is `null` for those tickets, so there is no promised response time until someone triages them by hand.