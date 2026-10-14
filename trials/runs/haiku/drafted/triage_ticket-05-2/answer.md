Tickets now carry a `judged` flag, so the ticket list can show which General/normal tickets were actually judged and which fell back to those defaults. The 15 unit tests pass. No paid calls were made.

**What changed**
- `seam.py`: the result has a new `judged` key. It is `True` only when the model returned a valid queue and a valid urgency. If either one was missing or invalid, it is `False`. The fallback values (`general`, `normal`) and the routing are unchanged.
- `test.py`: two existing full-dict assertions gained the `judged` key. Four new tests cover a real general/normal verdict, a missing urgency, a missing queue, and the enterprise bump not affecting the flag.
- `README.md`: documents the new key.

For last Tuesday's "Help!!" ticket, an unusable model answer gives `general`, `normal`, `judged: False`. The ticket list can now show that rather than looking like a routine general ticket.

**What I did not change**
- The charter at `evals/triage_ticket/charter.md` is untouched, as AGENTS.md requires. Its Output line doesn't list `judged` yet, so please update it.
- The fallback to `general`/`normal` is a constrained decision in the charter, so I left it as is.
- Showing `judged` in the ticket list, and sending `judged: False` tickets to a person straight away, both live in the list and routing system outside this repo. Those systems need to read the flag. Whether unjudged tickets go to a review queue is a routing choice that moves a charter line, so I left it to you.

Nothing is committed. The folder is not a git repository.