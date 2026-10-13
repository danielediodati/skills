I made only part of the fix, because the rest needs a charter line moved and that decision is yours. Your Pro-plan ticket would still be misrouted.

**What I changed**
- **Prompt (`seam.py`):** it now tells the model to route and summarise on what the customer is asking for, wherever in the message it appears. It also says quoted earlier messages, pasted logs and backstory often come first, and the request is often last. This is context for the model's judgement; it doesn't dictate any answer.
- **Test (`test.py`):** I added a test that the prompt carries this guidance. All 12 tests pass.

This helps tickets that fit within the 2000-character window but bury the ask at the bottom. It does nothing for the case you described.

**Why your ticket still fails:** the body sent to the model is cut at 2000 characters, head only, and the charter lists that as a constraint. Three pages of quoted thread use up the whole window, so the model never sees the line about the 1,480 EUR charge. No prompt wording can fix that.

**The line, and what moving it would buy:** "Body sent to the model is cut at 2000 characters, head only." Two ways to move it:
1. **Head plus tail within the same 2000 characters** (for example the first 500 and the last 1500). This keeps the budget and the one-call rule. It would catch the quoted-thread and log-then-question cases, but not a request buried in the middle.
2. **A larger window, or a window that skips quoted text.** This catches more but costs more per ticket, and quote-stripping is a heuristic in code deciding what counts as the customer's words.

I'd recommend option 1. If you want it, update the charter and I'll implement it.