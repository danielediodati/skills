Reasons in the strip are now either a complete sentence or blank, never a cut-off fragment. All 16 tests pass.

**Cause:** `seam.py` cut every reason at 80 characters with a plain slice (`[:MAX_REASON_CHARS]`), so it stopped wherever the 80th character happened to fall.

**Changes:**
- **`seam.py`, prompt:** the model is now asked for "one complete sentence of at most 70 characters", leaving headroom under the 80 cap so most reasons fit without trimming.
- **`seam.py`, `_complete_reason`:** a reason that fits is returned as is. A longer one is cut back to the last whole sentence that fits within 80 characters. If no whole sentence fits, the reason is empty. The empty case was already allowed by the existing tests.
- **`test.py`:** replaced the old test that asserted the mid-word cap with tests for the new behaviour: whitespace clean-up, cutting back to whole sentences, empty when no sentence fits, and the 80-character limit.
- **`README.md`:** documents the new reason contract.

**Limits:**
- If the model writes a single long sentence over 80 characters, the product gets no reason at all. That's a blank line rather than a broken one, and the prompt change should make it rare.
- A short reason that fits but is unfinished still passes through, because the code can't tell that a reason is incomplete. The prompt change is the main defence there.

I didn't run the model, so I haven't checked how often it follows the 70-character instruction. Your two examples would both now be blank or a shorter full sentence, depending on what the model returns.