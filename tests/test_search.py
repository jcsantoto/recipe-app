import unittest
from src import search
import requests


class SearchByNameTests(unittest.TestCase):
    search_pizza = search.search_by_name("pizza")
    search_gibberish = search.search_by_name("dhsyufgabfba4478fh4a8fbaewkdjfs")
    search_twenty = search.search_by_name("cake", 20)
    search_blank = search.search_by_name("")

    def test_search_name_not_empty_given_reasonable_query(self):
        self.assertNotEqual(len(self.search_pizza), 0)

    def test_search_name_empty_given_unreasonable_query(self):
        self.assertEqual(len(self.search_gibberish), 0)

    def test_search_name_returns_ten_results_by_default(self):
        self.assertEqual(len(self.search_pizza), 10)

    def test_search_name_returns_specified_number_of_results(self):
        self.assertEqual(len(self.search_twenty), 20)

    def test_search_name_with_blank_is_invalid(self):
        self.assertEqual(len(self.search_blank), 0)


class SearchByIngredientTest(unittest.TestCase):
    search_apples_milk = search.search_by_ingredient("apples,milk")
    search_gibberish = search.search_by_ingredient("fdajhfdsjkfhdsjakfhueawhfd-fa324723849")
    search_thirty = search.search_by_ingredient("flour,water", 30)
    search_blank = search.search_by_ingredient("")

    def test_search_ingredient_not_empty_given_reasonable_query(self):
        self.assertNotEqual(len(self.search_apples_milk), 0)

    def test_search_ingredient_empty_given_unreasonable_query(self):
        self.assertEqual(len(self.search_gibberish), 0)

    def test_search_ingredient_returns_ten_results_by_default(self):
        self.assertEqual(len(self.search_apples_milk), 10)

    def test_search_ingredient_returns_specified_number_of_results(self):
        self.assertEqual(len(self.search_thirty), 30)

    def test_search_ingredient_with_blank_is_invalid(self):
        self.assertEqual(len(self.search_blank), 0)

    def test_search_ingredient_actually_contains_specified_ingredients(self):
        ids = ",".join([str(x['id']) for x in self.search_apples_milk])

        url = "https://api.spoonacular.com/recipes/informationBulk?ids=" + ids + search.APIKEY

        bulk_info = requests.get(url).json()

        recipes_ingredients = [x["extendedIngredients"] for x in bulk_info]

        for recipe in recipes_ingredients:
            ingredients = ",".join([x["name"] for x in recipe])
            self.assertTrue("apple" in ingredients or "milk" in ingredients)


class FilterByPriceTest(unittest.TestCase):
    search_cake = search.filter_by_price_range("cake", 0, 5)
    search_gibberish = search.filter_by_price_range("fdajhfdsjkfhdsjakfhueawhfd-fa324723849", 2, 4)
    search_thirty = search.filter_by_price_range("cake", 0, 20, 30)
    search_blank = search.filter_by_price_range("", 4, 40)
    search_invalid_range = search.filter_by_price_range("cake", 5, 2)

    def test_filter_by_price_not_empty_given_reasonable_query(self):
        self.assertNotEqual(len(self.search_cake), 0)

    def test_filter_by_price_empty_given_unreasonable_query(self):
        self.assertEqual(len(self.search_gibberish), 0)

    def test_filter_by_price_returns_ten_results_by_default(self):
        self.assertEqual(len(self.search_cake), 10)

    def test_filter_by_price_returns_specified_number_of_results(self):
        self.assertEqual(len(self.search_thirty), 30)

    def test_filter_by_price_recipes_are_within_price_range(self):
        prices = [x["price"] for x in self.search_cake]
        for p in prices:
            self.assertTrue(0 < p < 20)

    def test_filter_by_price_with_blank_is_invalid(self):
        self.assertEqual(len(self.search_blank), 0)

    def test_filter_by_price_with_invalid_range_is_invalid(self):
        self.assertEqual(len(self.search_invalid_range), 0)


if __name__ == '__main__':
    unittest.main()
