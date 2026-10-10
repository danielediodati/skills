Summaries are now shortened at a word boundary and marked with `…`, but I couldn't run the tests. The command to run them was denied approval in this session, so none of this has been executed.

**What changed in `seam.py`**
- A summary that already fits in 120 characters is left alone.
- When it's too long, whole leading sentences are kept if they fit, followed by ` …`. The two example tickets would show complete first sentences instead of a fragment.
- If not even the first sentence fits, it is cut at the last whole word and `…` is added directly after it.
- The `…` counts toward the 120 characters, so the list column width doesn't change.
- A single word longer than the space is still hard-cut and marked, since there is no word boundary to use.

**Tests and docs**
- I added four tests in `test.py`: a short summary is untouched, a long one is cut at a word and marked, whole sentences are preferred, and the existing cap test now also checks for `…`.
- I updated the `summary` line in `README.md` to describe the new behaviour.

**Things to know**
- Sentence splitting is by `.`, `!` or `?` followed by whitespace, so an abbreviation like "e.g. " can end a sentence early. That only makes the kept part shorter; it never cuts a word.
- `…` is a non-ASCII character. If the ticket list can't display it, change `ELLIPSIS` at the top of `seam.py` to `"..."`.

Please run `python -m unittest` in that directory to confirm.