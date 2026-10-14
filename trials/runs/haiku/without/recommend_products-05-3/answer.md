Reasons in the strip now end on a full sentence or are left empty; none are cut mid-word. All 16 tests pass.

The cut came from `seam.py`, which sliced the model's reason at 80 characters. I made three changes:

- **Prompt (`seam.py`):** the model is now told to write one complete sentence of at most 80 characters, ending with a full stop. This should stop most reasons from running long in the first place.
- **Trimming (`seam.py`):** a reason that fits is kept as is. One that is too long is cut back to its last whole sentence that fits. If no whole sentence fits, the reason is empty.
- **Tests and README:** the test that asserted a hard 80-character cut now checks the new behaviour. I added tests for a long reason with a whole sentence before the overflow, a long reason with no whole sentence, and a sentence of exactly the cap. The README describes the new rule.

The trade-off: a product whose reason can't be shortened to a whole sentence now shows no reason at all. The strip stays the same size, but some products will have a blank line where a reason used to be. If you would rather show a shorter sentence in that case, the fix is to ask the model again with a stricter limit, which means an extra model call per product.