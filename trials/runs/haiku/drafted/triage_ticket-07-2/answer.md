I made the part of the fix that the charter allows, and I stopped at the enterprise bump, which I did not change. The fix is only partial until that rule is decided.

**What changed (`seam.py`)**
- The prompt now defines the four urgency levels. "Urgent" means the customer's product or service is down or broken for them now, or data or security is at risk. "High" means seriously impaired with no workaround. "Normal" covers routine requests, questions, how-tos, access changes and copies of documents, and says a deadline alone does not make a ticket urgent. "Low" means no time pressure.
- The charter lists urgency as the model's free judgement. Criteria that inform that judgement are allowed, so I did not touch the charter or the code around it.
- The 11 existing unit tests pass. The tests use a fake model, so they cannot show whether the model now judges the invoice request as normal.

**The line I did not move**
- The enterprise bump (`seam.py`, the `tier == "enterprise"` block) raises urgency one level. The charter lists it as constrained: it is the contractual faster-answer promise. So an enterprise invoice request that the model rates "high" still becomes "urgent" with a one-hour deadline. Only a model rating of "normal" lands at "high", which is an 8-hour answer.
- Moving that line would mean changing the contract rule, which is your decision. Options include: bump only from "normal" to "high" and never to "urgent"; keep "urgent" for the model's own judgement only; or map enterprise to a separate response time that is not the urgent queue. Any of these needs a charter change from you.

**Not verified against the model**
- I have not run the model. Checking whether the new criteria actually separate the invoice request from the checkout outage needs paid calls. Per the project rules I need your approval and a spending budget first. A small set of about 10 tickets through the cheapest model would be enough to see the effect. Tell me the budget if you want that run.