I changed the urgency wording in the triage prompt. The unit tests pass, but I have not checked the change against the real model.

**What changed:** `seam.py` now defines the four urgency levels for the model:
- **urgent:** something is broken for the customer right now (payments failing, nobody can log in, data lost).
- **high:** the customer is losing money or work, but the service still runs (a wrong charge).
- **normal:** routine requests (a document copy, a how-to question, adding a user). A deadline in the ticket does not by itself make it urgent or high.
- **low:** no time pressure.

Under the existing enterprise rule, a model answer of `normal` becomes `high` (8 hours) for enterprise, so the August invoice request would move ahead of ordinary tickets without reaching the urgent list. The checkout outage stays `urgent` (1 hour). The `.format()` braces, the three-line answer shape and the closed lists are unchanged.

**What I did not change:**
- **Enterprise rule:** the one-level bump is code-owned and written in the charter as a constrained decision, so I left it alone. Changing it, for example to cap enterprise at `high`, would move a line that only you can move.
- **Charter:** I did not edit `evals/triage_ticket/charter.md`.
- **Paid calls:** I made none. Nothing shows whether the model will now rate invoice copies `normal`. That needs a small eval on sample tickets, such as the invoice and the checkout outage. That run costs money, so I need a spending budget for the ticket and your approval before running it.

**Decision for you:** if the model still rates the invoice `high`, enterprise routine requests will still land in urgent. The fix then is either a sharper prompt, or a change to the enterprise rule, which is your call.