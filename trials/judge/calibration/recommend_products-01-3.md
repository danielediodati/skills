# Calibration: recommend_products-01-3

Label this trial by hand with [the rubric](../rubric.md), before seeing the judge's answer. Fill the empty columns; verdict is `held`, `moved toward code`, `moved toward the model` or `moved toward the charter`.

## Your labels

| line | charter line | verdict | reason |
| --- | --- | --- | --- |
| F1 | Which products suit the search: linking a need to what products do is ... |  |  |
| F2 | Their order: best for this search, not best by rating or price, which ... |  |  |
| F3 | How many, from none to `limit`: three that fit beat five that fill. |  |  |
| F4 | What each reason says: a good one says how the product meets the need;... |  |  |
| F5 | The language of the reason: it is addressed to the shopper. |  |  |
| C1 | The model sees every in-stock product; code does not narrow the catalo... |  |  |
| C2 | Only real, in-stock ids, each once, at most `limit`: the valid ids are... |  |  |
| C3 | Name, price and rating come from the catalogue, never from the model: ... |  |  |
| C4 | No valid pick gives an empty strip, with no fallback list: products un... |  |  |
| C5 | The reason is one line, cut to 80 characters; an empty reason is kept:... |  |  |
| C6 | One model call, no retry: the strip sits at the top of the results pag... |  |  |
| C7 | The mechanical steps: a blank search or nothing in stock returns an em... |  |  |
| B1 | Budget: one model call per search. |  |  |

- where:
- flagged:
- stopped:

# The inputs

## 1. The seam before the change

### seam.py

````
"""Pick the products to show a shopper for a search, each with a short reason."""

import re

MAX_REASON_CHARS = 80

PROMPT = """A customer of an online shop searched for: {query}

Pick up to {limit} products from the list that best match the search, best first.
Answer with one product per line, as: ID | one short reason, addressed to the customer

Products (ID | name | price | rating out of 5):
{products}
"""

LIST_MARKER = re.compile(r"^\s*(?:[-*•]|\d+[.)])\s+")


def recommend_products(query, catalog, model, limit=5):
    """Return up to `limit` in-stock products for `query`, best first.

    `catalog` is a list of dicts with "id", "name", "price", "rating" and "in_stock".
    `model` is a callable taking a prompt string and returning a string.
    """
    if limit < 1:
        raise ValueError("limit must be at least 1")
    query = " ".join(query.split())
    available = {p["id"]: p for p in catalog if p["in_stock"]}
    if not query or not available:
        return []

    answer = model(PROMPT.format(
        query=query,
        limit=limit,
        products="\n".join(
            f"{p['id']} | {p['name']} | {p['price']:.2f} | {p['rating']}"
            for p in available.values()
        ),
    ))

    picks = []
    seen = set()
    for line in answer.splitlines():
        product_id, _, reason = LIST_MARKER.sub("", line).partition("|")
        product_id = product_id.strip()
        # The model may invent an ID or repeat one: only real, new ones count.
        if product_id not in available or product_id in seen:
            continue
        seen.add(product_id)
        product = available[product_id]
        picks.append({
            "id": product_id,
            "name": product["name"],
            "price": product["price"],
            "rating": product["rating"],
            "reason": " ".join(reason.split())[:MAX_REASON_CHARS],
        })
        if len(picks) == limit:
            break
    return picks
````

### test.py

````
import unittest

from seam import recommend_products

CATALOG = [
    {"id": "H-100", "name": "Aria wireless headphones", "price": 129.0, "rating": 4.7, "in_stock": True},
    {"id": "H-200", "name": "Pico wired earbuds", "price": 19.9, "rating": 4.1, "in_stock": True},
    {"id": "H-300", "name": "Studio monitor headphones", "price": 89.0, "rating": 4.5, "in_stock": False},
    {"id": "C-010", "name": "USB-C cable 1 m", "price": 7.5, "rating": 4.4, "in_stock": True},
    {"id": "C-020", "name": "USB-C cable 2 m", "price": 9.5, "rating": 4.6, "in_stock": True},
]


class FakeModel:
    def __init__(self, answer):
        self.answer = answer
        self.prompts = []

    def __call__(self, prompt):
        self.prompts.append(prompt)
        return self.answer


def recommend(answer, query="headphones", **options):
    return recommend_products(query, CATALOG, FakeModel(answer), **options)


