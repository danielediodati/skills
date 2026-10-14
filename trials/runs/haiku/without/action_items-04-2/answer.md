Owners now resolve from first names, surnames, and initials, so "Tom" becomes Tom Becker and "Priya" becomes Priya Raman. All 24 tests pass, including new ones for those cases.

The fix is in `seam.py`. The owner check used to require the full attendee name, so anything shorter was dropped to `None`. An owner now resolves in this order:

- **Full name** (case and spacing ignored), as before.
- **Nickname**, if the caller passes the new optional `aliases` argument, e.g. `aliases={"Tom Becker": ["Tommy"]}`.
- **Partial name**: every word must match a word of one attendee's name, and a single letter counts as the start of a word. So "Tom", "Becker", "Ana R." all resolve.

An owner stays unassigned when it fits no attendee, when it fits two (for example "Ana" with both Ana Ruiz and Ana Lopez in the meeting), or when it names a group like "Ana and Tom". I chose this so a wrong owner is never filled in silently, since an unowned item is at least visible.

Things to know:

- **Nicknames need configuring.** "Tommy" resolves only if you pass the alias. Without it, that item stays unowned. Tell me if you'd rather I keep a list of nicknames somewhere the tool reads automatically.
- **The tests use a fake model.** They confirm the code handles "Tom" and "Priya" correctly, but I haven't run this against your real model, so I can't confirm it writes first names the way your notes do.
- **The README is updated** to describe the new owner rules and the `aliases` argument.

The project isn't a git repo, so I haven't committed anything.