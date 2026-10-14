Long tickets are now routed and summarised on the customer's own request, wherever it sits in the message. The 15 unit tests pass. I haven't run it against your real model or real tickets.

**What was wrong:** `seam.py` sent the model only the first 2000 characters of the body and never removed quoted history. A 3-page quoted thread pushed the customer's new message out of view, so the model only saw the old delivery-address conversation. The old test `test_only_the_start_of_a_long_body_is_sent` was checking for exactly that behaviour.

**What changed in `seam.py`:**
- **Quoted history is removed before the model sees the body.** Lines starting with `>` are dropped, along with an `On … wrote:` line and everything after an `-----Original Message-----` marker. If stripping would leave nothing, the body is sent as written.
- **Long bodies keep their end.** Above 3000 characters, the model gets the first 1000 and the last 2000, with a marker in the middle. That covers a request placed after a log or a long story.
- **The prompt tells the model** that the current request can be anywhere in the message and to route on what the customer is asking for now.

**Tests:** I replaced the head-only test and added four: a question after a long quote, text after an Original Message marker, the reply-header line being dropped, and a body that is entirely quoted. The README now describes the new behaviour.

**Choices I made that you may want to change:**
- The cut-off points are 3000 characters total, with 1000 kept from the start and 2000 from the end. These are constants at the top of `seam.py`.
- Outlook's quoted block (a `From:/Sent:/Subject:` header with no `>` prefix) is not detected, unless it sits after an "Original Message" marker. Those quotes can still reach the model.

For your Pro-plan case, the reply's new paragraph would now be the text the model reads, so the ticket should go to billing with an overcharge summary. I checked that with a fake model in the tests, not a live one. I'd suggest replaying that ticket and a few long ones through the real model before relying on it.