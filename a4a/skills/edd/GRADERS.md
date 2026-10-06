# Graders

A grader turns one output into pass or fail, or into a score in [0, 1] that passes at 0.5 or above. Pick the cheapest grader that can disagree with the system, climbing the ladder only when the rung below cannot express the criterion:

1. **Structural check** (deterministic): the output parses, matches a schema, calls an allowed tool with valid arguments, stays within a step or token budget, cites something that exists. Cheap and exact; often enough for tool-using agents.
2. **Execution check** (deterministic): run the output and observe the effect. Tests pass after applying a patch, a query returns the expected rows, a plan satisfies the hard constraints when checked by code. The strongest grader there is: use it whenever the output can be executed.
3. **Reference comparison**: compare against a reference with a stated tolerance: exact match after normalisation, numeric tolerance, set overlap (recall at k for a retrieval), similarity above a calibrated threshold.
4. **Model judge**: a rubric of 2 to 5 binary criteria, each answered yes or no with a quoted span of the output as evidence. Binary criteria are steadier across runs and easier to calibrate than a 1 to 10 scale. A criterion the judge cannot support with a quote that really occurs in the output counts as no; `scripts/judge.py` checks the quotes.
5. **Human label**: ground truth for calibrating every rung above, and the grader of last resort.

A deterministic grader on a model seam does not make the seam deterministic: the grader checks the output, the model still produces it.

## Calibrating a model judge

A model judge grades nothing that decides a change until it is calibrated:

1. Label 20 to 30 outputs yourself in `evals/<seam>/calibration.jsonl`, pass or fail per criterion, with at least a third failing and a few borderline.
2. Run `python evals/calibrate.py <seam>`: it runs the judge on the same outputs.
3. Read the agreement per criterion, **separately on your pass labels and on your fail labels**. Raw agreement hides a judge that says yes to everything: on a set that is 85% pass, that judge agrees 85% of the time and catches no failure. Both rates must reach 0.85; otherwise rewrite or split the criterion and repeat.
4. Give the judge a different model from the system under test when one is available (a larger hosted model judging a small local one is the usual setup), and always a different prompt.
5. Recalibrate whenever the judge's model or prompt changes. `calibrate.py` logs each calibration as a row of its own in `evals/log.md`.

## Trajectory graders

An agent's final answer can be right for the wrong reasons. When the path matters, grade the trajectory as well: the tools called, their order where the order matters, the number of steps against a budget, whether the agent verified its result before declaring done.

Keep trajectory criteria to what the spec requires. Each extra criterion freezes one implementation and turns the eval into a test of internals, the same failure the `tdd` skill calls implementation-coupled.
