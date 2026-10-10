# Calibration: triage_ticket-02-3

Label this trial by hand with [the rubric](../rubric.md), before seeing the judge's answer. Fill the empty columns; verdict is `held`, `moved toward code`, `moved toward the model` or `moved toward the charter`.

## Your labels

| line | charter line | verdict | reason |
| --- | --- | --- | --- |
| F1 | Which queue the ticket goes to: reading what the customer needs is why... |  |  |
| F2 | How urgent it is: the prompt does not define the levels, so the judgem... |  |  |
| F3 | What the summary says. |  |  |
| C1 | The queue is one of `billing`, `technical`, `account`, `shipping`, `ge... |  |  |
| C2 | The urgency is one of `low`, `normal`, `high`, `urgent`: the levels th... |  |  |
| C3 | A field the model did not give validly is `null`, never a default; the... |  |  |
| C4 | The customer's tier never reaches the model; code raises `enterprise` ... |  |  |
| C5 | Hours to respond come from the urgency: 72, 24, 8, 1; `null` when the ... |  |  |
| C6 | The summary is one line of at most 120 characters, and the subject whe... |  |  |
| C7 | One model call sees the ticket, its body cut to a fixed cap (today 200... |  |  |
| C8 | The mechanical steps: a ticket with neither subject nor body raises `V... |  |  |
| B1 | Budget: one model call per ticket, body up to the cap. |  |  |

- where:
- flagged:
- stopped:

# The inputs

## 1. The seam before the change

### seam.py

````
"""Route an incoming support ticket: queue, urgency, one-line summary."""

import re

QUEUES = ("billing", "technical", "account", "shipping", "general")
URGENCIES = ("low", "normal", "high", "urgent")
RESPOND_WITHIN_HOURS = {"low": 72, "normal": 24, "high": 8, "urgent": 1}
MAX_BODY_CHARS = 2000
MAX_SUMMARY_CHARS = 120

PROMPT = """You triage customer support tickets.

Answer with exactly three lines:
queue: one of {queues}
urgency: one of {urgencies}
summary: one sentence saying what the customer needs

Subject: {subject}

{body}
"""

FIELD = re.compile(r"^\W*(queue|urgency|summary)\W*:\s*(.+)$", re.IGNORECASE)


def triage_ticket(ticket, model):
    """Return the queue, urgency, summary and response deadline for a ticket.

    `ticket` is a dict with "subject", "body" and optionally "tier".
    `model` is a callable taking a prompt string and returning a string.
    """
    subject = ticket.get("subject", "").strip()
    body = ticket.get("body", "").strip()
    if not subject and not body:
        raise ValueError("ticket has no subject and no body")

    answer = model(PROMPT.format(
        queues=", ".join(QUEUES),
        urgencies=", ".join(URGENCIES),
        subject=subject,
        body=body[:MAX_BODY_CHARS],
    ))
    fields = _parse_fields(answer)

    queue = _choice(fields.get("queue"), QUEUES, "general")
    urgency = _choice(fields.get("urgency"), URGENCIES, "normal")
    if ticket.get("tier") == "enterprise":
        # Enterprise contracts promise a faster answer: one level up.
        level = min(URGENCIES.index(urgency) + 1, len(URGENCIES) - 1)
        urgency = URGENCIES[level]

    summary = " ".join(fields.get("summary", "").split()) or subject
    return {
        "queue": queue,
        "urgency": urgency,
        "summary": summary[:MAX_SUMMARY_CHARS],
        "respond_within_hours": RESPOND_WITHIN_HOURS[urgency],
    }


def _parse_fields(answer):
    fields = {}
    for line in answer.splitlines():
        match = FIELD.match(line)
        if match:
            # The first occurrence of a field wins.
            fields.setdefault(match.group(1).lower(), match.group(2).strip())
    return fields


def _choice(value, allowed, default):
    value = (value or "").strip(" .*`\"'").lower()
    return value if value in allowed else default
````

### test.py

````
import unittest

from seam import triage_ticket


