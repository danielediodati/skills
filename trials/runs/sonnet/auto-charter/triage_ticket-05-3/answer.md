`triage_ticket` now returns a `fallback_fields` list that says which parts of the result were defaults rather than the model's answer. All 13 tests pass, including two new ones for this.

**What changed**
- `fallback_fields` is a list of `queue`, `urgency` and `summary`, naming each field the model gave no usable answer for and code defaulted.
- An empty list means the model really judged the ticket, so a real General / normal ticket shows `[]`.
- Your "Help!!" ticket would have shown `["queue", "urgency", "summary"]`, because the model's answer was unusable and the summary fell back to the subject.
- The list display can sort or highlight on `fallback_fields` being non-empty (or containing `queue` or `urgency`), so a person opens those tickets first.
- The change is in `seam.py`, with tests in `test.py` and a line in `README.md`.

**What did not change**
- The fallback behaviour is untouched: off-list or missing values still become `general` / `normal`, with no retry and no second model call.
- The model prompt, the enterprise uplift and the SLA table are also untouched.
- The model still decides queue, urgency and summary; the code only reports when it didn't get an answer.

**Limits**
- This catches tickets where the model's answer was missing or off-list. It does not catch a model that confidently answers "general / normal" for a ticket that should be urgent. That is a judgement-quality problem, and fixing it would mean changing how the model is asked.
- The charter's "Output" line lists four fields and doesn't mention `fallback_fields`. I left the charter alone since only you change it; you may want to add the field there.
- I didn't touch the ticket list itself, because that code isn't in this directory.