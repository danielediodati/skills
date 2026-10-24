# The plugin's regression set

Type: grilling
Status: open
Blocked by: 01

## Question

Measuring a few changed lines of the rule took `asked-move` a protocol written from scratch, 30 runs, about $24 and three usage windows. The plugin could be measured the way `edd` measures a seam: one fixed set of cases written once (REPS's cases and the synthetic seams, each with its rubric), a reference outcome per case, and one command that runs the set against a commit, a cheap core first and the extended set only if the core passes; a new protocol only for a new question, never for a change to the rule. Which cases go in the core and which in the extended set, on which models and how many repetitions, what counts as holding against the reference (and whether a stop the request did not need counts against it: today a stop on an episode counts as a hold), and where the set lives?
