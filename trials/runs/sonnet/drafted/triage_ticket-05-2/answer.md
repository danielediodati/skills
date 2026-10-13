Each triaged ticket now says whether the model really judged it. All 14 tests pass; no paid model calls were made.

**What changed**
- `seam.py`: the result gets a new key, `fallbacks`. It lists which of `queue`, `urgency` and `summary` got no usable answer from the model, so a default was used.
- `test.py`: the two existing exact-dict assertions include the new key. New tests cover three cases:
  - A real `general`/`normal` from the model has an empty list.
  - Each field reports its own fallback.
  - The enterprise raise doesn't hide a fallback.
- `README.md`: documents the new field.

**How your agents use it**
- `fallbacks == []`: the model really judged the ticket, including a genuine `general`/`normal`. Treat it as ordinary.
- `fallbacks` non-empty: the ticket arrived without a real verdict, and a person should open it straight away.
- Last Tuesday's "Help!!" ticket would have come out as `["queue", "urgency", "summary"]`, which is what the fallback summary repeating the subject line implied. Your ticket list needs to show or filter on this field; I changed only the triage function, not the list UI.

**Nothing else moved**
The fallback values (`general`, `normal`, the 24h deadline), the parsing and the enterprise rule behave exactly as before. I didn't edit the charter. It describes the output as four keys, so you may want to add `fallbacks` there yourself.

**Open question**
The model is still allowed to answer `general`/`normal` for an alarming ticket like the label-printing one. That is the model's judgement, which the charter lists as free, and this change doesn't address it. If that also happens in practice, fixing it means changing how the model is prompted or constrained, which is a decision for you.