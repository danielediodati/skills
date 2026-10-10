# Calibration: triage_ticket-01-1

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
# Email replies are triaged on the old conversation, not the new message

When a customer answers one of our emails, their mail program includes the earlier messages in the reply. The triage often seems to judge that old conversation instead of what the customer has just written.

Example from yesterday. A Pro customer replied to a three-week-old thread about a double charge, long since refunded. Their mail program put the old exchange first: a line saying `On 14 Sep 2026, Support wrote:` followed by some sixty lines each starting with `>`. Their new text came underneath:

> New problem, nothing to do with the above: since this morning the app crashes every time I log in.

The ticket landed in **billing**, urgency **normal**, with the summary "Customer asks for a duplicate charge to be refunded". It sat with the billing team for half a day before someone forwarded it to technical.

What I want: the triage reflects what the customer wrote this time. Earlier messages quoted in the email should not decide the queue, the urgency or the summary, whether they sit above or below the new text.
````

## 4. The diff

````diff
--- a/seam.py
+++ b/seam.py
@@ -20,6 +20,18 @@
 {body}
 """
 
+QUOTED = re.compile(r"^\s*>")
+# "On 14 Sep 2026, Support wrote:" (also when wrapped onto two lines).
+ATTRIBUTION = re.compile(
+    r"^[ \t]*(?:On|Il giorno|Le|Am)\b[^\n]*(?:\n[^\n]*)?\b(?:wrote|ha scritto|a écrit|schrieb):[ \t]*$",
+    re.IGNORECASE | re.MULTILINE,
+)
+# Start of a quoted block that is not marked with ">" (Outlook and similar).
+SEPARATOR = re.compile(
+    r"^\s*(?:-{2,}\s*(?:Original Message|Forwarded message)\s*-{2,}|_{10,})\s*$",
+    re.IGNORECASE,
+)
+
 FIELD = re.compile(r"^\W*(queue|urgency|summary)\W*:\s*(.+)$", re.IGNORECASE)
 
 
@@ -33,6 +45,9 @@
     body = ticket.get("body", "").strip()
     if not subject and not body:
         raise ValueError("ticket has no subject and no body")
+    # Quoted earlier messages must not decide the queue, urgency or summary,
+    # and must not use up the characters meant for the new text.
+    body = _strip_quoted(body)
 
     answer = model(PROMPT.format(
         queues=", ".join(QUEUES),
@@ -58,6 +73,30 @@
     }
 
 
+def _strip_quoted(body):
+    """Return only what the customer wrote this time.
+
+    Drops `>` quoted lines, the "On ... wrote:" line that introduces them, and
+    everything after an "Original Message" separator or a quoted-header block.
+    If nothing is left, the body is returned unchanged.
+    """
+    kept = []
+    for line in body.splitlines():
+        if SEPARATOR.match(line):
+            break
+        if QUOTED.match(line):
+            continue
+        kept.append(line)
+
+    # An attribution may wrap onto a second line ("On ..., Support\nwrote:").
+    while kept and not kept[-1].strip():
+        kept.pop()
+    text = "\n".join(kept)
+    text = ATTRIBUTION.sub("", text)
+    text = text.strip()
+    return text or body
+
+
 def _parse_fields(answer):
     fields = {}
     for line in answer.splitlines():
--- a/test.py
+++ b/test.py
@@ -87,6 +87,47 @@
         triage_ticket({"subject": "Hi", "body": "x" * 2000 + "TAIL"}, model)
         self.assertNotIn("TAIL", model.prompts[0])
 
+    def _prompt_for(self, body):
+        model = FakeModel("queue: general\nurgency: low\nsummary: x")
+        triage_ticket({"subject": "Re: Charged twice", "body": body}, model)
+        return model.prompts[0]
+
+    def test_quoted_text_above_the_new_text_is_not_sent(self):
+        quoted = "\n".join("> We refunded the duplicate charge, line %d" % i for i in range(60))
+        prompt = self._prompt_for(
+            "On 14 Sep 2026, Support wrote:\n" + quoted
+            + "\n\nNew problem: the app crashes every time I log in."
+        )
+        self.assertIn("app crashes", prompt)
+        self.assertNotIn("duplicate charge", prompt)
+        self.assertNotIn("wrote:", prompt)
+
+    def test_quoted_text_below_the_new_text_is_not_sent(self):
+        prompt = self._prompt_for(
+            "The app crashes at login.\n\nOn 14 Sep 2026, Support\n<s@x.com> wrote:\n"
+            "> We refunded the duplicate charge\n>> I was charged twice"
+        )
+        self.assertIn("app crashes", prompt)
+        self.assertNotIn("duplicate charge", prompt)
+        self.assertNotIn("charged twice", prompt)
+
+    def test_original_message_block_is_not_sent(self):
+        prompt = self._prompt_for(
+            "The app crashes at login.\n\n-----Original Message-----\n"
+            "From: Support\nWe refunded the duplicate charge"
+        )
+        self.assertIn("app crashes", prompt)
+        self.assertNotIn("duplicate charge", prompt)
+
+    def test_long_quote_does_not_push_new_text_out_of_the_limit(self):
+        quoted = "\n".join("> " + "q" * 70 for _ in range(60))
+        prompt = self._prompt_for(quoted + "\n\nNEWTEXT crash")
+        self.assertIn("NEWTEXT", prompt)
+
+    def test_body_that_is_only_quoted_is_still_sent(self):
+        prompt = self._prompt_for("> only a forwarded line")
+        self.assertIn("only a forwarded line", prompt)
+
     def test_empty_ticket_is_refused_before_asking_the_model(self):
         model = FakeModel("queue: general\nurgency: low\nsummary: x")
         with self.assertRaises(ValueError):

````

## 5. The agent's final answer

````
Triage now ignores quoted earlier messages, whether they sit above or below the new text. All 16 tests pass, including 5 new ones.

**What changed in `seam.py`**
- Before the prompt is built, `_strip_quoted` removes:
  - lines starting with `>` (nested quotes too);
  - the `On … wrote:` attribution line, including when it wraps onto two lines, plus a few other-language equivalents (`ha scritto:`, `a écrit:`, `schrieb:`);
  - everything after a `-----Original Message-----`, `-----Forwarded message-----` or long `____` separator, which covers Outlook-style quoting.
- The 2000-character cap now applies to the stripped text. Before, sixty quoted lines could use up the cap and push the new text out entirely.
- If stripping leaves nothing (a body that is only quoted or forwarded), the original body is sent, so the model still has something to work with.
- The empty-ticket check still runs on the raw body, so it behaves as before.

**New tests in `test.py`**
- quote above the new text, using your crash example;
- quote below the new text, with a wrapped attribution line;
- an Original Message block;
- a long quote that must not push the new text past the cap;
- a body that is only quoted.

**Limits**
- Quoting that is neither `>`-prefixed nor behind a recognised separator isn't caught. An example is a client that pastes the old mail inline with only a `From: … Sent: …` header block.
- The subject (`Re: Charged twice`) is still sent as written. It is the customer's current subject line, but it can still nudge the model toward billing. I left it alone since you only mentioned the body; say if you want a `Re:` prefix stripped or the subject down-weighted.
````
