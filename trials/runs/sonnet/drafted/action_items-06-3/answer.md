I changed the prompt so the model is told the weekday and given a calendar to read deadlines against. I have not run it against a real model, so I can't yet say your March 3 example now comes out right. The 18 unit tests pass, including a new one for the prompt content.

**Likely cause:** the prompt only said `2026-03-03`, so the model had to work out for itself that this was a Tuesday. That is the kind of arithmetic a model gets wrong by a day, which fits Ana's quote landing on Thursday the 5th. Spoken deadlines need that arithmetic, and dates written out do not, which matches the split you saw.

**What changed in `seam.py`:**
- The meeting date now reads `Tuesday 2026-03-03`.
- The prompt includes a calendar of the 14 days after the meeting, each with its weekday. For your meeting, Friday 6 March and Friday 13 March are listed explicitly.
- A short note on `due` says that spoken deadlines like "by Friday" or "end of next week" should be worked out from that calendar and written as a date only.

**What stays with the model:** deciding what "by Friday" and "end of next week" mean is still its call, since the charter lists the deadline's value as free. I gave it facts and a criterion, not an answer for any phrase.

**Tom's missing deadline:** I can't tell from the code whether the model wrote "none" or an unparseable value, and the cause is unconfirmed. The code drops any `due` that isn't a plain ISO date, which the charter fixes, and I left that alone. If the model replied with something like `2026-03-13 (end of next week)`, the item would end up undated. The prompt now asks for the date only, which should help.

**Next step:** a paid check of your exact notes would show whether the three dates come out as 6 March, 13 March and 10 March. I haven't started one. If you want it, tell me a budget for this ticket and which model to use, and I'll start with the cheapest.