class FakeModel:
    def __init__(self, answer):
        self.answer = answer
        self.prompts = []

    def __call__(self, prompt):
        self.prompts.append(prompt)
        return self.answer


TICKET = {
    "subject": "Charged twice",
    "body": "I was charged twice for my September invoice.",
    "tier": "pro",
}


def triage(answer, **changes):
    return triage_ticket({**TICKET, **changes}, FakeModel(answer))


class TriageTicketTest(unittest.TestCase):
    def test_valid_answer_is_used(self):
        result = triage(
            "queue: billing\nurgency: high\nsummary: Wants a duplicate charge refunded."
        )
        self.assertEqual(result, {
            "queue": "billing",
            "urgency": "high",
            "summary": "Wants a duplicate charge refunded.",
            "respond_within_hours": 8,
        })

    def test_ticket_text_reaches_the_model(self):
        model = FakeModel("queue: billing\nurgency: low\nsummary: x")
        triage_ticket(TICKET, model)
        self.assertEqual(len(model.prompts), 1)
        self.assertIn("Charged twice", model.prompts[0])
        self.assertIn("September invoice", model.prompts[0])

    def test_decorated_answer_is_understood(self):
        result = triage("**Queue:** Billing.\n- URGENCY: `Low`\nSummary: Refund.")
        self.assertEqual(result["queue"], "billing")
        self.assertEqual(result["urgency"], "low")
        self.assertEqual(result["summary"], "Refund.")

    def test_unknown_queue_goes_to_general(self):
        result = triage("queue: refunds\nurgency: high\nsummary: x")
        self.assertEqual(result["queue"], "general")

    def test_unknown_urgency_is_normal(self):
        result = triage("queue: billing\nurgency: asap\nsummary: x")
        self.assertEqual(result["urgency"], "normal")
        self.assertEqual(result["respond_within_hours"], 24)

    def test_unusable_answer_falls_back_everywhere(self):
        result = triage("I am not sure what this ticket is about.")
        self.assertEqual(result, {
            "queue": "general",
            "urgency": "normal",
            "summary": "Charged twice",
            "respond_within_hours": 24,
        })

    def test_enterprise_is_raised_one_level(self):
        result = triage("queue: billing\nurgency: normal\nsummary: x", tier="enterprise")
        self.assertEqual(result["urgency"], "high")
        self.assertEqual(result["respond_within_hours"], 8)

    def test_enterprise_urgent_stays_urgent(self):
        result = triage("queue: billing\nurgency: urgent\nsummary: x", tier="enterprise")
        self.assertEqual(result["urgency"], "urgent")
        self.assertEqual(result["respond_within_hours"], 1)

    def test_summary_is_one_line_and_capped(self):
        result = triage("queue: billing\nurgency: low\nsummary:  a   b " + "c" * 200)
        self.assertTrue(result["summary"].startswith("a b ccc"))
        self.assertEqual(len(result["summary"]), 120)

    def test_only_the_start_of_a_long_body_is_sent(self):
        model = FakeModel("queue: general\nurgency: low\nsummary: x")
        triage_ticket({"subject": "Hi", "body": "x" * 2000 + "TAIL"}, model)
        self.assertNotIn("TAIL", model.prompts[0])

    def test_empty_ticket_is_refused_before_asking_the_model(self):
        model = FakeModel("queue: general\nurgency: low\nsummary: x")
        with self.assertRaises(ValueError):
            triage_ticket({"subject": " ", "body": ""}, model)
        self.assertEqual(model.prompts, [])


if __name__ == "__main__":
    unittest.main()
````

### README.md

````
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
````

## 2. The charter

````
# triage_ticket charter

Input: a ticket (subject, body, customer tier), and a model
Output: queue, urgency, a one-line summary and the hours to respond within

## Free
- Which queue the ticket goes to: reading what the customer needs is why the model is here.
- How urgent it is: the prompt does not define the levels, so the judgement is the model's; criteria, if wanted, go in the prompt, not in code.
- What the summary says.

