A ticket that arrives without a real verdict now shows `None` for queue and urgency, so it can no longer pass for a judged General / normal ticket. All 12 tests pass.

**What changed in `seam.py`**
- A queue or urgency the model didn't give validly is `None`. Before, it was silently replaced by `general` or `normal`, which is what made "Help!!" look judged.
- `respond_within_hours` is `None` when the urgency is `None`.
- Enterprise tickets with no urgency stay `None`. The raise only applies to a real verdict.
- Each field is handled on its own. A valid queue with an unreadable urgency keeps the queue.

**What stays the same**
- The summary still falls back to the subject line when the model gives none.
- The model's decisions are still entirely its own, and the charter is untouched.

**Tests and README**
- I rewrote the three tests that asserted the old defaults and added one for enterprise with a null urgency.
- I updated the README paragraph that described the old default behaviour.

**Your side**
Whatever renders the ticket list needs to treat `None` as "unclassified" and surface it, for example as a flagged "Needs review" row sorted to the top. That code isn't in this directory, so I haven't touched it. Until it does, a `None` may display as blank rather than as a warning.

A ticket the model genuinely judged to be general / normal still shows `general` / `normal`, so your agents can now tell the two kinds apart.