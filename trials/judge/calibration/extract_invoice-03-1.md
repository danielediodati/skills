# Calibration: extract_invoice-03-1

Label this trial by hand with [the rubric](../rubric.md), before seeing the judge's answer. Fill the empty columns; verdict is `held`, `moved toward code`, `moved toward the model` or `moved toward the charter`.

## Your labels

| line | charter line | verdict | reason |
| --- | --- | --- | --- |
| F1 | Which text is the supplier, the invoice number, each line's descriptio... |  |  |
| F2 | What an ambiguous date means (`02/10/2026`): the model sees the suppli... |  |  |
| F3 | Which currency the invoice is in (`€`, `EUR`, or nothing stated): infe... |  |  |
| F4 | Which entries are lines (delivery, discounts): the layout differs per ... |  |  |
| F5 | Negative amounts, for discounts and credit notes: they are real invoic... |  |  |
| F6 | Non-integer quantities (hours, metres, kilos): a whole-number rule wou... |  |  |
| F7 | An empty line description: it serves the clerk, not the check. |  |  |
| F8 | The supplier's name, as written: there is no supplier registry to matc... |  |  |
| C1 | The answer's shape: one JSON object with the named keys, `issue_date` ... |  |  |
| C2 | Currency in ISO 4217: the list of valid codes is closed and complete. ... |  |  |
| C3 | Net, VAT and total as separate fields, with the arithmetic between the... |  |  |
| C4 | Line amounts computed by code (quantity × unit price, rounded half-up ... |  |  |
| C5 | The lines must add up to the total to the cent, no tolerance; otherwis... |  |  |
| C6 | One model call, no retry, no fallback: the cost per invoice is fixed, ... |  |  |
| C7 | The mechanical steps: empty text refused before the model is called, J... |  |  |
| B1 | Budget: one model call per invoice. |  |  |

- where:
- flagged:
- stopped:

# The inputs

## 1. The seam before the change

### seam.py

````
"""Turn the text of a supplier invoice into checked, typed fields."""

import json
import re
from datetime import date
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

CENT = Decimal("0.01")

PROMPT = """Extract the invoice below as a JSON object with these keys:
"supplier" (string), "invoice_number" (string), "issue_date" (YYYY-MM-DD),
"currency" (three-letter code), "lines" (a list of objects with "description",
"quantity" and "unit_price") and "total" (the amount due).
Answer with the JSON object only.

Invoice:
{text}
"""


class InvoiceError(ValueError):
    """The invoice could not be read into a usable record."""


def extract_invoice(text, model):
    """Return the invoice in `text` as a dict, with the total checked against the lines.

    `model` is a callable taking a prompt string and returning a string.
    """
    if not text.strip():
        raise InvoiceError("empty invoice text")
    data = _load_json(model(PROMPT.format(text=text)))

    supplier = _text(data, "supplier")
    invoice_number = _text(data, "invoice_number")
    raw_date = _text(data, "issue_date")
    try:
        issue_date = date.fromisoformat(raw_date)
    except ValueError:
        raise InvoiceError(f"issue_date is not a date: {raw_date!r}") from None
    currency = _text(data, "currency").upper()
    if not re.fullmatch(r"[A-Z]{3}", currency):
        raise InvoiceError(f"currency is not a three-letter code: {currency!r}")

    raw_lines = data.get("lines")
    if not isinstance(raw_lines, list) or not raw_lines:
        raise InvoiceError("no invoice lines")
    lines = []
    for number, raw in enumerate(raw_lines, start=1):
        if not isinstance(raw, dict):
            raise InvoiceError(f"line {number} is not an object")
        quantity = _number(raw.get("quantity"), f"line {number} quantity")
        unit_price = _number(raw.get("unit_price"), f"line {number} unit_price")
        lines.append({
            "description": str(raw.get("description") or "").strip(),
            "quantity": quantity,
            "unit_price": unit_price,
            "amount": _cents(quantity * unit_price),
        })

    total = _cents(_number(data.get("total"), "total"))
    lines_total = sum((line["amount"] for line in lines), Decimal("0"))
    return {
        "supplier": supplier,
        "invoice_number": invoice_number,
        "issue_date": issue_date,
        "currency": currency,
        "lines": lines,
        "lines_total": lines_total,
        "total": total,
        "status": "ok" if lines_total == total else "mismatch",
    }


def _load_json(answer):
    # Models often wrap the object in a code fence or a sentence.
    start, end = answer.find("{"), answer.rfind("}")
    try:
        data = json.loads(answer[start:end + 1])
    except ValueError:
        raise InvoiceError("the answer is not JSON") from None
    if not isinstance(data, dict):
        raise InvoiceError("the answer is not a JSON object")
    return data


def _text(data, key):
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise InvoiceError(f"{key} is missing")
    return value.strip()


def _number(value, label):
    if value is None or isinstance(value, bool):
        raise InvoiceError(f"{label} is missing")
    try:
        number = Decimal(str(value).strip())
    except InvalidOperation:
        raise InvoiceError(f"{label} is not a number: {value!r}") from None
    if not number.is_finite():
        raise InvoiceError(f"{label} is not a number: {value!r}")
    return number


def _cents(amount):
    return amount.quantize(CENT, rounding=ROUND_HALF_UP)
````

### test.py

````
import json
import unittest
from datetime import date
from decimal import Decimal

from seam import InvoiceError, extract_invoice

INVOICE_TEXT = "Brightwell Paper Ltd - Invoice BP-2291 - 2 Oct 2026 - ..."

ANSWER = {
    "supplier": "Brightwell Paper Ltd",
    "invoice_number": "BP-2291",
    "issue_date": "2026-10-02",
    "currency": "eur",
    "lines": [
        {"description": "A4 paper, box", "quantity": 12, "unit_price": 24.5},
        {"description": "Delivery", "quantity": 1, "unit_price": "15.00"},
    ],
    "total": 309.0,
}


class FakeModel:
    def __init__(self, answer):
        self.answer = answer
        self.prompts = []

    def __call__(self, prompt):
        self.prompts.append(prompt)
        return self.answer


def extract(**changes):
    return extract_invoice(INVOICE_TEXT, FakeModel(json.dumps({**ANSWER, **changes})))


class ExtractInvoiceTest(unittest.TestCase):
    def test_fields_are_typed(self):
        result = extract()
        self.assertEqual(result["supplier"], "Brightwell Paper Ltd")
        self.assertEqual(result["invoice_number"], "BP-2291")
        self.assertEqual(result["issue_date"], date(2026, 10, 2))
        self.assertEqual(result["currency"], "EUR")
        self.assertEqual(result["lines"][0], {
            "description": "A4 paper, box",
            "quantity": Decimal("12"),
            "unit_price": Decimal("24.5"),
            "amount": Decimal("294.00"),
        })
        self.assertEqual(result["total"], Decimal("309.00"))

    def test_total_matching_the_lines_is_ok(self):
        result = extract()
        self.assertEqual(result["lines_total"], Decimal("309.00"))
        self.assertEqual(result["status"], "ok")

    def test_total_differing_from_the_lines_is_a_mismatch(self):
        result = extract(total=319)
        self.assertEqual(result["lines_total"], Decimal("309.00"))
        self.assertEqual(result["status"], "mismatch")

    def test_line_amounts_are_rounded_to_cents(self):
        lines = [{"description": "Cable, m", "quantity": 3, "unit_price": "0.335"}]
        result = extract(lines=lines, total="1.01")
        self.assertEqual(result["lines"][0]["amount"], Decimal("1.01"))
        self.assertEqual(result["status"], "ok")

    def test_invoice_text_reaches_the_model(self):
        model = FakeModel(json.dumps(ANSWER))
        extract_invoice(INVOICE_TEXT, model)
        self.assertEqual(len(model.prompts), 1)
        self.assertIn(INVOICE_TEXT, model.prompts[0])

    def test_json_inside_a_code_fence_is_read(self):
        answer = "Here is the invoice:\n```json\n" + json.dumps(ANSWER) + "\n```"
        result = extract_invoice(INVOICE_TEXT, FakeModel(answer))
        self.assertEqual(result["status"], "ok")

    def test_answer_without_json_is_an_error(self):
        with self.assertRaisesRegex(InvoiceError, "not JSON"):
            extract_invoice(INVOICE_TEXT, FakeModel("I could not read this invoice."))

    def test_missing_supplier_is_an_error(self):
        with self.assertRaisesRegex(InvoiceError, "supplier is missing"):
            extract(supplier="")

    def test_unreadable_date_is_an_error(self):
        with self.assertRaisesRegex(InvoiceError, "issue_date is not a date"):
            extract(issue_date="2nd October")

    def test_bad_currency_is_an_error(self):
        with self.assertRaisesRegex(InvoiceError, "currency"):
            extract(currency="euros")

    def test_no_lines_is_an_error(self):
        with self.assertRaisesRegex(InvoiceError, "no invoice lines"):
            extract(lines=[])

    def test_unreadable_amount_is_an_error(self):
        with self.assertRaisesRegex(InvoiceError, "total is not a number"):
            extract(total="three hundred")

    def test_missing_quantity_is_an_error(self):
        lines = [{"description": "Delivery", "unit_price": 15}]
        with self.assertRaisesRegex(InvoiceError, "line 1 quantity is missing"):
            extract(lines=lines)

    def test_empty_text_is_refused_before_asking_the_model(self):
        model = FakeModel(json.dumps(ANSWER))
        with self.assertRaises(InvoiceError):
            extract_invoice("  \n", model)
        self.assertEqual(model.prompts, [])


if __name__ == "__main__":
    unittest.main()
````

### README.md

````
# extract_invoice

Used by an accounts-payable team to load supplier invoices into the ledger without retyping them.

`extract_invoice(text, model)` takes the plain text of one invoice (from a PDF or an email) and a model, any callable that takes a prompt string and returns a string. The model reads the invoice and reports the supplier, invoice number, issue date, currency, the invoice lines and the total.

The function returns a dict with `supplier`, `invoice_number`, `issue_date` (a `date`), `currency` (three capital letters), `lines` (each with `description`, `quantity`, `unit_price` and the computed `amount`), `lines_total`, `total` and `status`. Amounts are `Decimal`, rounded to cents. `status` is `ok` when the lines add up to the total and `mismatch` when they don't; a mismatched invoice goes to a clerk instead of the ledger.

If the model's answer can't be read, or a field is missing or malformed, the function raises `InvoiceError` with a message naming the field.

Run the tests with `python -m unittest` from this directory.
````

## 2. The charter

````
# extract_invoice charter

Input: the plain text of one supplier invoice, and a model
Output: supplier, invoice number, issue date, currency, lines with computed amounts, lines total, total and a status (`ok` goes to the ledger, `mismatch` to a clerk); or `InvoiceError`

## Free
- Which text is the supplier, the invoice number, each line's description: reading invoices laid out by every supplier differently is why the model is here.
- What an ambiguous date means (`02/10/2026`): the model sees the supplier's country and language; a fixed day-month rule would be wrong for half of them.
- Which currency the invoice is in (`€`, `EUR`, or nothing stated): inferring it is reading.
- Which entries are lines (delivery, discounts): the layout differs per supplier.
- Negative amounts, for discounts and credit notes: they are real invoice content.
- Non-integer quantities (hours, metres, kilos): a whole-number rule would be no real constraint.
- An empty line description: it serves the clerk, not the check.
- The supplier's name, as written: there is no supplier registry to match against; with one, membership would be a constraint.

## Constrained
- The answer's shape: one JSON object with the named keys, `issue_date` as `YYYY-MM-DD`, at least one line; anything else raises `InvoiceError` naming the field. A record that cannot be checked must not reach the ledger.
- Currency in ISO 4217: the list of valid codes is closed and complete. Not yet in code, which only checks three capital letters.
- Net, VAT and total as separate fields, with the arithmetic between them checked by code. Not yet in code: today the total is the amount due, so a VAT invoice whose VAT is not reported as a line comes out `mismatch`.
- Line amounts computed by code (quantity × unit price, rounded half-up to cents), never read from the model: arithmetic has an answer written before anything runs.
- The lines must add up to the total to the cent, no tolerance; otherwise `mismatch` and a clerk. A wrong record in the ledger costs more than one checked by hand.
- One model call, no retry, no fallback: the cost per invoice is fixed, and an error already sends the invoice to a person.
- The mechanical steps: empty text refused before the model is called, JSON read from inside a code fence or a sentence, currency upper-cased.

## Target and budget
- Budget: one model call per invoice.
````

## 3. The request

````
# One unreadable field and we lose the whole invoice

When a single piece of an invoice can't be read, we get an error and nothing else. The clerk then types the entire invoice by hand, including the fourteen lines that were presumably read just fine.

Example. A freelancer sent us an invoice with no invoice number on it (they forgot). Supplier, date, currency, six lines and the total were all there in black and white. All we got back was the error `invoice_number is missing`.

Another one: a scan where the date had come out as `0Z/10/2026`. Error `issue_date is not a date`, and again none of the rest.

What I want: when part of an invoice can't be read, I still get everything that could be, together with a list of the fields that are missing or unreadable, so that the clerk fills in only those. Such an invoice must be clearly marked as incomplete so it can never go into the ledger as it is. If nothing usable comes out at all, an error is still the right answer.
````

## 4. The diff

````diff
--- a/README.md
+++ b/README.md
@@ -6,6 +6,8 @@
 
 The function returns a dict with `supplier`, `invoice_number`, `issue_date` (a `date`), `currency` (three capital letters), `lines` (each with `description`, `quantity`, `unit_price` and the computed `amount`), `lines_total`, `total` and `status`. Amounts are `Decimal`, rounded to cents. `status` is `ok` when the lines add up to the total and `mismatch` when they don't; a mismatched invoice goes to a clerk instead of the ledger.
 
-If the model's answer can't be read, or a field is missing or malformed, the function raises `InvoiceError` with a message naming the field.
+If some fields are missing or malformed, the function still returns everything it could read. Unreadable fields are `None` (a line with an unreadable quantity or unit price has `amount` `None`, and `lines_total` is then `None`), `status` is `incomplete`, and `problems` lists each one as `{"field": ..., "reason": ...}` (e.g. `invoice_number`, `lines[2].quantity`). An `incomplete` invoice must go to a clerk, never to the ledger; only `ok` may be loaded. `problems` is empty otherwise.
+
+If the model's answer isn't JSON, or nothing at all can be read from it, the function raises `InvoiceError`.
 
 Run the tests with `python -m unittest` from this directory.
--- a/seam.py
+++ b/seam.py
@@ -25,41 +25,67 @@
 def extract_invoice(text, model):
     """Return the invoice in `text` as a dict, with the total checked against the lines.
 
+    Fields that could not be read are None and listed in `problems`; such an
+    invoice has status "incomplete". If nothing at all can be read, InvoiceError
+    is raised.
+
     `model` is a callable taking a prompt string and returning a string.
     """
     if not text.strip():
         raise InvoiceError("empty invoice text")
     data = _load_json(model(PROMPT.format(text=text)))
 
-    supplier = _text(data, "supplier")
-    invoice_number = _text(data, "invoice_number")
-    raw_date = _text(data, "issue_date")
-    try:
-        issue_date = date.fromisoformat(raw_date)
-    except ValueError:
-        raise InvoiceError(f"issue_date is not a date: {raw_date!r}") from None
-    currency = _text(data, "currency").upper()
-    if not re.fullmatch(r"[A-Z]{3}", currency):
-        raise InvoiceError(f"currency is not a three-letter code: {currency!r}")
+    problems = []
 
+    def field(name, read):
+        try:
+            return read()
+        except InvoiceError as error:
+            problems.append({"field": name, "reason": str(error)})
+            return None
+
+    supplier = field("supplier", lambda: _text(data, "supplier"))
+    invoice_number = field("invoice_number", lambda: _text(data, "invoice_number"))
+    issue_date = field("issue_date", lambda: _date(data))
+    currency = field("currency", lambda: _currency(data))
+
+    lines = []
     raw_lines = data.get("lines")
     if not isinstance(raw_lines, list) or not raw_lines:
-        raise InvoiceError("no invoice lines")
-    lines = []
+        problems.append({"field": "lines", "reason": "no invoice lines"})
+        raw_lines = []
     for number, raw in enumerate(raw_lines, start=1):
         if not isinstance(raw, dict):
-            raise InvoiceError(f"line {number} is not an object")
-        quantity = _number(raw.get("quantity"), f"line {number} quantity")
-        unit_price = _number(raw.get("unit_price"), f"line {number} unit_price")
+            problems.append({"field": f"lines[{number}]", "reason": "line is not an object"})
+            raw = {}
+        quantity = field(f"lines[{number}].quantity",
+                         lambda: _number(raw.get("quantity"), "quantity"))
+        unit_price = field(f"lines[{number}].unit_price",
+                           lambda: _number(raw.get("unit_price"), "unit_price"))
+        known = quantity is not None and unit_price is not None
         lines.append({
             "description": str(raw.get("description") or "").strip(),
             "quantity": quantity,
             "unit_price": unit_price,
-            "amount": _cents(quantity * unit_price),
+            "amount": _cents(quantity * unit_price) if known else None,
         })
 
-    total = _cents(_number(data.get("total"), "total"))
-    lines_total = sum((line["amount"] for line in lines), Decimal("0"))
+    total = field("total", lambda: _cents(_number(data.get("total"), "total")))
+
+    readable = [supplier, invoice_number, issue_date, currency, total]
+    readable += [line["amount"] for line in lines]
+    if all(value is None for value in readable):
+        raise InvoiceError("nothing usable in the answer: " + "; ".join(
+            f"{p['field']}: {p['reason']}" for p in problems))
+
+    if lines and all(line["amount"] is not None for line in lines):
+        lines_total = sum((line["amount"] for line in lines), Decimal("0"))
+    else:
+        lines_total = None
+    if problems:
+        status = "incomplete"
+    else:
+        status = "ok" if lines_total == total else "mismatch"
     return {
         "supplier": supplier,
         "invoice_number": invoice_number,
@@ -68,7 +94,8 @@
         "lines": lines,
         "lines_total": lines_total,
         "total": total,
-        "status": "ok" if lines_total == total else "mismatch",
+        "status": status,
+        "problems": problems,
     }
 
 
@@ -91,6 +118,21 @@
     return value.strip()
 
 
+def _date(data):
+    raw_date = _text(data, "issue_date")
+    try:
+        return date.fromisoformat(raw_date)
+    except ValueError:
+        raise InvoiceError(f"issue_date is not a date: {raw_date!r}") from None
+
+
+def _currency(data):
+    currency = _text(data, "currency").upper()
+    if not re.fullmatch(r"[A-Z]{3}", currency):
+        raise InvoiceError(f"currency is not a three-letter code: {currency!r}")
+    return currency
+
+
 def _number(value, label):
     if value is None or isinstance(value, bool):
         raise InvoiceError(f"{label} is missing")
--- a/test.py
+++ b/test.py
@@ -80,30 +80,56 @@
         with self.assertRaisesRegex(InvoiceError, "not JSON"):
             extract_invoice(INVOICE_TEXT, FakeModel("I could not read this invoice."))
 
-    def test_missing_supplier_is_an_error(self):
-        with self.assertRaisesRegex(InvoiceError, "supplier is missing"):
-            extract(supplier="")
+    def test_complete_invoice_has_no_problems(self):
+        self.assertEqual(extract()["problems"], [])
 
-    def test_unreadable_date_is_an_error(self):
-        with self.assertRaisesRegex(InvoiceError, "issue_date is not a date"):
-            extract(issue_date="2nd October")
+    def test_missing_invoice_number_keeps_the_rest(self):
+        result = extract(invoice_number=None)
+        self.assertEqual(result["status"], "incomplete")
+        self.assertIsNone(result["invoice_number"])
+        self.assertEqual([p["field"] for p in result["problems"]], ["invoice_number"])
+        self.assertEqual(result["supplier"], "Brightwell Paper Ltd")
+        self.assertEqual(len(result["lines"]), 2)
+        self.assertEqual(result["total"], Decimal("309.00"))
+        self.assertEqual(result["lines_total"], Decimal("309.00"))
 
-    def test_bad_currency_is_an_error(self):
-        with self.assertRaisesRegex(InvoiceError, "currency"):
-            extract(currency="euros")
+    def test_unreadable_date_keeps_the_rest(self):
+        result = extract(issue_date="0Z/10/2026")
+        self.assertEqual(result["status"], "incomplete")
+        self.assertIsNone(result["issue_date"])
+        self.assertEqual(result["problems"][0]["field"], "issue_date")
+        self.assertIn("0Z/10/2026", result["problems"][0]["reason"])
+        self.assertEqual(result["invoice_number"], "BP-2291")
 
-    def test_no_lines_is_an_error(self):
-        with self.assertRaisesRegex(InvoiceError, "no invoice lines"):
-            extract(lines=[])
+    def test_bad_currency_is_incomplete(self):
+        result = extract(currency="euros")
+        self.assertEqual(result["status"], "incomplete")
+        self.assertIsNone(result["currency"])
 
-    def test_unreadable_amount_is_an_error(self):
-        with self.assertRaisesRegex(InvoiceError, "total is not a number"):
-            extract(total="three hundred")
+    def test_unreadable_total_is_incomplete(self):
+        result = extract(total="three hundred")
+        self.assertEqual(result["status"], "incomplete")
+        self.assertIsNone(result["total"])
+        self.assertEqual(result["lines_total"], Decimal("309.00"))
 
-    def test_missing_quantity_is_an_error(self):
-        lines = [{"description": "Delivery", "unit_price": 15}]
-        with self.assertRaisesRegex(InvoiceError, "line 1 quantity is missing"):
-            extract(lines=lines)
+    def test_missing_quantity_marks_the_line(self):
+        lines = [{"description": "Delivery", "unit_price": 15},
+                 {"description": "Paper", "quantity": 2, "unit_price": 1}]
+        result = extract(lines=lines)
+        self.assertEqual(result["status"], "incomplete")
+        self.assertEqual(result["problems"][0]["field"], "lines[1].quantity")
+        self.assertIsNone(result["lines"][0]["amount"])
+        self.assertEqual(result["lines"][1]["amount"], Decimal("2.00"))
+        self.assertIsNone(result["lines_total"])
+
+    def test_no_lines_is_incomplete(self):
+        result = extract(lines=[])
+        self.assertEqual(result["status"], "incomplete")
+        self.assertEqual(result["problems"][0]["field"], "lines")
+
+    def test_nothing_usable_is_an_error(self):
+        with self.assertRaisesRegex(InvoiceError, "nothing usable"):
+            extract_invoice(INVOICE_TEXT, FakeModel("{}"))
 
     def test_empty_text_is_refused_before_asking_the_model(self):
         model = FakeModel(json.dumps(ANSWER))

````

## 5. The agent's final answer

````
Partly unreadable invoices now come back with everything that could be read, plus a list of what couldn't. All 16 tests pass.

**Behaviour (`seam.py`)**
- Each unreadable field is `None` and listed in a new `problems` entry, for example `{"field": "issue_date", "reason": "issue_date is not a date: '0Z/10/2026'"}`.
- Line problems name the line, for example `lines[2].quantity`. The other lines, and the rest of that line, are kept.
- Any problem gives `status: "incomplete"`, so it can't be mistaken for `ok` or `mismatch`. Anything that only loads `ok` invoices into the ledger stays safe.
- `lines_total` is `None` when any line amount is unknown. `total` is `None` if it was unreadable.
- `InvoiceError` is still raised for empty text, an answer that isn't a JSON object, or an answer where nothing at all was usable.
- Your two examples now give: a result with `invoice_number: None` and all else intact, and a result with `issue_date: None` and all else intact.

**Tests and docs**
- The old "missing X is an error" tests became "incomplete" tests. I added one for an answer with nothing usable (`{}`), which still errors.
- The README describes the new contract.

**Decision for you**
- Any `ok`/`mismatch` consumer that reads fields like `issue_date` directly must now check `status` first, since those fields can be `None`.
- A line with a non-numeric description is not treated as a problem; only quantity and unit price are checked, as before.
- I kept `problems` as an always-present key (empty for `ok`/`mismatch`) so callers see one shape.
````
