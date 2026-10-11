Summaries are now shortened at sentence or word boundaries and marked with `…` when cut. The final test run was blocked, so the last fix to the new tests is unverified.

**What changed** (`seam.py`, new `_fit`):
- **Fits in 120 characters:** the summary is left as is.
- **Too long, but leading sentences fit:** it keeps the whole sentences that fit, then `…`.
- **No sentence fits:** it cuts at the last space, drops trailing punctuation, and adds `…`.
- **A single word longer than the limit:** it is cut hard and marked.
- **Length:** the `…` counts toward the 120 characters, so the list space is unchanged.

The first example from the ticket would now end in "…cancel the…" or "…design team…", never in "rem".

**Charter:** the 120-character one-line cap is a constraint held in code, and I only changed how the code shortens. I did not ask the model to write shorter summaries, and I did not touch the charter. What the summary says is still the model's.

**Tests and docs:**
- `test.py`: I replaced the old test that expected a mid-word cut, and added tests for word-boundary cutting, sentence preference, hard-cut of one long word, and untouched short summaries.
- `README.md`: the `summary` bullet now describes the cutting rule.

**Verification:** the first run passed 14 of 15 tests. The failure was my own test text being too short to need cutting. I lengthened it, but my attempt to re-run `python -m unittest` was denied, so please run it once from the project directory.