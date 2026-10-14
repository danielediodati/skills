Owners named in the notes now stay on the item, including people who weren't at the meeting. For your 3 March notes, "Approve the budget" comes out as Marta Olsen's, due 10 March.

The bug was in `seam.py`: any owner not on the attendee list was replaced with `None`, so Marta's name was thrown away. Now:

- **Named owners are kept.** An attendee is returned as you spelled them. Anyone else is returned as the notes wrote the name.
- **`None` means nobody is named.** Placeholders such as `none`, `nobody`, `TBC`, `TBA` and `unknown` produce `None`, so the items you need to chase stay distinguishable from assigned ones.
- **The prompt asks for absent owners.** It now tells the model to name someone even if they weren't at the meeting, and to write `none` only when the notes don't say who took the task.
- **Duplicates are matched on owner case-insensitively**, so `Marta Olsen` and `marta olsen` on the same task appear once.

I updated the one test that asserted the old behaviour, added tests for the new cases, and updated the README. All 20 tests pass. I also replayed your meeting case with a stub model that returns the line you'd expect, and the item came out with owner `Marta Olsen`.

I haven't run it against a real model, so the result still depends on the model writing "Marta Olsen" in the owner field. The code can't make it do that.

The list you send out is built by whatever tool called this module. The repo doesn't include that formatter, so if it prints owners only for attendees, that code will need the same change. Nothing has been committed, and this folder isn't a git repository.

One option I didn't add: a flag on each item marking the owner as absent, so the list could read "Marta Olsen (not at meeting)". I can add that if you want it.