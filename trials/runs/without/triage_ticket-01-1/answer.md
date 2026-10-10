Triage now ignores quoted earlier messages, whether they sit above or below the new text. All 16 tests pass, including 5 new ones.

**What changed in `seam.py`**
- Before the prompt is built, `_strip_quoted` removes:
  - lines starting with `>` (nested quotes too);
  - the `On … wrote:` attribution line, including when it wraps onto two lines, plus a few other-language equivalents (`ha scritto:`, `a écrit:`, `schrieb:`);
  - everything after a `-----Original Message-----`, `-----Forwarded message-----` or long `____` separator, which covers Outlook-style quoting.
- The 2000-character cap now applies to the stripped text. Before, sixty quoted lines could use up the cap and push the new text out entirely.
- If stripping leaves nothing (a body that is only quoted or forwarded), the original body is sent, so the model still has something to work with.
- The empty-ticket check still runs on the raw body, so it behaves as before.

**New tests in `test.py`**
- quote above the new text, using your crash example;
- quote below the new text, with a wrapped attribution line;
- an Original Message block;
- a long quote that must not push the new text past the cap;
- a body that is only quoted.

**Limits**
- Quoting that is neither `>`-prefixed nor behind a recognised separator isn't caught. An example is a client that pastes the old mail inline with only a `From: … Sent: …` header block.
- The subject (`Re: Charged twice`) is still sent as written. It is the customer's current subject line, but it can still nudge the model toward billing. I left it alone since you only mentioned the body; say if you want a `Re:` prefix stripped or the subject down-weighted.