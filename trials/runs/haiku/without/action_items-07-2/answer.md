Marta's name now comes through: the 3 March budget item would show as "Approve the budget", owner Marta Olsen, due 10 March. All 19 tests pass.

The cause was in `seam.py`. Any owner who wasn't in the attendee list was set to `None`, even when the notes named them. Now:

- **Attendees** are still returned with the spelling you passed in.
- **Someone who missed the meeting** is kept as owner if the notes contain their name as a whole word. So "Marta Olsen" stays, but "Tom" doesn't match "Tomas".
- **A name the notes don't contain** is still dropped to `None`. That guards against the model inventing an owner.

The prompt now asks the model to name a non-attendee owner when the notes give one, and to use "none" only when nobody is named. I updated the README and the docstring to match.

Two things to know:

- **The tests use canned model answers,** so they confirm the code handles the model's output correctly, not that the real model names Marta. Regenerate the 3 March list with the real model to check that.
- **I didn't flag absent owners separately.** Marta's name now shows, but nothing in the output distinguishes her from a present attendee. If you want that, I can add a field to `ActionItem`, which would change its constructor.