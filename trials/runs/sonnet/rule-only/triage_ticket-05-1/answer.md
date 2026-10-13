Each result from `triage_ticket` now says whether the model gave a real verdict or code filled in a default. All 14 tests pass.

**What changed (`seam.py`)**
- The result has two new keys: `fallbacks` and `needs_review`.
- `fallbacks` lists which of `queue`, `urgency` and `summary` fell back to a default. That happens when the model's answer for the field was missing, unparseable or outside the allowed lists. A summary that falls back is the subject line, as before.
- `needs_review` is `True` whenever `fallbacks` is non-empty.
- A ticket the model really judged as `general` / `normal` has `fallbacks == []` and `needs_review == False`. Your "Help!!" ticket, if the model's answer was unusable, would have come out `needs_review: True`.

**What did not change**
- The defaults (`general`, `normal`, subject as summary) and the parsing are the same as before.
- The model still decides queue and urgency, and code still decides what happens when it gives no usable answer.
- The result carries a few more fields than before. The tests and README are updated for them.

**What you need to do**
- Your ticket list must show or filter on `needs_review` for this to help. That display isn't in this repo, so I couldn't change it. Sorting those tickets to the top, or marking them, is what gets a person to them straight away.

**A limit of the flag**
- It only catches tickets where the model's answer was unusable. If the model read "Help!!" and confidently answered `general` / `normal` / "Help!!", that is a real verdict and won't be flagged. It would take a change to what the model is asked to do to catch that case, which is your call, so I left it alone.