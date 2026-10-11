Each triaged ticket now says whether it got a real verdict, so the ticket list can flag the ones that didn't. All 13 tests pass.

**Cause.** When the model's answer was missing or unusable, `triage_ticket` quietly filled in `general`, `normal`, and the subject line as the summary. The result looked the same as a ticket the model really judged general and normal. That is why your "Help!!" ticket looked like a low-stakes ticket.

**Change (`seam.py`).** The result has two new keys. The existing keys and values are unchanged.
- `defaulted`: the fields that fell back to a default, from `queue`, `urgency` and `summary`. It is an empty list when the model answered everything usably.
- `needs_review`: `True` when `defaulted` is not empty.

A ticket the model really judged `general` / `normal` has `needs_review: False`. One that arrived with no usable verdict has `needs_review: True`.

**Tests and README.** I updated the existing tests to expect the new keys and added two: a real general/normal verdict is not flagged, and a missing summary is flagged. The README documents both keys.

**Your side.** Whatever builds the agents' ticket list needs to show `needs_review`, for example a badge or sorting those tickets to the top. That code isn't in this folder, so I haven't touched it.

**One decision for you.** A missing summary alone also sets `needs_review`. I chose that because the subject-as-summary look is exactly what hid your ticket, and `defaulted` lets you tell it apart from a missing queue or urgency. If it produces too much noise, change the flag to depend only on `queue` and `urgency`. That is a one-line edit in `seam.py`.

**Not covered.** This catches answers that were unusable. It doesn't catch a model that confidently says "general / normal" for a ticket that isn't. That would need a different check, such as scanning for urgency words in the body.