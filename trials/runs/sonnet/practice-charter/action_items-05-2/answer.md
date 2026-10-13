The list can no longer be cut without telling you, but it still holds at most 10 items, so on its own it would still show you ten of your fourteen. Getting all fourteen into the list needs a decision from you, described below. All 19 tests pass.

**What was happening:** the tool never told the model about the 10-item limit. It sorted items by deadline with undated ones last and then kept the first ten. In a long meeting with more than ten follow-ups, the undated ones (the venue contract, the legal question) were cut, with no count and no warning.

**What I changed in `seam.py`:**
- `extract_action_items` now emits a `UserWarning` whenever the cap cuts anything. It gives the number of items left out and their tasks, so a caller that surfaces warnings can show you what was dropped.
- A new `extract_with_omitted(...)` returns `(kept, omitted)`. `kept` is exactly what `extract_action_items` returns, and `omitted` holds the items that did not fit, so a caller can show all fourteen.
- Tests cover both, plus the case where nothing is cut and no warning appears.

**What I didn't change:** the 10-item cap itself. The charter lists it as a constrained decision, with the reason that consumers need a bounded list. Raising it, removing it, or asking the model to choose which items to keep would move that line, and only you can do that.

**Decision for you:** the cap is what drops your four items. Raising `MAX_ITEMS` (or lifting the cap for the sent-round list) would give you all fourteen, at the cost of the charter's promise of a bounded list for downstream tools. The alternative is to keep the cap and have the notes tool show the omitted items under the list, using `extract_with_omitted`. You'd need to update the charter and README either way; I left both untouched.

The README still says "at most 10". It also doesn't mention the new function or the warning, since I didn't want to edit docs that restate the charter without your say-so.