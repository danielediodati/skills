The list is still capped at 10, but it no longer drops items silently. The four missing items now come back in a new `omitted` attribute on the returned list. All 19 tests pass.

**Cause:** `MAX_ITEMS = 10` in `seam.py`. Dated items sort first, so when a meeting has more than 10 items, the undated ones are cut. That is why Tom's venue contract and Priya's legal question went missing, and nothing recorded the cut.

**What I changed:**
- `extract_action_items` returns the same list as before, now with an `omitted` attribute holding the valid items beyond the cap, in order.
- Existing callers are unaffected, because the result is still a plain list.
- I added two tests (items omitted over the cap, none omitted under it) and a README note.

**What you or the notes tool must still do:** nothing sends this warning to you yet. Whatever renders or sends the list has to check `items.omitted` and say something like "4 more items not shown". I didn't find that code in this directory.

**Your decision:** the cap and the "dated first, undated cut" ordering are rules in code, so I left them alone. Choose one of these:
- **Raise or remove the cap.** You would get all fourteen items. The cost is a longer list, and the README promises "at most 10".
- **Keep the cap, but cut by something other than date.** Dropping undated items first is the worst order for you, since they are the ones that slip.
- **Keep it as is.** The omission is now visible, but you would still have to retrieve the missing items yourself.

Two other things are also dropped silently: lines the model writes in the wrong format, and a deadline that is invalid or before the meeting date (the item stays, with no date). I left both alone, but a malformed line is also a way an item could go missing. Tell me if you want those reported too.