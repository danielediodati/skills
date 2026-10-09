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
