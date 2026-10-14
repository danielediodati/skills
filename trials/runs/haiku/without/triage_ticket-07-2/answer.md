The enterprise bump was the cause, and it's fixed. Enterprise tickets no longer raise urgency, so the invoice copy now comes back as a normal request with an 8-hour target and no page. The checkout outage stays urgent and pages. All 13 tests pass.

**What changed in `seam.py`:**
- **Urgency describes the problem only.** The one-level enterprise raise is gone. A routine enterprise request keeps its own urgency.
- **Enterprise gets a faster target instead.** The response windows are 24, 8, 4 and 1 hours for low, normal, high and urgent. Free and Pro keep 72, 24, 8 and 1. Urgent stays at one hour for everyone.
- **New `page_on_call` field.** It is `True` only when urgency is `urgent`, for any tier. Your pager can key off this field.
- **The prompt now defines urgent.** It means the customer cannot use the product or take payments right now with no workaround. Document requests, how-to questions and account changes are never urgent.

I updated `test.py` and `README.md` to match. The old enterprise test pinned the bump, so I replaced it.

**Decisions for you:**
- The enterprise windows (24/8/4/1) are my placeholders. Set them to what your contracts promise.
- Urgency still comes from the model, so the prompt definition matters. Spot-check a week of tickets and watch for real outages marked as anything below urgent.
- The invoice request has a Friday deadline that the triage doesn't capture. A `needed_by` field, taken from the ticket or entered by the customer, would let agents sort by deadline as well as by urgency. I didn't add it, since it needs a decision on where the date comes from.