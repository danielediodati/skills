Long tickets now reach the model with far more of the body, but this only helps tickets under the new limit, and I haven't checked it against a real model. The 12 local tests pass; I made no paid calls.

## Cause
`seam.py` sent only `body[:2000]` to the model. In your Pro-plan ticket, the three pages of quoted delivery-address thread filled that window, so the model never saw the overcharge message below it.

## Changes
- **`seam.py`:** `MAX_BODY_CHARS` goes from 2000 to 12000. The charter lists 2000 as an adjustable budget, so this is within the model's brief. 12000 chars is roughly 3k tokens per call.
- **`seam.py` prompt:** it now says the real request can be anywhere in the message (after quoted emails, logs or a long story) and to answer on what the customer is asking now. This is guidance only; the model still decides the queue, urgency and summary.
- **`test.py`:** a new test puts a request after a long quoted thread and checks it reaches the model. The truncation test now uses the constant instead of a hard-coded 2000.

## Limits
- **Very long tickets are still cut.** A message longer than 12000 characters, such as a big error log with the question underneath, still loses its tail. Raising the number further only moves the cutoff.
- **Fixing that means moving a line.** The charter says "only the first 2000 characters are sent… the start of a ticket carries the request". Sending the end of the body as well, or having code strip quoted lines, changes which part is read. That is a charter change, so it's your decision, and I haven't touched it. It would be the only way to reliably catch the log-then-question case, at about the same cost per call.
- **The charter text is now stale.** It still says 2000 in the constraints and the Budget section. I can't edit it, so please update it to 12000 if you keep this value.
- **The model's behaviour is unmeasured.** Whether the prompt change gets your example routed to billing needs a paid eval run. I'd propose a budget for the whole ticket once you tell me roughly how many cases and which model, and I won't run anything until you approve.

If 12000 is too generous for your cost per ticket, say so and I'll lower it.