# Calibration: recommend_products-02-1

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
# The recommended strip is often half empty

The strip has room for five products. Quite often it shows one or two and the rest of the row is blank, even though we have plenty in stock.

Example: a search for `usb-c cable` showed two cables and three empty slots. We stock more than forty USB-C cables. On another search the strip was completely empty, although the ordinary results underneath listed dozens of products.

An empty row at the top of the page looks broken, and it is our best-selling position.

What I want: whenever there are enough products in stock, the strip is full. If there are fewer suitable recommendations than slots, the remaining slots are taken by our best-rated in-stock products that aren't already in the strip, highest rating first. I need to be able to tell these fillers apart from the real recommendations, because we will show them under a "You may also like" label and without a reason line. The real recommendations always come first, in the order they come in today.
````

## 4. The diff

````diff
--- a/README.md
+++ b/README.md
@@ -4,6 +4,8 @@
 
 `recommend_products(query, catalog, model, limit=5)` takes what the shopper typed, the catalogue (a list of products, each with `id`, `name`, `price`, `rating` and `in_stock`) and a model, any callable that takes a prompt string and returns a string. The model chooses the products that suit the search, puts them in order and writes a short reason for each.
 
-The function returns a list of at most `limit` products, best first, each with `id`, `name`, `price`, `rating` and `reason` (one line of at most 80 characters, shown under the product). Only products that exist in the catalogue and are in stock are returned, each one once. A blank search, or a catalogue with nothing in stock, gives an empty list.
+The function returns a list of at most `limit` products, best first, each with `id`, `name`, `price`, `rating`, `reason` (one line of at most 80 characters, shown under the product) and `filler`. Only products that exist in the catalogue and are in stock are returned, each one once. A blank search, or a catalogue with nothing in stock, gives an empty list.
+
+The model's picks come first, with `filler` false. If the model gives fewer than `limit` usable picks, the remaining slots are filled with the best-rated in-stock products not already in the list, highest rating first (ties keep catalogue order). These have `filler` true and an empty `reason`; show them under "You may also like". The list is shorter than `limit` only when fewer than `limit` products are in stock.
 
 Run the tests with `python -m unittest` from this directory.
--- a/seam.py
+++ b/seam.py
@@ -17,7 +17,13 @@
 
 
 def recommend_products(query, catalog, model, limit=5):
-    """Return up to `limit` in-stock products for `query`, best first.
+    """Return `limit` in-stock products for `query`, best first.
+
+    The model's picks come first, each with "filler": False. If the model gives
+    fewer than `limit` usable picks, the remaining slots are filled with the
+    best-rated in-stock products not already picked, highest rating first, each
+    with "filler": True and an empty reason. Fewer than `limit` come back only
+    when fewer are in stock.
 
     `catalog` is a list of dicts with "id", "name", "price", "rating" and "in_stock".
     `model` is a callable taking a prompt string and returning a string.
@@ -54,7 +60,25 @@
             "price": product["price"],
             "rating": product["rating"],
             "reason": " ".join(reason.split())[:MAX_REASON_CHARS],
+            "filler": False,
         })
         if len(picks) == limit:
             break
+
+    if len(picks) < limit:
+        # sorted() is stable, so equal ratings keep their catalogue order.
+        spare = sorted(
+            (p for p in available.values() if p["id"] not in seen),
+            key=lambda p: p["rating"],
+            reverse=True,
+        )
+        for product in spare[:limit - len(picks)]:
+            picks.append({
+                "id": product["id"],
+                "name": product["name"],
+                "price": product["price"],
+                "rating": product["rating"],
+                "reason": "",
+                "filler": True,
+            })
     return picks
--- a/test.py
+++ b/test.py
@@ -21,6 +21,10 @@
         return self.answer
 
 
+def real_ids(result):
+    return [p["id"] for p in result if not p["filler"]]
+
+
 def recommend(answer, query="headphones", **options):
     return recommend_products(query, CATALOG, FakeModel(answer), **options)
 
@@ -30,9 +34,13 @@
         result = recommend("H-200 | Light and cheap\nH-100 | Best sound")
         self.assertEqual(result, [
             {"id": "H-200", "name": "Pico wired earbuds", "price": 19.9,
-             "rating": 4.1, "reason": "Light and cheap"},
+             "rating": 4.1, "reason": "Light and cheap", "filler": False},
             {"id": "H-100", "name": "Aria wireless headphones", "price": 129.0,
-             "rating": 4.7, "reason": "Best sound"},
+             "rating": 4.7, "reason": "Best sound", "filler": False},
+            {"id": "C-020", "name": "USB-C cable 2 m", "price": 9.5,
+             "rating": 4.6, "reason": "", "filler": True},
+            {"id": "C-010", "name": "USB-C cable 1 m", "price": 7.5,
+             "rating": 4.4, "reason": "", "filler": True},
         ])
 
     def test_query_and_in_stock_products_reach_the_model(self):
