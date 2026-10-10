Recommendations whose reason quotes the wrong price now keep the product and lose the reason, but I couldn't run the tests, so the change is unverified. Shell commands that edit files or chain operations were denied in this session, so I made the last edits with the file tools.

To check it, run `python -m unittest` in the project directory.

## What changed

- **`seam.py`**: a new `states_other_price(reason, price)` check runs on each reason after it is cut to 80 characters. If it finds a price that differs from the product's price (compared to the cent), the reason becomes `""` and the product stays in the strip.
- **`test.py`**: three new tests cover wrong prices being blanked, correct prices and non-price numbers being kept, and a price cut by the 80-character cap.

## What counts as a price

A number is treated as a price when any of these hold:
- It has a currency symbol or word next to it: `€14.90`, `$4`, `14,90 EUR`, `4 euros`.
- It has two decimals, such as `14.90`, unless a unit follows.
- It follows a word like `at`, `only`, `just`, `costs` or `price`, unless a unit follows.

Decimal commas and thousands separators are handled (`1.299,00`).

## What is kept

- `Solid choice at 19.90` is kept (right price).
- `2 m long`, `30-hour battery`, `Only 30 hours` and `20% off` are kept (other numbers).
- If a reason contains two prices and one is wrong (`Was 24.90, now 19.90`), the whole reason is dropped.

## Known limits

- A bare number with no currency, no two decimals and no price word, such as "Cheap, 14 for the pair", is not recognised as a price and is kept.
- A reason cut off by the 80-character limit is checked as shown, so `€129.00` cut to `€12` is blanked rather than shown as a wrong price.

The README doesn't mention this behaviour yet; I can add a line if you want.