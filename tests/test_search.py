import unittest
from src import search
import requests


class SearchByNameTests(unittest.TestCase):
    recipes = search.search_by_name("pizza")
    blank = search.search_by_name("dhsyufgabfba4478fh4a8fbaewkdjfs")
    twenty = search.search_by_name("cake", 20)

    def test_search_name_not_empty_given_reasonable_query(self):
        self.assertNotEqual(len(self.recipes), 0)

    def test_search_name_empty_given_unreasonable_query(self):
        self.assertEqual(len(self.blank), 0)

    def test_search_name_returns_ten_results_by_default(self):
        self.assertEqual(len(self.recipes), 10)

    def test_search_name_returns_specified_number_of_results(self):
        self.assertEqual(len(self.twenty), 20)


class SearchByIngredientTest(unittest.TestCase):
    recipes = search.search_by_ingredient("apples,milk")
    blank = search.search_by_ingredient("fdajhfdsjkfhdsjakfhueawhfd-fa324723849")
    thirty = search.search_by_ingredient("flour,water", 30)

    def test_search_ingredient_not_empty_given_reasonable_query(self):
        self.assertNotEqual(len(self.recipes), 0)

    def test_search_ingredient_empty_given_unreasonable_query(self):
        self.assertEqual(len(self.blank), 0)

    def test_search_ingredient_returns_ten_results_by_default(self):
        self.assertEqual(len(self.recipes), 10)

    def test_search_ingredient_returns_specified_number_of_results(self):
        self.assertEqual(len(self.thirty), 30)

    def test_search_ingredient_actually_contains_specified_ingredients(self):
        ids = ",".join([str(x['id']) for x in self.recipes])

        url = "https://api.spoonacular.com/recipes/informationBulk?ids=" + ids + search.APIKEY

        bulk_info = requests.get(url).json()

        recipes_ingredients = [x["extendedIngredients"] for x in bulk_info]

        for recipe in recipes_ingredients:
            ingredients = ",".join([x["name"] for x in recipe])
            self.assertTrue("apple" in ingredients or "milk" in ingredients)


class FilterByPriceTest(unittest.TestCase):
    recipes = search.filter_by_price_range("cake", 0, 5)
    blank = search.filter_by_price_range("fdajhfdsjkfhdsjakfhueawhfd-fa324723849", 2, 4)
    thirty = search.filter_by_price_range("cake", 0, 20, 30)

    def test_filter_by_price_not_empty_given_reasonable_query(self):
        self.assertNotEqual(len(self.recipes), 0)

    def test_filter_by_price_empty_given_unreasonable_query(self):
        self.assertEqual(len(self.blank), 0)

    def test_filter_by_price_returns_ten_results_by_default(self):
        self.assertEqual(len(self.recipes), 10)

    def test_filter_by_price_returns_specified_number_of_results(self):
        self.assertEqual(len(self.thirty), 30)

    def test_filter_by_price_recipes_are_within_price_range(self):
        prices = [x["price"] for x in self.recipes]
        for p in prices:
            self.assertTrue(0 < p < 20)




if __name__ == '__main__':
    unittest.main()
