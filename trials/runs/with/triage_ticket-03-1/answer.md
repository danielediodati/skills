Summaries over 120 characters are no longer cut mid-word, and a shortened one now ends with `…`. All 15 tests pass.

The cut happens in code, in a new `_shorten` in `seam.py`, so the model still writes the summary freely and the 120-character cap stays a code constraint. The marker counts toward the 120.

- **Fits:** a summary of 120 characters or fewer is left untouched.
- **Too long, several sentences:** the leading whole sentences that fit are kept, followed by `…`, instead of a fragment of the next sentence.
- **Too long, first sentence alone doesn't fit:** it is cut at the last whole word and ends with `…`. A single unbroken run with no spaces is hard-cut at 119 characters plus `…`.

I also updated the charter's summary rule and `README.md` to describe this, and added tests for each case. Your first example now reads "…wants to cancel the…" cut at a word instead of "rem", and its tail is marked so the agent knows to open the ticket.

Sentence splitting is a simple "`.`, `!` or `?` followed by whitespace" rule. An abbreviation such as "approx. 3 seats" could be treated as a sentence end, which only means the kept prefix is shorter than it could have been.

I rewrote the old `test_summary_is_one_line_and_capped` test. It asserted a hard cut in the middle of a run of `c`s, which is exactly the behaviour you asked to remove.