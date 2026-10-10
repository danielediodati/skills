The result now carries a `fallbacks` list that names which of `queue`, `urgency` and `summary` are stand-ins. All 14 tests pass.

**What changed (`seam.py`)**
- `fallbacks` is a list in the order queue, urgency, summary. It is empty when all three are the model's own judgement.
- Your "Parcel arrived smashed" ticket now comes back as `queue: general, urgency: normal, summary: <subject>, fallbacks: ["queue", "urgency", "summary"]`.
- The opening-hours ticket comes back with `fallbacks: []`. A model that answers `general` on purpose is not flagged, so you can show "check me" on `fallbacks` being non-empty and trust the rest.
- A missing summary is flagged as well as a missing or invalid queue or urgency.

**Decision for you**
- For an enterprise customer, a stand-in `normal` is still raised to `high`, and `urgency` stays in `fallbacks`. The value is partly invented, so I kept the flag.

**Other changes**
- The existing tests that compare the whole result now include `fallbacks`.
- New tests cover the cases above: deliberate `general` versus an unknown queue, a missing summary, and an enterprise ticket with a stand-in urgency.
- `README.md` documents the new field.

**Not covered**
- The summary flag only fires when the model gave no summary. A summary that merely repeats the subject is not flagged, because I can't tell that apart from a good one.
- A model answer with a valid queue but unusable urgency is flagged only on `urgency`, not on the whole ticket.