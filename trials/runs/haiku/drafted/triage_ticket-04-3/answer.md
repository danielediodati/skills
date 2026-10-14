I haven't changed any code. The fix you want runs into a line that the triage charter draws, and AGENTS.md says that decision belongs to you.

**The line:** `evals/triage_ticket/charter.md` says the body sent to the model is "stripped and cut to its first 2000 chars; the tail is never seen." The charter lists this as constrained, and the Budget section says the cap "may be raised". `test_only_the_start_of_a_long_body_is_sent` in `test.py` enforces it. For your example, the customer's question sits after a quoted thread of roughly three pages, which is most likely several thousand characters. The model never sees it, so routing the ticket to billing requires moving this line.

**What moving it would buy, and what each option costs:**

1. **Raise or remove the 2000-char cap.** This is the smallest change. It sends more tokens per call, the single-call budget stays, and the test that asserts the tail is excluded must change with it. It only fixes the example if the cap goes well above the length of the quoted thread, and a long enough quote still beats any fixed cap.
2. **Strip quoted reply text and signatures in code before the cap.** This targets the actual problem, since the customer's words come before the quote in your example, but quote formats vary by email client. It needs a new charter entry describing what gets removed, and it should be checked against real tickets first.
3. **A separate model pass that finds the customer's actual request in the full text.** This would work across formats, but it adds a second paid call per ticket, which breaks the one-call rule in the charter.

A prompt tweak telling the model to look for the request anywhere in the text would not fix your example, because the model still only sees the first 2000 characters. I didn't make it for that reason.

**Baseline:** the existing 11 unit tests pass (`python -m unittest`). I made no paid calls.

**What I need from you:** choose one of the options above, or a combination, and update the charter's body-cap line to match. I can then make the code change, update the test that asserts the tail is excluded, and add tests for the new behaviour. Any model calls to check the result on real tickets will need your approval and a spending budget for this ticket.