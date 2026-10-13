I changed the prompt in `seam.py` so the model writes every amount as a plain decimal with a period and no thousands separators, whatever notation the invoice uses. The tests pass, but I couldn't run a real model here, so I haven't confirmed that Kessler KW-10482 now comes through with a total of 1250.00.

- **Why it failed:** the model copied "1.250,00" from the page as-is, and the code, correctly, refused it as not a number.
- **What the prompt now says:** amounts are plain decimals, with "1.250,00" and "1,250.00" both given as examples of 1250.00. Writing numbers in a normalised form is the same job the model already does for dates, which the charter leaves to it.
- **Parser unchanged:** the "not a number" check in code is still strict, and I deliberately didn't make it understand European notation. A value like "1.250" is ambiguous on its own (1250 or 1.25), and the charter says a wrong ledger entry costs more than a refused one.
- **If the model still misreads:** the invoice is refused as before, or lands as `mismatch` for a clerk if the figures don't add up. It won't be loaded with wrong amounts.
- **Test added:** I added `test_prompt_asks_for_plain_decimal_numbers` in `test.py`, which only checks that the instruction is in the prompt.

The charter was not touched.