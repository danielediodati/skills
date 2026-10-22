# `edd` lets through the move the user names

Status: ready-for-agent
Blocked by: nothing

## What it produces

The `edd` skill on decision 15 in `CONTEXT.md`, as the rule `setup` writes and `charter` already have it since tickets 11.1 and 11.2:

- "Only the user changes a charter" goes from *Before the first change* and from *The diff against the charter*. A diff that edits the charter is a finding only when the line it moves is not one the user named in the request.
- In the diff check, a moved line the user named is reported as made and flagged, not as drift, and does not stop the change. A moved line nobody named still stops it, whatever the score.
- *The line holds*: "Moving the line is the user's decision" and the paragraph on a charter change decided by an eval say what the rule says: the user's request is the decision; the eval runs both versions and shows the scores beside the move, within the spending rules, without waiting for a choice.
- *When the budget is spent*: "the line moved on purpose" stays a way out put to the user, since no request named that move.

## Done when

- No sentence of `edd` contradicts the rule `setup` writes or `charter`'s *When a line moves*.
- Read on D4 and E5: on D4 the diff check reports the buttons' line as moved by the user and lets the change through; on E5 the enum written in the approved ticket is reported as drift and stops the change.
