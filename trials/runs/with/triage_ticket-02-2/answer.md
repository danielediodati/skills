Each result now says which of queue, urgency and summary is a stand-in, and all 13 tests pass.

## What changed

**`seam.py`**
- A queue or urgency the model didn't give validly is now `None`, not `general` or `normal`.
- `respond_within_hours` is `None` when the urgency is `None`.
- An enterprise ticket with a `None` urgency stays `None`.
- When the model gives no summary, the subject is used as before, but it is now flagged. If the subject is empty too, the summary is `None`.
- The result has a new `stand_ins` list, e.g. `["queue", "urgency", "summary"]`. It is empty when all three fields are the model's own.

**`test.py` and `README.md`** are updated to match.

## What this does for your example

"Parcel arrived smashed" would now come back with `queue: None`, `urgency: None` and `stand_ins: ["queue", "urgency", "summary"]`. The opening-hours ticket has `stand_ins: []`. Showing a "check me" marker whenever `stand_ins` is non-empty is enough.

## Things to know

- **This is a breaking change for anything reading the result.** Queue and urgency can now be `null`, so consumers that assumed a string, such as the ticket list or any routing on `general`, need to handle that.
- **The charter already asked for the `null`.** `evals/triage_ticket/charter.md` says a field not given validly is `null`, never a default, and marks that as "not yet in code". I brought the code in line with it, so the charter is unchanged.
- **`stand_ins` is new and not in the charter.** It only reports; it doesn't change any decision. The charter's line on the summary ("the subject when the model gives none") is respected; it's just flagged now. You may want to add a line about `stand_ins` to the charter.
- **Line endings:** the files use CRLF and I preserved that.