Replies are now triaged on what the customer wrote this time, not on the thread they quoted. All 12 tests pass, including a new one for your crash-after-refund case. I ran only the tests, not a real model.

Two changes in `seam.py`:

- **Prompt:** it now says the ticket may be a reply, that quoted earlier messages (an `On … wrote:` line, `>` lines) are background, and that the model should judge what the customer wrote this time. This is criteria for the model's judgement, so queue, urgency and summary stay its decision.
- **Quoted lines dropped before the cap:** lines starting with `>` are removed from the body before it is cut to 2000 characters. Your example needed this because sixty quoted lines would have used up the cap, so the model would never have seen the new text. It also covers quotes sitting below the new text.

I read the quote-stripping as a mechanical input step rather than a change to what the model decides, so I left the charter alone. If you'd rather the model always see the raw body, the prompt note still works, but long quotes will push new text out of the 2000 characters.

Limits you should know about:

- **Attribution line:** the `On … wrote:` line itself is not stripped, because recognising it across mail programs and languages is guesswork. The model is told to ignore it.
- **Quoting styles:** replies quoted without `>` (some Outlook-style `-----Original Message-----` blocks) are not detected, so only the prompt note protects those.