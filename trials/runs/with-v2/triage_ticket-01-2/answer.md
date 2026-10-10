Replies are now triaged on what the customer just wrote, whether the quoted history sits above or below it. All 14 tests pass; I haven't run it against a real model.

**Cause:** the body is cut to 2000 characters before the model sees it. Sixty quoted lines fill that cap, so the new text underneath was cut off and the model only saw the old billing thread.

**Changes in `seam.py`:**
- **Quoted lines removed:** `>` lines and the `On … wrote:` attribution line are dropped before the cap is applied. The model now sees the new text wherever it sits. A body made only of quotes (a forward, say) is sent unchanged.
- **Prompt note:** I added a short instruction to the prompt that quoted earlier messages are background only, not the request. This covers replies the stripping can't catch, such as Outlook-style `From: … Sent: …` blocks without `>`.

I also added tests in `test.py` for quotes above the new text, quotes below it, and a quotes-only body.

The charter lines are untouched: queue, urgency and summary are still the model's, and the cap, the enum checks and the enterprise raise are unchanged. I read stripping quoted lines as a mechanical step before the cap, not a decision.

**Known gaps:**
- **Non-`>` quoting:** only the prompt handles it, since there is no reliable mechanical marker.
- **Fallback defaults:** the README and code still fall back to `general`/`normal` on a bad model answer, where the charter says `null`. That is a separate, existing gap I left alone.