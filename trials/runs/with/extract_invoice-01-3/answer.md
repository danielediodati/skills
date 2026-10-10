Amounts written the way your suppliers write them are now read as numbers, and the tests pass (17, including new ones for this).

**What changed**
- `seam.py`: `_number` now parses string amounts in code, with no extra model call and no change to the prompt.
- Accepted forms:
  - Thousands separators: `.`, `,`, `'`, `’`, and spaces.
  - Decimal point or decimal comma.
  - A currency symbol or three-letter code before or after the amount, including `Fr.`.
  - A sign before or after the symbol.
- Your three examples (`1.234,56`, `£1,234.56`, `1'050.00 CHF`) now read as 1234.56, 1234.56 and 1050.00.
- Malformed or badly grouped amounts (`1,23,456`, `12.34.56`, `5 apples`) are still refused with `is not a number`.

**Refused as ambiguous**
- A lone separator followed by exactly three digits, after a one-to-three-digit number not starting with 0, is refused with `... is ambiguous, thousands or decimals`. That covers `1.234`, `1,234` and `CHF 12,345`.
- `0.335` and `1234,567` still read as decimals, because a thousands group can't look like that.
- Plain JSON numbers from the model are untouched.

**Behaviour change**
- A three-decimal unit price the model returns as a string, like `"1.234"`, used to load as 1.234 and is now refused. That follows your preference for refusing over guessing. If suppliers send many such prices, the model could be asked to return them as JSON numbers, but that is a decision for you.

I also added the rule to the charter's mechanical steps and a short note to the README. The seam's free and constrained lines are unchanged.