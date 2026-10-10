# Calibration: extract_invoice-01-2

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
# Invoices fail when amounts are written the way our suppliers write them

A good share of our invoices is refused because of how the amounts are written, although a person reads them without a second thought.

Three from last week's import log:

- An Italian supplier, total printed as `1.234,56`. Refused with: `total is not a number: '1.234,56'`
- A British one, total printed as `£1,234.56`. Refused with: `total is not a number: '£1,234.56'`
- A Swiss one, unit price printed as `1'050.00 CHF`. Refused with: `line 2 unit_price is not a number: "1'050.00 CHF"`

Each of these went to a clerk to be typed in by hand, and there was nothing wrong with any of them.

What I want: amounts written with thousands separators, with a decimal comma or a decimal point, and with a currency symbol or code next to them, are read as the numbers they are. `1.234,56` and `1,234.56` are both one thousand two hundred thirty-four and fifty-six cents. Where an amount really can be read two ways and nothing in it settles the matter, I would rather the invoice be refused, as today, than loaded with a guess.
````

## 4. The diff

````diff
--- a/README.md
+++ b/README.md
@@ -8,4 +8,6 @@
 
 If the model's answer can't be read, or a field is missing or malformed, the function raises `InvoiceError` with a message naming the field.
 
+Amounts may be written as suppliers print them: thousands separators (`.` `,` `'` or a space), a decimal comma or point, and a currency symbol or code before or after (`1.234,56`, `£1,234.56`, `1'050.00 CHF`). An amount whose separators can be read two ways, such as `1.234` or `1,234` (one thousand two hundred thirty-four, or one and 234 thousandths), is refused with "is ambiguous" rather than guessed. Numbers that arrive as JSON numbers are taken as they are.
+
 Run the tests with `python -m unittest` from this directory.
--- a/seam.py
+++ b/seam.py
@@ -91,11 +91,32 @@
     return value.strip()
 
 
+class _Ambiguous(Exception):
+    """The separators in an amount can be read two ways."""
+
+
+# A currency symbol or code: "£", "CHF", "Fr.", "US$".
+_CURRENCY = r"(?:[^\W\d_]{1,3}[^\w\s.,'+\-]|[^\W\d_]{1,3}\.?|[^\w\s.,'+\-]{1,3})"
+_AMOUNT = re.compile(
+    rf"(?P<sign1>[-+])?\s*(?:{_CURRENCY}\s*)?(?P<sign2>[-+])?\s*"
+    rf"(?P<core>[\d.,' ]*\d[\d.,' ]*?)\s*(?:{_CURRENCY})?"
+)
+_EXPONENT = re.compile(r"[-+]?\d+(?:\.\d+)?[eE][-+]?\d+")
+_SEPARATORS = str.maketrans({
+    " ": " ", " ": " ", " ": " ", "’": "'", "ʼ": "'",
+})
+
+
 def _number(value, label):
     if value is None or isinstance(value, bool):
         raise InvoiceError(f"{label} is missing")
     try:
-        number = Decimal(str(value).strip())
+        if isinstance(value, str):
+            number = _written_amount(value)
+        else:
+            number = Decimal(str(value).strip())
+    except _Ambiguous:
+        raise InvoiceError(f"{label} is ambiguous: {value!r}") from None
     except InvalidOperation:
         raise InvoiceError(f"{label} is not a number: {value!r}") from None
     if not number.is_finite():
@@ -103,5 +124,47 @@
     return number
 
 
+def _written_amount(text):
+    """Read an amount as a supplier writes it: "1.234,56", "£1,234.56", "1'050.00 CHF".
+
+    Raises InvalidOperation when it is not an amount, _Ambiguous when the
+    separators could mean two different amounts (such as "1.234").
+    """
+    text = text.translate(_SEPARATORS).strip()
+    if _EXPONENT.fullmatch(text):
+        return Decimal(text)
+    match = _AMOUNT.fullmatch(text)
+    if not match or (match["sign1"] and match["sign2"]):
+        raise InvalidOperation
+    sign = match["sign1"] or match["sign2"] or ""
+    core = match["core"].strip()
+
+    seps = re.findall(r"[.,' ]", core)
+    pieces = re.split(r"[.,' ]", core)
+    frac = ""
+    if not seps:
+        whole = pieces
+    elif seps[-1] in ".," and seps.count(seps[-1]) == 1 and len(seps) > 1:
+        # "1,234.56", "1.234,56", "1 234,56": the last separator is the decimal one.
+        if len(set(seps[:-1])) != 1:
+            raise InvalidOperation
+        whole, frac = pieces[:-1], pieces[-1]
+    elif len(seps) == 1 and seps[0] in ".,":
+        whole, frac = pieces[:1], pieces[1]
+        if len(frac) == 3 and whole[0] not in ("", "0") and len(whole[0]) <= 3:
+            raise _Ambiguous  # "1.234" is 1234 or 1.234
+    else:
+        # Only grouping separators: "1,234,567", "1'050", "1 234".
+        if len(set(seps)) != 1:
+            raise InvalidOperation
+        whole = pieces
+    if "" in pieces[1:]:
+        raise InvalidOperation
+    if len(whole) > 1 and not (1 <= len(whole[0]) <= 3 and whole[0] != "0"
+                               and all(len(group) == 3 for group in whole[1:])):
+        raise InvalidOperation
+    return Decimal(f"{sign}{''.join(whole) or '0'}" + (f".{frac}" if frac else ""))
+
+
 def _cents(amount):
     return amount.quantize(CENT, rounding=ROUND_HALF_UP)
