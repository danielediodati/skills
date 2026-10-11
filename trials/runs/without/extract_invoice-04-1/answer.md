Continental number formats now load correctly, and all 18 tests pass, including the new ones. The Kessler invoice's `1.250,00` comes through as a total of `1250.00`, and Cartiera Lombarda's `2.340,50` as `2340.50`.

**What changed in `seam.py`**
- **Amount parsing:** when an amount arrives as text, `_number` now works out which separator is the decimal point and which is the thousands separator before converting it. It handles:
  - `1.250,00` (German/Italian)
  - `1,250.00` (British)
  - `1 250,00`, `1'250.50` and `2,5`
  - a trailing `EUR` or a `€`
- **Prompt:** I added a line asking the model to give amounts as plain numbers with a `.` decimal point. That should avoid most of these cases up front, and the parser covers the rest.

**One behaviour to know about**
A single separator followed by exactly three digits, such as `1.250` or `1,250`, is now rejected as `total is ambiguous, thousands or decimals`. It could mean 1250 or 1.25, and silently guessing wrong would be a thousand-fold error on a payment. Previously `"1.250"` was read as 1.25. `0.335` is unaffected, and so are amounts with two decimals or with both separators.

Malformed groupings like `1.25.00` are still refused as "not a number".

I added tests for the continental formats, English-grouped amounts, the ambiguous cases and bad grouping in `test.py`.