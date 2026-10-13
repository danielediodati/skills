Every ticket now carries a `fell_back` list that names the fields where the model gave no usable answer and a default was substituted. All 13 tests pass.

**What changed**
- **`seam.py`**: the result gains `fell_back`, a list drawn from `queue`, `urgency` and `summary`.
  - `queue` or `urgency` is listed when the model's value was missing or outside the allowed list, so `general` or `normal` was filled in.
  - `summary` is listed when the model gave none and the subject line was used instead.
- **`README.md`**: documents the new field.
- **`test.py`**: the two exact-match tests now include `fell_back`, and there are new cases for the single-field fallbacks.

**How it answers your question**
- **Real verdict:** a ticket the model actually judged as `general` / `normal` has `fell_back == []`.
- **No real verdict:** your "Help!!" case, where the answer was unusable and the summary repeats the subject, has `fell_back == ["queue", "urgency", "summary"]`. A person should look at it straight away.
- **Enterprise customers:** enterprise tickets are still raised one level. A fallen-back urgency is flagged even when it was bumped.

**What I didn't touch**
- The defaults, the prompt and the routing are unchanged. Which queue and urgency a ticket gets is decided exactly as before.
- I did not add any sorting, escalation or auto-urgency for flagged tickets. That would change what the seam decides, so it's your call.

**What you need to do**
The ticket list has to display or filter on `fell_back`, and that code isn't in this directory.

**A limit to know about**
This flags tickets where the model's answer was unusable. If the model returns a well-formed `general` / `normal` for a ticket that deserved better, that is a wrong judgement and it will not be flagged.