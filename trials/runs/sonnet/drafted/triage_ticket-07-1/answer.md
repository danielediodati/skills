I've made part of the fix. The rest needs a decision from you, because it would change a rule the charter reserves for you.

## What I changed (free tests pass, no paid calls)

The prompt in `seam.py` now tells the model what each urgency level means. `urgent` is something broken right now for the customer or their users, where waiting an hour costs real damage. A deadline or a firm tone alone is not urgent. A request with a date a few days out is `high` at most, and an ordinary request is `normal`. This only informs the model's own judgement, which the charter lists as free. The tier is still not sent to the model. I added one test for that.

On its own this will not fix your problem. I haven't run it against a real model, so I can't say how much it shifts. That would be a paid eval, and I'd need your approval and a budget first.

## The line I did not move

The cause is the enterprise rule in code (`seam.py:47-50`, charter "Constrained"): enterprise raises urgency one level, capped at `urgent`. Any enterprise ticket the model rates `high`, such as the invoice copy needed before month-end, becomes `urgent`. That means a 1-hour deadline and a page. The checkout outage and the invoice copy then look identical, because the raise is applied after the model and changes the same field.

Better wording for the model can reduce how often it says `high` for routine requests. It cannot stop the rule from turning a legitimate enterprise `high` into `urgent`. Fixing that means changing the rule itself, which is a contractual promise recorded in the charter, so it is your call. Options:

1. **Cap the enterprise raise at `high`.** Enterprise `normal` becomes `high` (8h instead of 24h). `urgent` then only comes from the model judging a real emergency, and enterprise customers still get the 1-hour answer for a real outage. The cost is that an enterprise ticket the model rates `high` gets no speed-up over a Pro one. I recommend this as the smallest change that restores what `urgent` means.
2. **Keep the one-level raise but add a separate marker.** The result would carry a field such as `enterprise: true` or a distinct priority, and your list and paging would sort on it. `urgent` would still be set by the raise, so paging would need to key on something other than `urgency` to benefit. That is more work downstream.
3. **Add a new level between `high` and `urgent`**, with its own deadline (for example 4h) and no page. This changes both the urgency list and the deadline table.

Each of these edits the charter, so I haven't touched it. Tell me which one you want, or that you'd rather change the charter yourself. I'll implement the code and tests after that.