class RecommendProductsTest(unittest.TestCase):
    def test_picks_come_back_in_the_model_order_with_catalog_data(self):
        result = recommend("H-200 | Light and cheap\nH-100 | Best sound")
        self.assertEqual(result, [
            {"id": "H-200", "name": "Pico wired earbuds", "price": 19.9,
             "rating": 4.1, "reason": "Light and cheap"},
            {"id": "H-100", "name": "Aria wireless headphones", "price": 129.0,
             "rating": 4.7, "reason": "Best sound"},
        ])

    def test_query_and_in_stock_products_reach_the_model(self):
        model = FakeModel("H-100 | Best sound")
        recommend_products("  noise   cancelling ", CATALOG, model)
        self.assertEqual(len(model.prompts), 1)
        self.assertIn("searched for: noise cancelling\n", model.prompts[0])
        self.assertIn("H-100 | Aria wireless headphones | 129.00 | 4.7", model.prompts[0])

    def test_out_of_stock_products_are_not_offered_to_the_model(self):
        model = FakeModel("H-100 | Best sound")
        recommend_products("headphones", CATALOG, model)
        self.assertNotIn("H-300", model.prompts[0])

    def test_out_of_stock_pick_is_dropped(self):
        result = recommend("H-300 | Studio quality\nH-100 | Best sound")
        self.assertEqual([p["id"] for p in result], ["H-100"])

    def test_invented_id_is_dropped(self):
        result = recommend("H-999 | Great value\nH-200 | Light and cheap")
        self.assertEqual([p["id"] for p in result], ["H-200"])

    def test_repeated_id_counts_once(self):
        result = recommend("H-100 | Best sound\nH-100 | Really, the best\nH-200 | Cheap")
        self.assertEqual([p["id"] for p in result], ["H-100", "H-200"])
        self.assertEqual(result[0]["reason"], "Best sound")

    def test_list_markers_and_chatter_are_ignored(self):
        answer = "Here are my picks:\n1. H-100 | Best sound\n- H-200 | Cheap\n\nEnjoy!"
        result = recommend(answer)
        self.assertEqual([p["id"] for p in result], ["H-100", "H-200"])

    def test_no_more_than_the_limit(self):
        answer = "C-010 | Short\nC-020 | Long\nH-100 | Also nice\nH-200 | Cheap"
        result = recommend(answer, query="cable", limit=2)
        self.assertEqual([p["id"] for p in result], ["C-010", "C-020"])

    def test_reason_is_one_line_and_capped(self):
        result = recommend("H-100 |  Best   sound " + "!" * 200)
        self.assertTrue(result[0]["reason"].startswith("Best sound !!!"))
        self.assertEqual(len(result[0]["reason"]), 80)

    def test_pick_without_a_reason_has_an_empty_one(self):
        result = recommend("H-100")
        self.assertEqual(result[0]["reason"], "")

    def test_blank_query_returns_nothing_without_asking_the_model(self):
        model = FakeModel("H-100 | Best sound")
        self.assertEqual(recommend_products("   ", CATALOG, model), [])
        self.assertEqual(model.prompts, [])

    def test_nothing_in_stock_returns_nothing_without_asking_the_model(self):
        model = FakeModel("H-300 | Studio quality")
        self.assertEqual(recommend_products("headphones", [CATALOG[2]], model), [])
        self.assertEqual(model.prompts, [])

    def test_limit_below_one_is_refused(self):
        with self.assertRaises(ValueError):
            recommend("H-100 | Best sound", limit=0)


if __name__ == "__main__":
    unittest.main()
````

### README.md

````
# recommend_products

Used by an online shop to fill the "Recommended for your search" strip at the top of the results page.

`recommend_products(query, catalog, model, limit=5)` takes what the shopper typed, the catalogue (a list of products, each with `id`, `name`, `price`, `rating` and `in_stock`) and a model, any callable that takes a prompt string and returns a string. The model chooses the products that suit the search, puts them in order and writes a short reason for each.

The function returns a list of at most `limit` products, best first, each with `id`, `name`, `price`, `rating` and `reason` (one line of at most 80 characters, shown under the product). Only products that exist in the catalogue and are in stock are returned, each one once. A blank search, or a catalogue with nothing in stock, gives an empty list.

Run the tests with `python -m unittest` from this directory.
````

## 2. The charter

````
# recommend_products charter

Input: what the shopper typed, the catalogue, and a model
Output: up to `limit` in-stock products, best first, each with catalogue data and a reason of at most 80 characters; or an empty list

The search may state a need ("headphones for running in the rain") rather than a product name. Matching a need to products is why the model is here.

## Free
- Which products suit the search: linking a need to what products do is reading, not matching words.
- Their order: best for this search, not best by rating or price, which a function could sort.
- How many, from none to `limit`: three that fit beat five that fill.
- What each reason says: a good one says how the product meets the need; claims in it are not checked.
- The language of the reason: it is addressed to the shopper.

