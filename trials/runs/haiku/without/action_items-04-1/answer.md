Owners now resolve from first names, nicknames, and "Ana R."-style forms, so the venue and badge tasks from your 3 March notes would come out with Tom Becker and Priya Raman. All 22 tests pass (17 existing, 5 new).

The cause was an exact-match lookup: an owner was kept only if it matched a full attendee name, so "Tom" or "Priya" became `None`. I changed two things in `seam.py`:

- **Prompt:** the model is now asked to give the full name from the attendee list, and to map first names, nicknames and short forms onto it.
- **Code:** `_resolve_owner` does the same mapping on whatever the model returns, so it doesn't depend on the model following the prompt. An owner still has to be one of the attendees.

The matching rules, in order:

1. Exact full name, or a surname (with or without an initial). "Becker", "Ana R." and "Tom Becker" all resolve.
2. First names match exactly before any nickname matching is tried. "Tom" goes to Tom Becker even when a "Tomas" is also in the meeting.
3. Nicknames match when one name is a prefix of the other and the shorter is at least 3 letters. "Tommy" resolves to Tom Becker.
4. If more than one attendee matches, the owner stays `None`. With Ana Ruiz and Ana Reyes both present, a bare "Ana" is not guessed.

Two things to be aware of:

- **Prefix trade-off:** if "Tom" is the only Tom-like name in the meeting and the attendee is "Tomas Lopez", the prefix rule will match it. I judged that better than leaving the task unowned. If you'd rather be strict, it's a one-line change in `_same_name`.
- **Not tested against a real model:** the tests use a fake model. The prompt change is only checked by the code fallback, which handles the cases above either way.

The changes are in `seam.py` (prompt, `_resolve_owner` and helpers) and `test.py` (new `OwnerTest` cases). This directory is not a git repository, so there is no commit.