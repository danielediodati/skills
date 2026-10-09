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
