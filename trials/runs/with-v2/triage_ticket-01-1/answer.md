Quoted earlier messages are now stripped from the body before the model sees it, so the triage judges only what the customer wrote this time. All 12 tests pass, including a new one for your crash-on-login example.

**What changed**
- **`seam.py`:** a new `_without_quotes` step removes every line starting with `>` and the `On <date>, <name> wrote:` line that introduces it (also when wrapped over two lines). It does this wherever the quote sits, above or below the new text. The 2000-character cap is applied after the stripping.
- **`test.py`:** new test covering the quoted block above and below the new text, with a 60-line quote like the one in your example.

**Why it was misrouted**
- **Quote dominance:** the sixty quoted lines were the bulk of what the model read.
- **Cap cutoff:** they also consumed the 2000-character cap, so the new text could be cut off entirely.

**Charter and open points**
- **Charter:** the charter is untouched. The queue, urgency and summary are still entirely the model's call; this only changes which text it is given.
- **Edge case:** a reply that is nothing but quoted text reaches the model with just the subject.
- **Not covered:** quotes that don't use `>`, such as Outlook's "From: … Sent: …" header blocks. Tell me if your customers' mail programs produce those and I can extend the stripping.
- **Pre-existing mismatch:** unrelated to this request, `seam.py` still defaults invalid answers to `general` and `normal`, while the charter says they should be `null` and marks that as "not yet in code". I left it alone.