I made a partial change. The prompt now tells the model that a customer's current request can come after quoted earlier messages or a pasted log. I did not fix the core problem, because the constraint that causes it is in the charter and only you can change that.

**What's stuck:** the body is cut to its first 2000 characters before it reaches the model (`seam.py`, the `body[:MAX_BODY_CHARS]` line). The charter lists that cut under Constrained, so changing it moves a line. Your example, three pages of quoted thread before the new message, is almost certainly past 2000 characters. The model never sees the 1,480 EUR complaint, so the prompt change alone will not reroute that ticket.

**Options, each of which moves the line:**
- **Strip quoted reply text before the cut.** This would most likely fix the email-client case, since quoted blocks are usually marked with `>` or an "On … wrote:" line. It changes what the charter describes as "the first 2000 characters of body", and it would need a new test in place of `test_only_the_start_of_a_long_body_is_sent`.
- **Raise the cap.** The charter says the number "may be raised", but a three-page thread can still exceed any reasonable cap, so this only shifts the problem.
- **Send the head and the tail of long bodies.** This catches a question at the end of a long log, but it still has to be weighed against the cost budget.

**What I changed:** one paragraph in the prompt in `seam.py`, which is a criterion for the model's judgement and so sits in the free part of the charter. I did not touch the charter file.

**Verification:** the 11 existing unit tests pass before and after the change. I made no model calls, so the new prompt has not been tested against real tickets. The repo isn't a git repository, so there is no commit.

If you want the example ticket to reach billing, tell me which option to take, and I'll make the change and add tests for it. Any run that calls a model will need your approval and a budget first.