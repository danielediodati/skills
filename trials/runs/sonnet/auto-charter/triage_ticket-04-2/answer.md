I raised the body limit from 2000 to 12000 characters (`MAX_BODY_CHARS` in `seam.py`). The tests pass, including a new one for your overcharge case: a long quoted thread followed by the real request.

**What was wrong:** only the first 2000 characters of the body reached the model. Your Pro customer's 1,480 EUR message came after about three pages of quoted thread, so the model saw only the delivery-address history. It had no way of routing the ticket to billing.

**What this fixes:** the cap now covers roughly 12,000 characters, so a typical quoted thread or pasted log plus the question below it is read in full. This is the budget the charter marks as adjustable. I didn't touch the model's decisions on queue, urgency or summary, or any of the code-enforced rules.

**What it doesn't fix:**
- **Very long tickets:** anything past 12,000 characters is still cut off from the end, so a request buried under a huge log can still be missed. I can't make that fully reliable by raising a number.
- **Cost:** prompts for long tickets are up to about six times larger, so cost and latency go up on exactly those tickets.
- **Charter text:** `evals/triage_ticket/charter.md` still says "first 2000 characters". I'm not allowed to edit it, so that line is now stale and you'll need to update it.

**Your call:** the more robust fix is to send the beginning and the end of long bodies, since the request is usually at one end or the other. That changes what the charter describes ("only the first N characters"), so I haven't done it. If you want it, say so and update the charter wording.