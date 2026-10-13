The list can no longer be shortened silently. The 19 tests pass, including two new ones.

**Cause:** `extract_action_items` caps the list at 10 after sorting by deadline, so undated items are cut first. That matches your four missing items: "Renew the venue contract" and "Ask legal about the new supplier terms" were found and then discarded with no trace.

**What I changed:**
- The result is still a normal list of at most 10 items. It now also has a `.dropped` attribute holding every item the cap cut, in order.
- So after the planning day you would have all fourteen: ten in the list and four in `items.dropped`.
- `README.md` now says to check `items.dropped` and tell readers when the list was shortened, for example "10 of 14 shown".

**What I left alone:**
- The cap of 10, the sort, and the cut-after-sort rule are as the charter has them, and I did not edit the charter.
- The model's choices about what counts as an item, who owns it and what the deadline is are untouched.

**Still needed:** `.dropped` only helps if the tool that builds the message you send round reads it. That code isn't in this directory, so wherever the list is rendered it needs to show a "shortened" note and the dropped items.

**Your call:** raising `MAX_ITEMS` would make a 14-item day fit outright. The charter allows it, as a tunable budget. However, its Output line says "at most 10", so that text would need updating, and only you can change the charter. Any fixed cap will still cut a big enough meeting, which is why I made the cut visible first.