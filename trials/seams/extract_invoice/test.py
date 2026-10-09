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
