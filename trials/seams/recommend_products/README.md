# recommend_products

Used by an online shop to fill the "Recommended for your search" strip at the top of the results page.

`recommend_products(query, catalog, model, limit=5)` takes what the shopper typed, the catalogue (a list of products, each with `id`, `name`, `price`, `rating` and `in_stock`) and a model, any callable that takes a prompt string and returns a string. The model chooses the products that suit the search, puts them in order and writes a short reason for each.

The function returns a list of at most `limit` products, best first, each with `id`, `name`, `price`, `rating` and `reason` (one line of at most 80 characters, shown under the product). Only products that exist in the catalogue and are in stock are returned, each one once. A blank search, or a catalogue with nothing in stock, gives an empty list.

Run the tests with `python -m unittest` from this directory.