--- a/test.py
+++ b/test.py
@@ -100,6 +100,42 @@
         with self.assertRaisesRegex(InvoiceError, "total is not a number"):
             extract(total="three hundred")
 
+    def test_amounts_as_suppliers_write_them_are_read(self):
+        cases = {
+            "1.234,56": "1234.56",
+            "1,234.56": "1234.56",
+            "£1,234.56": "1234.56",
+            "1'050.00 CHF": "1050.00",
+            "EUR 1 234,56": "1234.56",
+            "€ 1.234.567,89": "1234567.89",
+            "1,234,567": "1234567",
+            "1’050": "1050",
+            "-£1,234.56": "-1234.56",
+            "12,5": "12.5",
+            "0.335": "0.335",
+            "1234.567": "1234.567",
+            "15.00": "15.00",
+            "US$ 99.90": "99.90",
+        }
+        for written, expected in cases.items():
+            with self.subTest(written):
+                result = extract(lines=[{"description": "x", "quantity": 1,
+                                         "unit_price": written}])
+                self.assertEqual(result["lines"][0]["unit_price"], Decimal(expected))
+
+    def test_ambiguous_amount_is_an_error(self):
+        for written in ("1.234", "1,234", "12,345", "123.456 EUR"):
+            with self.subTest(written):
+                with self.assertRaisesRegex(InvoiceError, "total is ambiguous"):
+                    extract(total=written)
+
+    def test_malformed_amounts_are_errors(self):
+        for written in ("1,23,456", "1.234,56,7", "1,234.56.78", "12 34", "1.", "--5",
+                        "1.2.3", "total 12", "1,234.567,89"):
+            with self.subTest(written):
+                with self.assertRaises(InvoiceError):
+                    extract(total=written)
+
     def test_missing_quantity_is_an_error(self):
         lines = [{"description": "Delivery", "unit_price": 15}]
         with self.assertRaisesRegex(InvoiceError, "line 1 quantity is missing"):

````

## 5. The agent's final answer

````
Amounts written the way your suppliers write them are now read as the numbers they are, and the three examples from last week's log load correctly. The suite, with the new tests, passes (17 tests).

**What changed**
- The reading logic is in `seam.py` (`_number` and a new `_written_amount`).
- `README.md` documents the new behaviour.
- `test.py` has new tests for the accepted, ambiguous and malformed cases.

**What is read now**
- **Examples:** `1.234,56`, `1,234.56`, `£1,234.56`, `1'050.00 CHF`, `EUR 1 234,56`, `-£1,234.56` and `1,234,567` all work.
- **Separators:** `.`, `,`, `'`, `’`, a space and non-breaking or thin spaces count as thousands separators.
- **Decimals:** when a comma and a point both appear, the last one is the decimal separator. A single separator with anything other than three digits after it is a decimal (`12,5`, `0.335`, `1234.567`).
- **Currency:** a symbol or code before or after the amount is ignored (`£`, `€`, `CHF`, `Fr.`, `US$`).

**What is refused**
- **Ambiguous amounts:** `1.234` and `1,234` could be one thousand two hundred thirty-four or one and 234 thousandths, so they are refused with `total is ambiguous: '1.234'`.
- **Malformed amounts:** mismatched or misplaced groupings (`1,23,456`, `1.2.3`, `12 34`, `1,234.567,89`), a trailing separator, and stray words are refused with `is not a number`.

**Things to be aware of**
- A string like `"1.234"` used to load as 1.234. It is now refused, because that exact form is how an Italian `1.234` (one thousand two hundred thirty-four) would arrive. Numbers the model sends as real JSON numbers are untouched.
- Three-decimal quantities such as `1.250` kg, sent as a string, will also be refused, since they are ambiguous in the same way.
- Indian lakh grouping (`1,23,456`) and negatives written `(123.45)` or `123.45-` are refused rather than guessed. Say if you want them supported.
- The currency printed on an amount is not compared with the invoice's `currency` field.
````
