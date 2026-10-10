Replies are now triaged on the new text only. All 15 tests pass, including four new ones.

**What changed in `seam.py`**
- A new `_strip_quoted()` removes the quoted history from the body before the prompt is built.
- It drops `>` lines at any depth, and the `On … wrote:` line that introduces them, including when it wraps onto two lines. It also recognises the Italian `Il … ha scritto:`.
- It cuts everything after an `-----Original Message-----` or `-----Forwarded message-----` separator, or a line of underscores. Outlook-style replies put the history there without `>` markers.
- The new text can sit above or below the quote.
- Stripping happens before the 2000-character cut. Before, sixty quoted lines could fill the whole window and push the customer's new text out of what the model saw.

**Tests added in `test.py`**
- Quote above the new text, using your example shape (60 `>` lines).
- Quote below the new text, with a wrapped attribution.
- Original Message separator.
- A very long quote that must not push the new text out.

**Things to know**
- **Quote-only replies:** if the body is only quoted text and the subject is non-empty, the ticket is triaged on the subject alone. If both are empty after stripping, it raises `ValueError`, the same as an empty ticket.
- **Subject lines:** the subject of a reply is usually still the old thread's (`Re: Charged twice`). It is sent to the model and is the summary fallback, so it can still pull a reply toward the old topic. I left it alone. If you see that in practice, we could tell the prompt that subject may be stale on `Re:` tickets.
- **Other mail clients:** the localized headers and `From:/Sent:` blocks that other clients insert are not covered beyond the cases above.
- **Scratch file:** `<work>\fix_triage.py` is a leftover helper of mine. The delete was blocked by the approval policy, so you can remove it.