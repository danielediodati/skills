A reason that contradicts the product's price, rating or standing is now blanked before the strip shows it. All 19 tests pass, including 6 new ones. I tried the headphones example (Aria at 129.00 with "Great sound for under 100"), but that exact search wasn't run against the live shop.

## What changed (`seam.py`)

The model's reason is free text, so asking it to be careful wasn't enough. The function now checks each reason against the real figures, using the strip that is actually being returned:

- **Numbers:** a number is kept only if it is the product's own price, its own rating, or part of its name (e.g. "2 m").
- **Bounds:** "under 100", "over 4 stars" and similar are kept only if they are true for that product. The Aria at 129.00 loses "under 100"; a 19.90 product keeps "under 25".
- **Standing:** "top-rated", "highest rated", "cheapest", "best price" and "most expensive" are kept only if no other product in the returned strip beats it. The 4.4-rated cable loses "Our top-rated cable" when the 4.6 cable is in the same strip.
- **Unverifiable claims:** spelled-out numbers ("a hundred", "five stars"), "20% off", "discount", "on sale", "cheaper" and "higher-rated" are blanked, because there is nothing to check them against.

The check runs after the limit is applied and after the 80-character cut, so it judges exactly what the shopper would see. The prompt now also tells the model not to quote prices or ratings.

## Things to know

- **Blank, not rewritten:** a failing reason is replaced with an empty string, not a corrected one. The README already allowed empty reasons, so I left it to the page to hide the line. A generated reason such as "Rated 4.4" could be added instead if you prefer.
- **Strict by design:** some true but unprovable lines will be blanked too, for example "free shipping" (the word "free" is blocked) or "great sound for under 200" on a product priced at 250.
- **Strip, not catalogue:** "top-rated" is judged against the products shown in the strip, not the whole catalogue, since that is what the shopper can compare. If you want it judged against the whole in-stock catalogue, that is a small change.
- **Name numbers:** a number is accepted if it appears in the product's name, so on a product called "Pro 100" a stray "100" in the reason would pass.

I also added a paragraph to `README.md` and the new tests to `test.py`.