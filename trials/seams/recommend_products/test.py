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
