Long tickets now keep their start and their end, so a request under quoted history or a pasted log reaches the model. All 12 tests pass, but I haven't run this against a real model.

**Cause:** `triage_ticket` sent only `body[:2000]`. In your example the three pages of quoted thread filled that limit, so the model never saw the 1,480 EUR message and routed on the address text.

**Changes**
- **Body trimming (`seam.py`):** bodies over 2000 characters now keep the first 600 and the last 1400 characters, with a marker where the middle was dropped. The end gets more room because that is where the customer's own message usually sits. The start is kept for customers who put the ask first and the log after. Bodies under 2000 characters are unchanged.
- **Prompt (`seam.py`):** it now tells the model to route on what the customer is asking wherever it appears, and not to route on quoted or older topics.
- **Tests (`test.py`):** I replaced the test that required the tail to be dropped with two new ones. One checks that a short body is sent whole. The other checks that a long body keeps its start and a request at the very end, and stays within the size cap.
- **Docs (`README.md`):** I documented the new behaviour.

**Limits**
- A request buried in the middle of a very long message (over 2000 characters) is still cut. In your three examples it would be at the end, but a story with the ask in a middle paragraph would still be missed.
- A tail-heavy cut can still be dominated by a long signature or legal footer. Stripping quoted lines (`>` prefixes, "On … wrote:" blocks) before trimming would stretch the window further, but email clients quote differently enough that I left it out.
- The 2000-character cap is unchanged. If your model handles more, raising `MAX_BODY_CHARS` and `BODY_HEAD_CHARS` is the simplest way to cover more cases.