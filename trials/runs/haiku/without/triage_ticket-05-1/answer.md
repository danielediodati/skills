Tickets that didn't get a real verdict from the model are now marked with `judged: False`, so your agents can sort or filter on that flag. All 15 tests pass.

**What changed in `seam.py`:**
- `triage_ticket` returns a new `judged` field.
- `judged` is `True` only when the model's answer contains a valid queue and a valid urgency. A real `general` / `normal` verdict gets `True`, so it stays distinguishable from a fallback.
- `judged` is `False` when the answer is unusable, a queue or urgency is outside the allowed lists, or either field is missing. The `general` / `normal` fallback still happens, but it's now visible.
- I replaced the `_choice` helper with `_clean`, which returns the valid value or an empty string, and the defaults are applied after the check.

**Tests (`test.py`):** the existing tests now expect `judged`, and I added cases for a real general/normal verdict, an invalid queue, an invalid urgency, and a missing urgency.

**README:** documents the new field.

**What this doesn't cover:**
- **The ticket list is outside this repo.** The flag only helps once the list shows it, for example as a badge or a sort to the top. Whoever owns the list needs to read `judged` from the triage result.
- **Existing tickets have no flag.** Tickets triaged before this change won't have `judged`, so the "Help!!" ticket from last Tuesday can't be identified from this change alone. You could re-run triage on the backlog, or treat a missing flag as unjudged.
- **Confident wrong answers aren't caught.** If the model returns a valid but wrong `general` / `normal`, `judged` is `True`. The flag only separates "no verdict" from "some verdict."
- **The summary fallback isn't flagged.** When the summary is missing, it's replaced by the subject line, which is the "Help!!" pattern you saw. `judged` doesn't track that. If you want the summary fallback flagged too, I can add it.