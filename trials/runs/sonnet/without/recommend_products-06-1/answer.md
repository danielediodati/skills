The fix is in and all 16 tests pass.

**Cause:** the model sometimes names a product without writing a reason. `seam.py` kept those picks with `reason: ""`, and the old test even asserted that behaviour. That is how the earbuds and the cable ended up as cards with a blank line.

**What changed (`seam.py`):**
- **Second ask:** if any picks come back without a reason, the model is asked once more for just those products. That prompt tells it to say how the product differs or what it is good for. A wired earbud for a "wireless headphones" search should get something like "Wired, but light and cheap".
- **Drop if still empty:** a product that still has no reason is left out. I chose this over a canned filler line, which would reintroduce the "didn't understand me" feeling.
- **Fill the strip:** the `limit` is now applied after dropping, so a dropped product makes room for the next one the model chose rather than shrinking the strip.
- **No extra cost normally:** when every pick has a reason, there is still only one model call.

**Tests and docs:**
- I replaced the test that expected an empty reason with four tests: a retry fills reasons, a still-empty pick is dropped, no retry when none are missing, and a dropped pick makes room for the next.
- The README now states that every returned product has a non-empty reason.

**Trade-offs:**
- **Extra latency:** a search where the model omits reasons now makes two model calls, so those searches take a bit longer.
- **Shorter strip:** if the retry also fails, the strip can be shorter than `limit`, and in the worst case empty.
- **Not covered:** a line where the model writes "H-200 - reason" without the `|` is still dropped, as before.