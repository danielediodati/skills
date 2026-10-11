A reason that quotes a price different from the product's actual price is now blanked, and the product stays in the strip. All 16 tests pass, including the new ones.

**What counts as a price**

A number in the reason is treated as a price when it is:
- next to a currency (`€14.90`, `$4`, `15 euros`, `19.90 EUR`);
- written with two decimals (`14,90`);
- right after a price word such as `at`, `only`, `just`, `for` or `costs`, and not followed by a unit.

Every price found must equal the product's price. Both `.` and `,` decimals are accepted. The check runs on the 80-character text that is actually shown.

**Examples**

| Reason | Product price | Result |
|---|---|---|
| "A bargain at only €14.90" | 19.90 | reason blanked |
| "Just $4" | 19.90 | reason blanked |
| "Solid choice at 19.90" | 19.90 | kept |
| "2 m long" | 19.90 | kept |
| "30-hour battery" | 19.90 | kept |
| "Rated 4.5 stars" | 19.90 | kept |

**Limits**

This is a pattern check, not a full parse of the reason:
- A bare number with no currency, no price word and no two decimals is not treated as a price, for example "Great value, 15 for a pair".
- Written-out prices ("fifteen euros") are not caught.
- A number written like a price will be blanked if it is not the product's price, for example "4.50" in a reason about ratings.

The change is in `seam.py`, and the new tests are in `test.py`.