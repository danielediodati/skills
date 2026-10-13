I've made only part of the fix, and your example ticket will still be misrouted. Fixing it fully means moving a line in the charter, which is your decision.

**What I changed**
- The prompt in `seam.py` now tells the model to route and summarise on what the customer is asking for, wherever in the message they say it, and that quoted threads, logs and background often come first. This is guidance for the model's judgment, so it stays within the charter's free decisions.
- I added a test for it in `test.py`. All 12 tests pass.
- This only helps tickets that fit in the 2000-character budget, where the model sees the ask but may be pulled toward the opening.

**The line I did not move**
The charter lists this as constrained: *"Body sent to the model is cut at 2000 characters, head only: context and cost are code's budget."*

Your ticket had about three pages of quoted thread before the new message, so the overcharge text was cut before the model saw it. No prompt wording can fix that. The model can't weigh text it never receives.

**What moving it would buy** (any of these changes the charter, which only you can do)
1. **Head and tail.** Send, for example, the first 500 and last 1500 characters. The budget and the one call per ticket stay the same, and it covers the pasted-log-then-question and story-then-ask cases. It would miss an ask buried in the middle.
2. **Raise the cap** (say to 6000–8000 characters). This is simple and covers more, but it costs more per ticket and still fails on very long threads.
3. **Strip quoted reply lines** (`>` prefixes, "On … wrote:" blocks) before the cut. This fixes your exact case but not logs or long stories, and it makes code decide which text matters.

I'd pick option 1, possibly with the head share kept small, since the ask is usually at the end or the start. Tell me which you want, update the charter's line yourself or tell me to go ahead, and I'll implement it with tests.

There's a related gap that is also listed in the charter as "not yet in code". Today a fallback `general`/`normal` can't be told apart from a judged one. That would help you spot tickets the model failed on, but it's separate from this request and I haven't touched it.