# skills
Skills for disciplined agentic engineering of AI systems.

## Does a charter keep a coding agent from moving decisions silently?

For Sonnet 5.5 and for Haiku 5.5, each on its own, the protocol's rule says yes. On sixteen requests that describe only a problem, three runs each, the agent moved a decision between the model and code without saying so:

| agent | no charter | with a charter it drafted | judge |
| --- | --- | --- | --- |
| Sonnet 5.5 | **32 of 48** (67%, 95% CI 53-78%) | **2 of 48** (4%, 1-14%) | Opus 5.5, uncalibrated: 4 of 8 |
| Haiku 5.5 | **33 of 48** (69%, 55-80%) | **1 of 48** (2%, 0-11%) | Sonnet 5.5, calibrated: 5 of 7 |

With a charter, each agent read the one the plugin ships: written by its own model from the seam's code, read by nobody. Each judge held every change against the line the user drew, which no agent saw. **The two rows are not compared with each other:** each has its own judge and its own drafts.

**What it costs: stops.** With the charter, Sonnet stopped in 24 of 48 trials, 10 of them with no change at all, and Haiku in 34 of 48, 20 with no change. Some of those stops are on changes the user wants, because a charter written from the code states today's behaviour as wanted.

**The judges.** The user checked each judge on trials chosen where it was most likely wrong, and agreed with Opus on 4 of 8 and with Sonnet on 5 of 7. The counts use the user's verdicts where they were given. With the judges' own verdicts, the charter's counts are 5 of 48 (5-22%) for Sonnet and 0 of 48 (0-7%) for Haiku, and the result is the same.

Synthetic seams, one file each. The protocol: [`trials/protocol-silent-drift-3.md`](trials/protocol-silent-drift-3.md); the results: [`trials/results-silent-drift-3.md`](trials/results-silent-drift-3.md).
