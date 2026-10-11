Summaries over 120 characters are no longer cut mid-word; the change is in `seam.py` and all 15 tests pass.

How it behaves now:
- **Fits:** a summary of 120 characters or less is left as it is.
- **Several sentences:** the leading sentences that fit whole are kept, followed by ` …`.
- **First sentence too long:** the text is cut at the last word boundary and ends with `…`.
- **No spaces:** a long unbroken string is hard-cut and ends with `…`.
- **Length:** the `…` counts toward the 120 characters, so the list space is unchanged.

Your first example would now read "The customer would like to keep the subscription for the three seats used by the design team but wants to cancel the …", assuming it is one sentence, with the cut at a word boundary and marked.

I replaced the old `test_summary_is_one_line_and_capped` in `test.py`. It asserted a raw 120-character slice, which is exactly the behaviour you asked to remove. Four new tests cover the cases above.

The charter is untouched. What the summary says is still the model's decision, and the 120-character one-line limit is still enforced in code. The change only affects how an over-long summary is shortened.