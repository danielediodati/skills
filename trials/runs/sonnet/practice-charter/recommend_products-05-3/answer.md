I made the part of the fix I could, but it doesn't fully guarantee what you asked for. Tests pass.

**What I changed**
- `seam.py`: the prompt never told the model about the 80-character limit, so it wrote freely and the code chopped the result. The prompt now says each reason must be a complete sentence of at most 80 characters, including spaces, and that it gets cut at that length. The number comes from `MAX_REASON_CHARS`.
- `test.py`: one new test checks that the prompt states the limit.

This should make most reasons arrive complete and within the space you already have. The wording and angle stay with the model, as the charter says.

**What I can't guarantee**
The charter makes the cut a fixed rule in code: whitespace collapsed, cut at 80 characters, "mid-word, with no ellipsis". If the model overruns anyway, which models do when counting characters, the code will still cut it mid-word. Making every reason complete would move that line, and only you can decide to do that. The options:

1. **Cut at the last word boundary.** No broken words, but the sentence can still end abruptly, like your Pico example.
2. **Drop reasons that don't fit.** The product is shown with an empty reason, which the charter already allows for a pick with no reason. Every reason shown is then whole, but some products show no reason.
3. **Ask the model to rewrite a reason that's too long.** This gives complete reasons, but it breaks the "one model call per search, no retries" budget.

Option 2 matches your goal most directly. If you want one of these, change the charter's "Reason length and shape" entry and I'll implement it.