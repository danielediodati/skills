Reasons in the strip no longer get cut mid-sentence. The 16 unit tests pass.

The cause was in `seam.py`: the reason was sliced to 80 characters with no regard for sentence boundaries, and the prompt never told the model about the limit. I made two changes:

- **Prompt:** the model is now asked for "a single complete sentence of at most 80 characters", so most reasons should fit without any trimming.
- **Fallback:** if a reason is still over 80 characters, only its leading whole sentences that fit are kept. If no whole sentence fits, the reason is empty.

Choices I made that you may want to change:
- When nothing fits, I show no reason rather than a shorter fragment. That keeps every visible reason complete, but a product can end up with no line under it.
- The Pico example's point ("a good backup") would be lost in the fallback if the model's sentence is too long. The better fix is the prompt change, which should stop that happening in the first place. I haven't run this against the real model, so I can't confirm how often the model stays under 80.

Files changed:
- `seam.py`: prompt update, new `_whole_sentences` helper, and the reason is now built with it.
- `test.py`: replaced the old test that asserted the 80-character hard cut. Added tests for keeping whole sentences, dropping a reason with no whole sentence, and a long sentence never being cut mid-word.
- `README.md`: describes the new behaviour.

The directory isn't a git repo, so I haven't committed anything.