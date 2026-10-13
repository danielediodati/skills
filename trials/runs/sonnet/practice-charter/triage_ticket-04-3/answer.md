I made only part of this fix. The rest needs a decision from you, because it means moving a line in the charter.

**Why the ticket was misrouted**

`seam.py` sends the model only the first 2,000 characters of the body (`body[:MAX_BODY_CHARS]`). Three pages of quoted thread fill that budget, so the model never saw the "charged 1,480 instead of 148" paragraph. It routed the ticket on the old delivery-address thread, which is the only thing it was shown. No prompt wording can fix that, because the model can't act on text it never receives.

**What I changed**

I added a paragraph to the prompt saying the real request can appear anywhere (after a quoted thread, after a log, in the last paragraph) and that it should judge on what the customer is asking now. This only helps when the request falls inside the 2,000 characters, for example a short quoted reply or a modest log. It does not fix your example. The 11 existing tests still pass.

**The line I stopped at**

The charter lists this as constrained: "Body sent to the model is cut at 2000 characters, head only." Your request can't be met without changing that, so I left it alone and did not edit the charter. Moving it would buy this:

- **Head plus tail within the same budget:** send, say, the first ~700 and last ~1,300 characters, with a marker for the cut. The cost stays at 2,000 characters and one call. This catches the "question underneath the log" and "ask in the last paragraph" cases, and most reply-above-quote layouts. The risk is a request buried in the middle of a very long message.
- **Raise the cap:** costs more per ticket and still fails once a thread outgrows it.
- **Strip quoted text in code (`>` lines, "On … wrote:" blocks):** this keeps the head-only rule but puts code in charge of deciding what is relevant. That is the kind of keyword judgment the charter reserves for the model, and it fails on clients that don't mark quotes.

I'd recommend head plus tail. If you approve it, the charter line needs rewording to say something like "head and tail", plus the new split. I can then make the code change and add a test where the request sits after 3,000 characters of quoted text.