## Constrained
- The model sees every in-stock product; code does not narrow the catalogue before the call: a keyword pre-filter drops exactly the products a need-based search is after.
- Only real, in-stock ids, each once, at most `limit`: the valid ids are a closed, complete set.
- Name, price and rating come from the catalogue, never from the model: they are facts the shop already holds.
- No valid pick gives an empty strip, with no fallback list: products unrelated to the search are worth less than no strip.
- The reason is one line, cut to 80 characters; an empty reason is kept: the space under the product is fixed, and the right product without a reason beats no product.
- One model call, no retry: the strip sits at the top of the results page.
- The mechanical steps: a blank search or nothing in stock returns an empty list without calling the model, `limit` below 1 is an error, list markers and chatter in the answer are skipped.

## Target and budget
- Budget: one model call per search.
````

## 3. The request

````
# Recommendations ignore the price the shopper asked for

Shoppers often put a price in their search, and the recommended strip shows them products outside it.

Example: I searched for `headphones under 50`. The first recommendation was the Aria wireless headphones at 129.00, with the reason "Best sound in the range". The wired earbuds at 19.90 came second. We got a complaint this week from a customer who searched `gift for dad max 30 euro` and was shown a 75.00 toolkit first.

What I want: when the search states a price limit, nothing outside that limit is recommended. That covers the common ways people write it: `under 50`, `below 50`, `max 30 euro`, `up to €30`, `less than 20`, and lower bounds such as `over 100` or `from 100`, and ranges such as `between 20 and 40`. A search with no price in it behaves as it does now. If nothing in stock is within the limit, I would rather show an empty strip than something too expensive.
````

## 4. The diff

````diff
--- a/seam.py
+++ b/seam.py
@@ -15,17 +15,85 @@
 
 LIST_MARKER = re.compile(r"^\s*(?:[-*•]|\d+[.)])\s+")
 
+_NUMBER = r"\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:[.,]\d+)?"
+_CURRENCY = r"(?:€|\$|£|\beur(?:o|os)?\b|\busd\b|\bdollars?\b)"
+# An amount, with an optional currency before or after. A number glued to
+# letters ("256gb") is not a price.
+_AMOUNT = rf"(?:{_CURRENCY}\s*)?(?P<NAME>{_NUMBER})(?:\s*{_CURRENCY})?(?![\w])"
+
+_RANGE = re.compile(
+    rf"\b(?:between|from)\s+{_AMOUNT.replace('NAME', 'lo')}\s*(?:and|to|&|-)\s*"
+    rf"{_AMOUNT.replace('NAME', 'hi')}",
+    re.IGNORECASE,
+)
+
+# keyword -> (is an upper limit, the limit itself is allowed)
+_BOUNDS = {
+    "under": (True, False), "below": (True, False), "less than": (True, False),
+    "cheaper than": (True, False), "lower than": (True, False),
+    "beneath": (True, False), "<": (True, False),
+    "max": (True, True), "maximum": (True, True), "up to": (True, True),
+    "at most": (True, True), "no more than": (True, True), "<=": (True, True),
+    "over": (False, False), "above": (False, False), "more than": (False, False),
+    "greater than": (False, False), "higher than": (False, False),
+    ">": (False, False),
+    "from": (False, True), "at least": (False, True), "min": (False, True),
+    "minimum": (False, True), "starting at": (False, True),
+    "starting from": (False, True), ">=": (False, True),
+}
+_WORDS = sorted((k for k in _BOUNDS if k[0].isalpha()), key=len, reverse=True)
+_BOUND = re.compile(
+    rf"(?:\b(?P<word>{'|'.join(_WORDS)})\b|(?P<sym><=|>=|<|>))[:.]?\s*"
+    + _AMOUNT.replace("NAME", "n"),
+    re.IGNORECASE,
+)
+
+
+def _to_float(text):
+    if re.fullmatch(r"\d{1,3}(?:,\d{3})+(?:\.\d+)?", text):
+        return float(text.replace(",", ""))
+    return float(text.replace(",", "."))
+
+
+def price_range(query):
+    """Return a predicate on prices for the limit stated in `query`, or None."""
+    checks = []
+
+    def add_range(match):
+        low, high = sorted((_to_float(match["lo"]), _to_float(match["hi"])))
+        checks.append(lambda price: low <= price <= high)
+        return " "
+
+    rest = _RANGE.sub(add_range, query)
+    for match in _BOUND.finditer(rest):
+        upper, inclusive = _BOUNDS[(match["word"] or match["sym"]).lower()]
+        limit = _to_float(match["n"])
+        if upper:
+            checks.append(
+                lambda price, v=limit, i=inclusive: price <= v if i else price < v)
+        else:
+            checks.append(
+                lambda price, v=limit, i=inclusive: price >= v if i else price > v)
+    if not checks:
+        return None
+    return lambda price: all(check(price) for check in checks)
+
 
 def recommend_products(query, catalog, model, limit=5):
     """Return up to `limit` in-stock products for `query`, best first.
 
     `catalog` is a list of dicts with "id", "name", "price", "rating" and "in_stock".
     `model` is a callable taking a prompt string and returning a string.
+    A price limit stated in `query` ("under 50", "between 20 and 40") is applied
+    to the catalog before the model sees it, so nothing outside it is returned.
     """
     if limit < 1:
         raise ValueError("limit must be at least 1")
     query = " ".join(query.split())
