Summaries are now shortened without ever ending mid-word, and a shortened one always ends with `...`. All 12 tests pass.

The change is a new `_shorten` in `seam.py`, applied where the summary used to be sliced at 120 characters:

- **Fits in 120:** the summary is returned unchanged.
- **Too long, and the leading sentences fit:** it keeps as many whole sentences as fit and appends ` ...`. For example, `Customer wants to keep three seats. ...`.
- **Too long, and the first sentence alone doesn't fit:** it cuts at the last whole word and appends `...`. Trailing punctuation before the marker is dropped.
- **A single word longer than the limit:** it is hard-cut, since there is no word boundary to use.
- **Limit:** the `...` counts toward the 120, so the list column is unchanged.

Two things to be aware of:

- **Your first example still reads as "keep the subscription".** A single long sentence can only be cut at a word boundary, so it becomes "…but wants to cancel the...". The `...` now signals there is more, but the text can still be misleading. If you want to avoid that, the better fix is to ask the model for a shorter summary in the prompt (for example "under 100 characters") so truncation rarely happens. I haven't changed the prompt.
- **Sentence splitting is simple.** It splits after `.`, `!` or `?` followed by whitespace, so an abbreviation like "e.g." can end a "sentence" early.

I also changed the old test that expected a mid-word cut, added tests for the new behaviours, and described the rule in the README.