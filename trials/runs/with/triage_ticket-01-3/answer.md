Quoted earlier messages are now removed from the body before the model sees it, so the triage is based on what the customer wrote this time. All 13 tests pass, including two new ones.

**Cause:** the body was sent to the model whole, cut to 2000 characters. Sixty quoted lines fill that cap, so the new text ("the app crashes every time I log in") never reached the model. What it did see was the old billing conversation.

**Fix**, in `seam.py`:
- `_without_quoted_replies` drops every line starting with `>` and the `On <date>, <name> wrote:` line before it. It also handles that line when the mail program wraps it over two lines.
- It runs before the 2000-character cap, so quoted text cannot push the new words out.
- It works whether the quote sits above or below the new text.

**Charter:** the new step is documented in `evals/triage_ticket/charter.md` and the README. It stays on the code side of the line: code does not choose the queue, urgency or summary, it only changes which part of the body the model reads. Everything the charter lists as free is untouched.

**Tests:** `test.py` gains two cases, one with the quote above the new text (your example) and one with the quote below and a wrapped attribution line.

**Limits:**
- The detection is tied to the `>` and `On … wrote:` conventions. Outlook-style quoting (a `From: … Sent: …` header followed by unmarked text) and non-English attribution lines ("Le … a écrit :") are not caught. Say if your customers' mail programs produce those and I'll add them.
- If a reply is only quoted text, the model sees the subject alone, and the ticket is not rejected as empty.