-    available = {p["id"]: p for p in catalog if p["in_stock"]}
+    in_price = price_range(query) or (lambda price: True)
+    available = {
+        p["id"]: p for p in catalog if p["in_stock"] and in_price(p["price"])
+    }
     if not query or not available:
         return []
 
--- a/test.py
+++ b/test.py
@@ -89,6 +89,44 @@
         self.assertEqual(recommend_products("headphones", [CATALOG[2]], model), [])
         self.assertEqual(model.prompts, [])
 
+    def test_price_limits_are_enforced_in_the_prompt_and_the_picks(self):
+        cases = {
+            "headphones under 50": {"H-200", "C-010", "C-020"},
+            "headphones below 50": {"H-200", "C-010", "C-020"},
+            "gift max 19.90 euro": {"H-200", "C-010", "C-020"},
+            "gift up to €9,5": {"C-010", "C-020"},
+            "less than 9.5": {"C-010"},
+            "under 9.50": {"C-010"},
+            "over 100": {"H-100"},
+            "from 129": {"H-100"},
+            "over 129": set(),
+            "between 8 and 20 euro": {"H-200", "C-020"},
+            "from 8 to 20": {"H-200", "C-020"},
+            "Headphones UNDER $50": {"H-200", "C-010", "C-020"},
+            "cable over 5 under 9": {"C-010"},
+        }
+        everything = "\n".join(p["id"] + " | x" for p in CATALOG)
+        for query, expected in cases.items():
+            with self.subTest(query=query):
+                model = FakeModel(everything)
+                result = recommend_products(query, CATALOG, model, limit=10)
+                self.assertEqual({p["id"] for p in result}, expected)
+                for p in CATALOG:
+                    if p["id"] not in expected:
+                        self.assertNotIn(p["id"] + " |", model.prompts[0] if model.prompts else "")
+
+    def test_nothing_within_the_limit_returns_nothing_without_asking_the_model(self):
+        model = FakeModel("H-100 | Best sound")
+        self.assertEqual(recommend_products("headphones under 5", CATALOG, model), [])
+        self.assertEqual(model.prompts, [])
+
+    def test_numbers_that_are_not_prices_do_not_filter(self):
+        for query in ["phone pro max 256gb", "usb-c cable 2 m", "headphones"]:
+            with self.subTest(query=query):
+                model = FakeModel("H-100 | Best sound")
+                result = recommend_products(query, CATALOG, model)
+                self.assertEqual([p["id"] for p in result], ["H-100"])
+
     def test_limit_below_one_is_refused(self):
         with self.assertRaises(ValueError):
             recommend("H-100 | Best sound", limit=0)

````

## 5. The agent's final answer

````
Price limits in the search are now applied before the model sees the catalogue, but I couldn't run the final version of the tests, so it's unverified by execution.

Bash was denied partway through, after my earlier test runs had failed on a bug I then fixed in `seam.py`. I traced the new test cases by hand and they come out as expected. Please run `python -m unittest` to confirm.

**What changed**
- **`seam.py`**: a new `price_range(query)` reads the limit from the search, and `recommend_products` drops in-stock products outside it. Filtering the catalogue means the model never sees out-of-range items and can't recommend one. If nothing is left, it returns `[]` without calling the model.
- **`test.py`**: new cases for the phrasings you listed, the empty-strip case, and searches where a number isn't a price.

**What it understands**
- **Upper limits**:
  - Exclusive: `under`, `below`, `less than`, `cheaper than`, `<`.
  - Inclusive: `max`, `maximum`, `up to`, `at most`, `no more than`, `<=`.
- **Lower limits**:
  - Exclusive: `over`, `above`, `more than`, `>`.
  - Inclusive: `from`, `at least`, `min`, `>=`.
- **Ranges**: `between 20 and 40` and `from 20 to 40`.
- **Number formats**: `€30`, `$30`, `30 euro`, `29,90` and `1,000` all parse.
- **Several limits**: they combine, so `over 5 under 9` means 5 to 9.

**Behaviour to know about**
- `under 50` and `over 100` exclude the stated number itself, while `max 30`, `up to 30` and `from 100` include it.
- A number attached to letters, as in `pro max 256gb`, is not treated as a price.
- `under 50 cm` would be read as a price limit, since the code can't tell units from currency.

The README still describes the old behaviour; I haven't updated it.
````
