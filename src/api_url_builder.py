from __future__ import annotations
from enum import Enum


APIKEY = "&apiKey=b9f570c04c8a44229ffd38618ddfabe2"


class RecipeSearch:
    """
    Class used to easily build API calls for recipe searching in the Spoonacular API
    """
    default_url = "https://api.spoonacular.com/recipes/complexSearch"

    def __init__(self, url=default_url):
        self.url = url
        self.url.replace(APIKEY, "")

    def add_query(self, query: str) -> RecipeSearch:
        """
        Specifies a search by name in the API call
        :param query: The name of the recipe
        :return: self
        """
        self.url += "?query=" + query
        return self

    def add_ingredient_search(self, ingredient: str) -> RecipeSearch:
        """
        Specifies ingredients to search for in API call
        :param ingredient: List of ingredients as a comma separated list
        :return: self
        """
        self.url += "?includeIngredients=" + ingredient
        return self

    def add_sort(self, sort: str) -> RecipeSearch:
        """
        Specifies the type of sort to perform in the API call
        :param sort: Type of sort
        :return: self
        """
        self.url += "&sort=" + sort
        return self

    def add_filter(self, filter: str, min: int, max: int):
        """

        :param filter:
        :param min:
        :param max:
        :return:
        """
        self.url += "&min" + filter + "=" + min
        self.url += "&max" + filter + "=" + max

        return self

    def add_diets(self, diet: str) -> RecipeSearch:
        """
        Specifies which diet to filter by in the API call
        :param diet: Diet type
        :return: self
        """
        self.url += "&diet=" + diet
        return self

    def add_recipe_info(self) -> RecipeSearch:
        """
        Specifies that you want the API to return extended information about the recipe.
        :return: self
        """
        self.url += "&addRecipeInformation=true"
        return self

    def add_offset(self, offset: int) -> RecipeSearch:
        """
        Specifies how many results to skip ahead when returning the list of recipes.
        :param offset: Number of recipes to skip
        :return: self
        """
        self.url += "&offset=" + str(offset)
        return self

    def set_num_results(self, num_results: int) -> RecipeSearch:
        """
        Specifies how many results to return.
        :param num_results: Number of results to return
        :return: self
        """
        self.url += "&=" + str(num_results)

    def get_url(self) -> RecipeSearch:
        """
        Retrieves the url
        :return: the url appended with the API key.
        """
        return self.url + APIKEY



class InfoSearch:
    """
    Class used to easily build API calls for searching up the details of a specific recipe in the Spoonacular API
    """
    def __init__(self, id: int) -> None:
        self.url = "https://api.spoonacular.com/recipes/{id}/information"
        self.url.replace("{id}", str(id))

    def set_id(self, id: int):
        self.url.replace("{id}", str(id))


class SortOptions(Enum):
    """
    Class used to maintain consistency on the types of sorting options that Spoonacular API offers.
    """
    popularity = "popularity"
    healthiness = "healthiness"
    price = "price"
    time = "time"
    carbs = "carbs"
    cholesterol = "cholesterol"
    total_fat = "total-fat"
    sugar = "sugar"
    sodium = "sodium"
    calories = "calories"
    protein = "protein"


class DietOptions(Enum):
    GlutenFree = "glutenfree"
    Ketogenic = "ketogenic"
    Vegetarian = "vegetarian"
    LactoVegetarian = "lacto-vegetarian"
    OvoVegetarian = "ovo-vegetarian"
    Vegan = "vegan"
    Pescetarian = "pescetarian"
    Paleo = "paleo"
    Primal = "primal"
    Whole30 = "whole30"


class FilterOptions(Enum):
    Diet = 0
    Calories = "Calories"
    Price = 1


class SearchMode(Enum):
    """
    Class used to maintain consistency on the type of search we are performing on the API.
    """
    search_by_ingredients = 0
    search_by_name = 1
    



