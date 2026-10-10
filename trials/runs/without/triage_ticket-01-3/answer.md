Triage now judges only what the customer wrote this time. All 14 tests pass: the 11 existing ones plus 3 new ones.

**What changed in `seam.py`**
- **Quoted text removed:** before the prompt is built, the body is stripped of earlier messages. This happens before the 2000-character cap, so sixty quoted lines can no longer push the new text out of the prompt.
- **What counts as quoted:**
  - lines starting with `>`, including nested `> >`;
  - the `On … wrote:` line above a quote, including when it wraps onto two lines (English, Italian, French, German and Spanish forms);
  - everything after a `-----Original Message-----` separator.
- **Position doesn't matter:** this works whether the quote is above or below the new text. Unquoted text between quoted blocks is kept.
- **Prompt:** I added a line telling the model the subject (`Re: Charged twice`) may belong to the old conversation and that the body is what to judge.
- **Quotes only:** if a reply contains only quoted text, the model gets the subject alone. With no subject either, the original body is sent rather than the ticket being refused.

**Limits**
- Outlook-style replies that quote with a `From: … Sent: …` header block and no `>` or separator line are not detected.
- Plain-text replies with no markers at all can't be told apart from new text.
- The subject is still sent to the model and is still the fallback summary, so a very old subject can influence the result.

My first edit attempt garbled both files through shell escaping. I rewrote `seam.py` in full and fixed the test block, and the passing run above is on the rewritten files. The README is unchanged.