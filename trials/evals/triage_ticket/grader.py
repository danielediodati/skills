"""Grader for triage_ticket: reference comparison (GRADERS.md, rung 3).

A case's `expected` holds, for the two decisions the model is free to take, the values a person
at the desk would accept, and for the summary the words it must and must not carry:

    queue          the accepted queues
    urgency        the accepted urgencies, after the enterprise raise
    summary_any    the summary names what the customer needs: at least one of these, any case
    summary_none   the summary carries none of these (optional)
"""


def grade(case, result):
    expected, output = case["expected"], result["output"]
    summary = (output["summary"] or "").lower()
    return (
        output["queue"] in expected["queue"]
        and output["urgency"] in expected["urgency"]
        and any(word.lower() in summary for word in expected["summary_any"])
        and not any(word.lower() in summary for word in expected.get("summary_none", ()))
    )
