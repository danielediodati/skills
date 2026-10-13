Long tickets are now read in full up to a much larger limit, and the model is told to judge on what the customer is asking for now, wherever it appears. All 12 tests pass, but I haven't run this against a real model, so I can't yet confirm the 1,480 EUR ticket lands in billing.

**Cause:** only the first 2000 characters of the body were sent to the model. Three pages of quoted thread used up that limit before the customer's actual message. The model never saw the overcharge, only the address thread.

**Changes**
- **Body limit:** `MAX_BODY_CHARS` in `seam.py` goes from 2000 to 20000. The charter names this number as an adjustable budget, so queue, urgency, summary and the single model call are untouched. Cost per ticket rises for long tickets, roughly 5k tokens at most.
- **Prompt:** it now says to judge the ticket by what the customer is asking for now, wherever it appears, including after quoted messages, pasted logs or a long story, and that it may differ from the subject or the quoted thread. This is guidance for the model's judgement, not a rule that dictates the answer.
- **Tests:**
  - The old test that checked the body was cut at 2000 characters now checks the cut at the budget.
  - A new test puts a request after a long quoted thread and checks it reaches the model.

**What this doesn't cover**
- A ticket longer than 20000 characters is still cut, so a request at the very end of a huge log can be missed. Some email clients also quote the whole thread in a way that can exceed this.
- Sending the start and the end of the body instead of a fixed head would handle those cases at a flat cost. That changes the charter's rule that only the first N characters are sent, so it is your decision. I haven't done it.
- The charter text still says 2000 characters (the Constrained section, line 20, and the Target and budget section). I can't edit it, so please update the number when you next review it.