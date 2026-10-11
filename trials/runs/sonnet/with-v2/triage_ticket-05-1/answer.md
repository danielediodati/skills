Tickets the model didn't actually classify now come back with `null` instead of `general` / `normal`, so they can be told apart from tickets that were genuinely judged. All 12 tests pass.

**What changed**
- **`seam.py`:** a `queue` or `urgency` the model didn't give validly is now `None`. Before, it silently became `general` and `normal`, which is exactly what made "Help!!" look like a judged low-stakes ticket.
- **`respond_within_hours`:** it is `None` whenever the urgency is `None`. Previously it showed 24 hours.
- **Fields are independent:** a ticket with a valid urgency but an invalid queue keeps the urgency and its deadline.
- **Enterprise tier:** the one-level raise is skipped when the urgency is `None`, so there is no invented urgency to raise.
- **Summary:** it still falls back to the subject, as the charter specifies. A summary that merely repeats the subject is no longer a reliable signal on its own; the `null` queue and urgency are.
- **`test.py` and `README.md`:** updated to the new behaviour, plus a new test for enterprise with a null urgency.

**This is a charter alignment, not a line move.** The charter already said a field not given validly is `null`, "never a default", and noted this was "not yet in code". I left the charter untouched.

**What you still need to do**
- **Ticket list:** whatever renders the list has to show `null` queue/urgency visibly, for example as "Unclassified – needs review", and sort or filter those to the top. That code isn't in this directory, so I couldn't change it.
- **Default response time:** if your ticketing system needs a deadline on every ticket, give unclassified tickets a short review SLA on that side. Don't put it back in the seam as a `normal` default.