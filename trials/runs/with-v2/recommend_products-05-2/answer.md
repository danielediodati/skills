I changed the prompt in `seam.py` so the model knows the limit. The tests pass, but I haven't run it against a real model, so I can't yet confirm the cut-offs are gone.

**Cause:** the model was never told the reason had to fit in 80 characters. It wrote natural-length sentences and the code chopped them at character 80, which is why they stop mid-word.

**Fix:** the prompt now says each reason must be a complete sentence of at most 80 characters, that anything longer gets cut off, and that it should say less rather than run long. The limit comes from `MAX_REASON_CHARS`, so the prompt and the cut can't drift apart. The space under the product is unchanged.

**What this doesn't guarantee:** the charter fixes the reason as "cut to 80 characters" with one model call and no retry, so the cut stays as a safety net. If the model still overruns, a reason can still be trimmed. Every guarantee I can offer within the charter depends on the model following the instruction.

Closing that gap in code would mean one of these, and each moves a line that only you can change:
- Allow a retry, or a second call to shorten any reason that comes back too long.
- Drop or blank any reason over 80 characters instead of cutting it. That would show no reason rather than a broken one, and the charter currently says the right product with a reason beats a missing one.

I'd watch real output for a while first. If cut-offs still show up, the retry is the option that actually delivers "every reason is complete".