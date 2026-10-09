# triage_ticket

Used by a support desk to route each incoming ticket before a person opens it.

`triage_ticket(ticket, model)` takes a ticket (`subject`, `body` and the customer's `tier`: `free`, `pro` or `enterprise`) and a model, any callable that takes a prompt string and returns a string. The model reads the ticket and proposes a queue, an urgency and a one-sentence summary.

The function returns a dict with:

- `queue`: one of `billing`, `technical`, `account`, `shipping`, `general`
- `urgency`: one of `low`, `normal`, `high`, `urgent`; enterprise customers are raised one level
- `summary`: a single line of at most 120 characters, shown in the agents' ticket list
- `respond_within_hours`: 72, 24, 8 or 1, depending on the urgency

Anything the model answers outside these lists is replaced by `general` and `normal`. A ticket with neither subject nor body raises `ValueError`.

Run the tests with `python -m unittest` from this directory.
