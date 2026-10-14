Tickets now carry a `judged` flag, so you can tell a real General/normal verdict from a ticket that got the fallback. All 16 local tests pass. I made no paid model calls.

**What changed**
- `seam.py`: `triage_ticket` returns a fifth key, `judged`. It is `True` only when the model returned a valid queue, a valid urgency and a summary. If any of those is missing or invalid, it is `False`. Routing is unchanged: the same fallbacks to `general`, `normal` and the subject still apply.
- `test.py`: the two exact-dict tests now include `judged`. I added five tests covering genuine verdicts, invalid queue, invalid urgency, missing summary, and the enterprise raise.
- `README.md`: documents the new key.

**What it can and can't catch**
- Your Tuesday ticket: the summary repeating the subject suggests the model's summary line was missing or unusable. If so, that ticket now gets `judged: False`. I can't confirm that from here since I don't have the ticket or the raw model reply.
- It won't catch a model that writes a complete, valid answer that is simply wrong, such as `queue: general`, `urgency: normal`, `summary: Help!!`. That ticket would still show `judged: True`. Catching that needs a different check, and it would be a judgement about the model's output, not a fallback signal.
- Tickets already in the list don't have the flag. It only appears on tickets triaged after this change.

**Charter note**
`evals/triage_ticket/charter.md` still lists the four output keys. It is now out of date because it doesn't mention `judged`. AGENTS.md says only you change a charter, so I left it alone. You may want to add a line saying `judged` is an output that reports whether the model's answer was usable.