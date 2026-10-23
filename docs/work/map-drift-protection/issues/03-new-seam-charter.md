# How a seam created during development gets its charter

Type: grilling
Status: open
Blocked by: nothing

## Question

`setup` lists the seams once, and the rule sends the agent to a charter before it changes a seam, not when it creates one. A project with `extract_invoice` and its charter gets, two months later, a request for an email summary of the invoice: the agent adds a `summarize_invoice` prompt, a new seam with no charter, and the next request on it has no line to hold. Who writes that charter, and when: the rule at creation, `edd`, `setup` run again, or something else?