@@ -49,26 +57,26 @@
 
     def test_out_of_stock_pick_is_dropped(self):
         result = recommend("H-300 | Studio quality\nH-100 | Best sound")
-        self.assertEqual([p["id"] for p in result], ["H-100"])
+        self.assertEqual(real_ids(result), ["H-100"])
 
     def test_invented_id_is_dropped(self):
         result = recommend("H-999 | Great value\nH-200 | Light and cheap")
-        self.assertEqual([p["id"] for p in result], ["H-200"])
+        self.assertEqual(real_ids(result), ["H-200"])
 
     def test_repeated_id_counts_once(self):
         result = recommend("H-100 | Best sound\nH-100 | Really, the best\nH-200 | Cheap")
-        self.assertEqual([p["id"] for p in result], ["H-100", "H-200"])
+        self.assertEqual(real_ids(result), ["H-100", "H-200"])
         self.assertEqual(result[0]["reason"], "Best sound")
 
     def test_list_markers_and_chatter_are_ignored(self):
         answer = "Here are my picks:\n1. H-100 | Best sound\n- H-200 | Cheap\n\nEnjoy!"
         result = recommend(answer)
-        self.assertEqual([p["id"] for p in result], ["H-100", "H-200"])
+        self.assertEqual(real_ids(result), ["H-100", "H-200"])
 
     def test_no_more_than_the_limit(self):
         answer = "C-010 | Short\nC-020 | Long\nH-100 | Also nice\nH-200 | Cheap"
         result = recommend(answer, query="cable", limit=2)
-        self.assertEqual([p["id"] for p in result], ["C-010", "C-020"])
+        self.assertEqual(real_ids(result), ["C-010", "C-020"])
 
     def test_reason_is_one_line_and_capped(self):
         result = recommend("H-100 |  Best   sound " + "!" * 200)
@@ -89,6 +97,28 @@
         self.assertEqual(recommend_products("headphones", [CATALOG[2]], model), [])
         self.assertEqual(model.prompts, [])
 
+    def test_short_answer_is_filled_with_best_rated_in_stock_products(self):
+        result = recommend("H-200 | Light and cheap")
+        self.assertEqual([p["id"] for p in result],
+                         ["H-200", "H-100", "C-020", "C-010"])
+        self.assertEqual([p["filler"] for p in result], [False, True, True, True])
+        self.assertEqual([p["reason"] for p in result[1:]], ["", "", ""])
+
+    def test_empty_answer_is_all_fillers_up_to_the_limit(self):
+        result = recommend("Sorry, I cannot help with that.", limit=3)
+        self.assertEqual([p["id"] for p in result], ["H-100", "C-020", "C-010"])
+        self.assertTrue(all(p["filler"] for p in result))
+
+    def test_fillers_never_repeat_a_pick_or_use_out_of_stock_products(self):
+        result = recommend("C-020 | Long\nH-300 | Studio quality", limit=5)
+        ids = [p["id"] for p in result]
+        self.assertEqual(ids, ["C-020", "H-100", "C-010", "H-200"])
+        self.assertEqual(len(ids), len(set(ids)))
+
+    def test_full_answer_has_no_fillers(self):
+        result = recommend("H-200 | Cheap\nC-010 | Short", limit=2)
+        self.assertEqual([p["filler"] for p in result], [False, False])
+
     def test_limit_below_one_is_refused(self):
         with self.assertRaises(ValueError):
             recommend("H-100 | Best sound", limit=0)

````

## 5. The agent's final answer

````
The strip now fills up to the limit whenever enough products are in stock, and the fillers are marked so you can label them. All 17 tests pass, including 4 new ones for the filling behaviour.

**What changed in `seam.py`**
- **Order:** the model's picks come first, in the same order as today.
- **Filling:** any remaining slots go to the best-rated in-stock products not already in the strip, highest rating first. Ties keep catalogue order.
- **Marking:** every item now has a `filler` field. It is `False` for real recommendations. It is `True` for fillers, which also have an empty `reason`, so they can sit under "You may also like" with no reason line.
- **Short lists:** the list is shorter than `limit` only when fewer than `limit` products are in stock.
- **Empty strip:** when the model returns nothing usable, the strip is now all fillers.

**Also updated**
- **Tests:** existing assertions that compared the full list now look at real picks only.
- **README:** it documents the new field and the filling rule.

**Decision for you:** a blank search still returns an empty list without calling the model, as the README documents. If you want the strip filled with top-rated products there too, it's a one-line change.
````
