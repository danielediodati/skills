Summaries now never end mid-word, and any that had to be shortened end with `…`. All 15 tests pass.

The change is in `seam.py`, in a new `_shorten` helper. The 120-character limit still includes the `…`.

- **Fits:** the summary is returned untouched, with no marker.
- **Too long, first sentence(s) fit:** only the whole leading sentences are kept, followed by `…`. A fragment of the next sentence is never shown.
- **Too long, first sentence alone doesn't fit:** it is cut at the last whole word that fits (trailing `, ; : -` removed) and `…` is added. Your first example now ends "…wants to cancel the…" rather than "…the rem".
- **One unbroken string longer than the limit:** it is hard-cut and marked, since there is no word boundary to use.

The old test `test_summary_is_one_line_and_capped` assumed a plain 120-character slice, so I replaced it with tests for the cases above. The README's description of `summary` now mentions the shortening and the marker.

The shortened summary can be well under 120 characters when the first sentence is just under the limit and the second doesn't fit. I read that as what you asked for, but say so if you'd rather fill the space with part of the next sentence.