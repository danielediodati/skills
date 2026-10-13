The cause is that one field is carrying two different things: how bad the problem is, and how quickly you promised this customer an answer. Enterprise tickets get bumped into "urgent" because that is the only way the field can express "faster". The fix is to stop expressing the contract through priority.

## Split it into two dimensions

| | Set by | Drives |
|---|---|---|
| **Severity** (Urgent / High / Normal / Low) | What is broken and for whom | Paging, queue position among emergencies, the "drop everything" signal |
| **Customer tier** (Enterprise / Pro / …) | Account record, automatic | The SLA clock and sort order within a severity level |

Urgent is then defined only by impact, for example: production down or unusable for many users, checkout or payments failing, data loss or corruption, or a security incident. It does not depend on the plan.

## Make the enterprise promise a faster clock, not a higher level

| Severity | Standard SLA | Enterprise SLA |
|---|---|---|
| Urgent (outage) | 1 hour, pages on-call | 30 min, pages on-call |
| High | 8 hours | 2 hours |
| Normal | 24 hours | 8 hours |

The invoice copy becomes Normal with a 2–4 hour enterprise clock. It sits ahead of every non-enterprise Normal ticket and does not page anyone. The checkout outage is Urgent, pages, and is clearly different in the list. An enterprise customer with a real outage still gets the strictest response of anyone.

Adjust the numbers to match what the contracts actually say. The point is that every promise is expressed as a clock.

## Implementation

1. **Find the rule that bumps enterprise tickets to urgent** and remove it. Replace it with one that sets tier and attaches the tier's SLA policy.
2. **Sort the queue by time-to-breach**, not by priority label alone. Enterprise Normal tickets then rise naturally as their clock runs down.
3. **Page only on Severity = Urgent.** An SLA that is about to breach should send a warning to the desk, not a page.
4. **Show tier as a visible badge** (e.g. "ENT") next to severity, so agents see both.
5. **Make severity something an agent confirms.** A customer's self-selected "urgent" or a form default shouldn't set it. A short triage question at intake helps: "Is your service down or unusable for your users right now?"
6. **Let date-driven requests carry a due date.** "Needed for month-end close Friday" is a deadline, not an emergency. A due-date field lets the invoice request be handled in time without competing with outages.

## Rollout

- **Audit last month's urgent tickets** and label each as a real emergency or not. This gives you a baseline and a test set for the new rules. If the new rules would have classified your four missed outages as Urgent and the invoice copies as Normal, they are right.
- **Tell account managers and enterprise customers** what changed: faster response than before on routine requests, and a separate emergency lane. Frame it as a stronger commitment, not a downgrade.
- **Rebuild trust with agents.** Once urgent is clean again, say so explicitly and ask them to flag any urgent that isn't.

## What to measure

- Share of urgent tickets that are real emergencies (target: nearly all).
- One-hour (or 30-minute) response rate on real outages.
- Enterprise SLA attainment on High and Normal tickets, to show the contract promise is still being kept.
- Number of pages per week that turn out to be non-emergencies.

If you tell me which helpdesk system you use (Zendesk, Freshdesk, Jira Service Management, etc.), I can map this onto its fields, triggers and SLA policies.