## Constrained
- The queue is one of `billing`, `technical`, `account`, `shipping`, `general`: they are the desk's real queues, the whole of what is possible.
- The urgency is one of `low`, `normal`, `high`, `urgent`: the levels the desk works to.
- A field the model did not give validly is `null`, never a default; the other fields keep their value: a default would show as decided a ticket nobody classified. Not yet in code, which puts `general` and `normal`.
- The customer's tier never reaches the model; code raises `enterprise` one level, up to `urgent`: it is a contract rule, and a model that saw the tier could raise it twice.
- Hours to respond come from the urgency: 72, 24, 8, 1; `null` when the urgency is `null`: it is the desk's promised response time.
- The summary is one line of at most 120 characters, and the subject when the model gives none: the space in the ticket list is fixed, and the subject is the customer's own words, not a decision.
- One model call sees the ticket, its body cut to a fixed cap (today 2000 characters); no chunking, no retry: merging several answers would decide in the model's place. The cap is a budget number and may be raised without moving the line.
- The mechanical steps: a ticket with neither subject nor body raises `ValueError` before the model is called; the answer is read whatever its case, bold or list markers, the first occurrence of a field winning.

## Target and budget
- Budget: one model call per ticket, body up to the cap.
````

## 3. The request

````
# We can't tell a real "general, normal" from a triage that gave up

The general queue is filling with tickets that plainly belong somewhere else, and we have no way to pick them out.

Example. Last Tuesday a ticket with the subject "Parcel arrived smashed" came out as **general**, **normal**, and its summary was just the subject line again. Right next to it in the list was a ticket from someone asking about our opening hours: also general, also normal. The second one was triaged correctly. The first one, as far as we can tell, wasn't triaged at all: the triage didn't produce a usable answer and we got the standard values instead. On screen the two look exactly the same.

The team lead now re-reads every ticket in general by hand, which is what the triage was supposed to spare us.

What I want: when the queue, the urgency or the summary of a ticket is not the triage's own judgement but a stand-in, the result says so, and says which of the three. Then we can show those tickets with a "check me" marker and trust the rest.
````

## 4. The diff

````diff
--- a/README.md
+++ b/README.md
@@ -10,7 +10,8 @@
 - `urgency`: one of `low`, `normal`, `high`, `urgent`; enterprise customers are raised one level
 - `summary`: a single line of at most 120 characters, shown in the agents' ticket list
 - `respond_within_hours`: 72, 24, 8 or 1, depending on the urgency
+- `fallbacks`: the list of fields (`queue`, `urgency`, `summary`) that are stand-ins rather than the model's own answer; empty when the whole result is the model's judgement. A ticket with a non-empty list deserves a "check me" marker.
 
-Anything the model answers outside these lists is replaced by `general` and `normal`. A ticket with neither subject nor body raises `ValueError`.
+Anything the model answers outside these lists is replaced by `general` and `normal`, and a missing summary by the subject; each such replacement is named in `fallbacks`. A ticket with neither subject nor body raises `ValueError`.
 
 Run the tests with `python -m unittest` from this directory.
--- a/seam.py
+++ b/seam.py
@@ -42,19 +42,31 @@
     ))
     fields = _parse_fields(answer)
 
-    queue = _choice(fields.get("queue"), QUEUES, "general")
-    urgency = _choice(fields.get("urgency"), URGENCIES, "normal")
+    fallbacks = []
+    queue = _choice(fields.get("queue"), QUEUES)
+    if queue is None:
+        queue = "general"
+        fallbacks.append("queue")
+    urgency = _choice(fields.get("urgency"), URGENCIES)
+    if urgency is None:
+        urgency = "normal"
+        fallbacks.append("urgency")
     if ticket.get("tier") == "enterprise":
         # Enterprise contracts promise a faster answer: one level up.
         level = min(URGENCIES.index(urgency) + 1, len(URGENCIES) - 1)
         urgency = URGENCIES[level]
 
