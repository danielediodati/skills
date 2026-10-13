Fixed in `seam.py`: enterprise tickets no longer get their urgency raised, so only genuinely urgent tickets reach "urgent" and page on call. All 12 tests pass.

**Cause.** `triage_ticket` bumped every enterprise ticket up one urgency level. Anything the model rated "high" became "urgent", with a one-hour deadline and a page. That is how "Copy of August invoice" ended up looking like a checkout outage.

**Change.**
- `urgency` is now the model's own judgement of the ticket, whatever the customer's tier.
- Enterprise customers get a faster deadline at the same urgency instead:

| urgency | standard | enterprise |
|---|---|---|
| low | 72h | 24h |
| normal | 24h | 8h |
| high | 8h | 4h |
| urgent | 1h | 1h |

- The invoice copy would now arrive as normal or high with an 8h or 4h deadline. It still jumps ahead of ordinary tickets, but it sits below the checkout outage and doesn't page anyone.
- Only genuinely urgent tickets get the one-hour deadline, for any tier.

**Things to check.**
- **The 4-hour value for enterprise "high" is my choice.** If your contracts name specific response times, put those in `ENTERPRISE_RESPOND_WITHIN_HOURS` in `seam.py`.
- **Your ticket list needs to sort or filter on `respond_within_hours`, not only `urgency`.** If it sorts by urgency alone, enterprise tickets won't visibly come ahead of ordinary ones.
- **The model prompt is untouched.** If it over-rates how-to questions and user additions as "urgent" on its own, that is a separate fix, and I'd want a few of your real tickets to tune it against.

I also updated `README.md` and replaced the "raised one level" test with two tests for the new behaviour.