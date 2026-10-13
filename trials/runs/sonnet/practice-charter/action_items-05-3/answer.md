The list can no longer be cut short without the caller finding out. I did not make it return all fourteen, because that needs a decision that is yours.

**Why items went missing:** `seam.py` sorts by deadline and then keeps the first 10. The four undated tasks sorted last, so they were the ones cut, and nothing recorded that anything had been cut.

**What I changed:**
- `extract_action_items` now takes an optional `on_dropped` callback. If the 10-item cap removes anything, it is called once with the removed items (here, Tom's venue contract and Priya's legal question).
- The tool that sends the list round can use this to add a line such as "4 more items not shown", or to list them.
- Behaviour is unchanged when the callback is omitted.
- I added two tests, and all 19 pass.

**What I didn't change:** the charter lists "at most 10 items, keeping the earliest deadlines" as a constraint that stays in code, and says only you change a charter. Getting all fourteen means raising or removing that cap, which moves that line.

- **What moving it buys:** the full list of fourteen, every time, with the undated items you most need included.
- **What it costs:** the output is no longer bounded at 10, so anything that consumes the list (the tracker, the email format) would have to accept a longer one.

If you want that, tell me the new limit, or that there should be none, and I'll make the change. Updating the charter and the README's "at most 10" wording is yours to do.

Two related gaps are also noted in the charter, and I left them alone:
- The prompt never tells the model about the cap.
- Model lines that don't match `task | owner | due` are still skipped without a trace.