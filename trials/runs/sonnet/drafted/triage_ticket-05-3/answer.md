Each triaged ticket now carries a `defaulted` field that lists which of `queue`, `urgency` and `summary` fell back to a fixed default instead of coming from the model. All 14 unit tests pass (local only, no paid calls).

- **Real verdict:** `defaulted` is `[]`, even if the model genuinely said general/normal. A short-subject ticket that was truly judged general is not flagged.
- **No verdict:** a ticket that looks like your "Help!!" case has `defaulted` set to `["queue", "urgency", "summary"]`. The list shows the three fields that came from fallbacks, and a person can open that ticket straight away.
- **Enterprise raise:** a defaulted urgency stays flagged after the enterprise raise, so the raise doesn't hide it.

**What changed**
- **`seam.py`:** records which fields took a default.
- **`test.py`:** adds coverage for the new field.
- **`README.md`:** documents the field.

The queue, urgency and summary values, the defaults, the deadline table and the one-call-no-retry rule are exactly as before. No charter line moved, and I didn't touch the charter.

**What you need to do**
- **Show the flag in the ticket list:** that list is outside this repo. Whatever renders it needs to show or sort on a non-empty `defaulted`.
- **Charter wording:** its Output line still lists four keys. It's yours to update if you want the new field recorded there.

**Limit**
- **Wrong verdicts aren't flagged:** the flag catches tickets where the model's answer was unusable. If the model read a ticket and wrongly answered "general, normal", that is a judgment error and looks like a real verdict. I can't detect that without moving a charter line.
- **Next step if "Help!!" was one of those:** if you can share the raw model answer for that ticket, we can tell which case it was. Checking against real tickets would be a paid run, so I'd agree a budget with you first.