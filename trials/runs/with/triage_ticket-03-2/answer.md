Summaries longer than 120 characters are now shortened in code, never mid-word, and always end in `…`. All 14 tests pass.

**Behaviour** (`_shorten` in `seam.py`):
- A summary of 120 characters or fewer is left untouched.
- Otherwise, whole leading sentences are kept if they fit, followed by ` …`.
- If not even the first sentence fits, it is cut at the last whole word that fits, trailing punctuation is dropped, and `…` is appended.
- A single unbroken run with no spaces (for example a long URL) is hard-cut, since there is no word boundary to use.
- The 120-character limit still holds, counting the `…`.

Your first example would now read "…the design team but wants to cancel the…", so the cut is visible.

**Decision for you: charter wording.** I kept the shortening in code rather than asking the model to write shorter, so what the summary says stays the model's decision. I added one clause to the "Constrained" summary bullet in `evals/triage_ticket/charter.md` describing the new rule, and a note in `README.md`. Please review the charter wording, since you own that line.

**Tests:** I added tests for word-boundary cuts, whole-sentence preference and untouched short summaries. I also changed `test_summary_is_one_line_and_capped` to expect "at most 120 characters ending in `…`" instead of exactly 120, since the cut now stops at a word.

**Environment:** the directory is not a git repo, so nothing is committed.