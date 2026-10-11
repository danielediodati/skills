A ticket the model didn't validly classify now comes out with `null` for the missing field instead of a default, so you can tell it apart from a genuine `general` / `normal` verdict. All 12 tests pass.

**What changed in `seam.py`**
- A queue or urgency the model didn't give as a valid value is `None`, not `general` / `normal`.
- Each field is judged on its own. A valid queue with a garbled urgency keeps its queue.
- `respond_within_hours` is `None` when the urgency is `None`, so no promised answer time appears for an unclassified ticket.
- The enterprise one-level raise is skipped when urgency is `None`.
- The summary still falls back to the subject, as the charter says.

I also updated the tests and the README for the new behaviour. The charter already specified this and noted that the code didn't do it yet, so I didn't touch it.

**What you'll see in the list**
- Last Tuesday's "Help!!" ticket would show as queue `null`, urgency `null`, no deadline, instead of looking like a calm general ticket.
- A real general ticket with a short subject shows `general` / `normal` / 24h.

**Still to do on your side**
- The ticket list needs to render `null` visibly, for example as "Unclassified", and sort those tickets first. That code isn't in this repository.
- Any downstream code that assumes `queue` and `urgency` are always strings, or that uses `respond_within_hours` as a number, must handle `None`.

**One limit**
This only catches tickets where the model's answer was unusable. If the model confidently answers `general` / `normal` for a ticket like the warehouse one, that is a judgement call and it will look like any other general ticket. Improving that means changing the prompt's criteria, which the charter leaves open if you want to pursue it.