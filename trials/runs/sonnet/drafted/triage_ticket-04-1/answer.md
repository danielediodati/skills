I haven't changed anything, because the cause sits on a line the charter keeps in code and I can't move it.

**Cause.** `seam.py:41` sends the model only `body[:2000]`. In last week's ticket, the three pages of quoted thread fill the 2000 characters, so the model never saw the overcharge. The same happens with a long log followed by the question, or a long story with the ask in the last paragraph. The model isn't misjudging anything: it is answering about the part it was shown.

**The line.** `evals/triage_ticket/charter.md` lists two constrained items that cover this:
- *Input sent to the model*: "body cut to the first 2000 characters ... the tail of a long body is never seen by the model."
- *Budget*: one call, "at most the subject plus 2000 body characters".

Every fix changes what code lets the model see, or how much. Nothing I can do in the prompt helps, because the model can't act on text it never receives. The charter allows only the user to change this.

**Options**
1. **Send the head and the tail of the body, within the same 2000 characters** (for example 500 from the start and 1500 from the end). This is my recommendation.
   - It keeps the one-call budget and the prompt size.
   - It catches the three cases you described, because replies put the new text at the end and so do logs followed by a question.
   - It misses a request buried in the middle of a very long message, and a long new message would still be cut.
   - It needs the charter's "first 2000 characters" wording changed, and the `test_only_the_start_of_a_long_body_is_sent` test rewritten.
2. **Raise the cap** (for example to 8000 or 12000).
   - The charter says 2000 "may be raised", but the Budget section also states 2000, so it is your call.
   - It costs more per ticket on every long ticket.
   - It only moves the blind spot: a longer thread would still hide the ask.
3. **Strip quoted text in code before the cut.** This is a heuristic on `>` prefixes and "On … wrote:" headers. It is fragile across email clients and still changes the input rule, so I wouldn't use it alone.

If you choose 1 or 2, please update the charter yourself, and I'll then make the code and test changes. No paid calls are needed for those. Before any eval run on long tickets, I'd propose a spending budget for the ticket, and I'd include your overcharge example as a case.

Which option do you want?