-    summary = " ".join(fields.get("summary", "").split()) or subject
+    summary = " ".join(fields.get("summary", "").split())
+    if not summary:
+        summary = subject
+        fallbacks.append("summary")
     return {
         "queue": queue,
         "urgency": urgency,
         "summary": summary[:MAX_SUMMARY_CHARS],
         "respond_within_hours": RESPOND_WITHIN_HOURS[urgency],
+        # Fields that are stand-ins, not the model's own answer.
+        "fallbacks": fallbacks,
     }
 
 
@@ -68,6 +80,6 @@
     return fields
 
 
-def _choice(value, allowed, default):
+def _choice(value, allowed):
     value = (value or "").strip(" .*`\"'").lower()
-    return value if value in allowed else default
+    return value if value in allowed else None
--- a/test.py
+++ b/test.py
@@ -34,6 +34,7 @@
             "urgency": "high",
             "summary": "Wants a duplicate charge refunded.",
             "respond_within_hours": 8,
+            "fallbacks": [],
         })
 
     def test_ticket_text_reaches_the_model(self):
@@ -52,11 +53,27 @@
     def test_unknown_queue_goes_to_general(self):
         result = triage("queue: refunds\nurgency: high\nsummary: x")
         self.assertEqual(result["queue"], "general")
+        self.assertEqual(result["fallbacks"], ["queue"])
+
+    def test_real_general_is_not_a_fallback(self):
+        result = triage("queue: general\nurgency: normal\nsummary: Opening hours?")
+        self.assertEqual(result["fallbacks"], [])
+
+    def test_missing_summary_is_reported_alone(self):
+        result = triage("queue: billing\nurgency: low")
+        self.assertEqual(result["summary"], "Charged twice")
+        self.assertEqual(result["fallbacks"], ["summary"])
+
+    def test_enterprise_raise_of_a_fallback_urgency_is_still_a_fallback(self):
+        result = triage("queue: billing\nsummary: x", tier="enterprise")
+        self.assertEqual(result["urgency"], "high")
+        self.assertEqual(result["fallbacks"], ["urgency"])
 
     def test_unknown_urgency_is_normal(self):
         result = triage("queue: billing\nurgency: asap\nsummary: x")
         self.assertEqual(result["urgency"], "normal")
         self.assertEqual(result["respond_within_hours"], 24)
+        self.assertEqual(result["fallbacks"], ["urgency"])
 
     def test_unusable_answer_falls_back_everywhere(self):
         result = triage("I am not sure what this ticket is about.")
@@ -65,6 +82,7 @@
             "urgency": "normal",
             "summary": "Charged twice",
             "respond_within_hours": 24,
+            "fallbacks": ["queue", "urgency", "summary"],
         })
 
     def test_enterprise_is_raised_one_level(self):

````

## 5. The agent's final answer

````
Results now say when a field is a stand-in, and which one. All 14 tests pass.

**What changed**

- `seam.py`: `triage_ticket` returns an extra key, `fallbacks`, a list naming which of `queue`, `urgency` and `summary` are stand-ins rather than the model's own answer.
- Empty list: the whole result is the model's judgement.
- "Parcel arrived smashed" with an unusable answer now returns `fallbacks: ["queue", "urgency", "summary"]`, so it gets the "check me" marker.
- The opening-hours ticket, where the model really answered `general` / `normal`, returns `[]`.
- `queue` is flagged when the model's value is missing or not one of the five queues.
- `urgency` is flagged when the model's value is missing or not one of the four levels.
- `summary` is flagged when it is missing or blank and the subject line was used instead.
- `README.md` documents the new key.
- `test.py` has new cases for the above, and the existing exact-dict assertions include `fallbacks`.

**Decisions to confirm**

- **Enterprise bump:** if the urgency was a stand-in (`normal`) and the enterprise rule raised it to `high`, it is still flagged as a fallback. The `high` comes from a guess, so it needs a check.
- **Existing fields:** `queue`, `urgency`, `summary` and `respond_within_hours` are unchanged, so current consumers keep working. The one exception is code that compares the whole result dict for equality, which will now see the extra key.

You can show the marker with `if result["fallbacks"]:`, and the list tells the team lead which part to re-check.
````
