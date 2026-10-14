# skills
Skills for disciplined agentic engineering of AI systems.

## Does a charter keep a coding agent from moving decisions silently?

For Sonnet 5.5, the protocol's rule says yes. On sixteen requests that describe only a problem, three runs each, Sonnet moved a decision between the model and code without saying so in **32 of 48 trials** with no charter (67%, 95% CI 53-78%) and in **2 of 48** with one (4%, 1-14%).

The charter was the one the plugin ships: written by Sonnet from the seam's code, read by nobody. The judge, Opus 5.5, held each change against the line the user drew, which no agent saw.

**What it costs: stops.** With the charter, the agent stopped in 24 of 48 trials, 10 of them with no change at all, and asked the user. Some of those stops are on changes the user wants, because a charter written from the code states today's behaviour as wanted.

**The judge is uncalibrated:** the user agreed with it on 4 of 8 trials chosen where it was most likely wrong. The counts use the user's verdicts where they were given; with the judge's own, the charter's count is 5 of 48 (5-22%), and the result is the same.

Haiku 5.5 is still to run. Synthetic seams, one file each. The protocol: [`trials/protocol-silent-drift-3.md`](trials/protocol-silent-drift-3.md); the results: [`trials/results-silent-drift-3.md`](trials/results-silent-drift-3.md).
