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

    def add_filter(self, filter_type: str, min_val: int, max_val: int):
        """

        :param filter_type:
        :param min_val:
        :param max_val:
        :return:
        """
        if min_val:
            self.url += "&min" + filter_type + "=" + str(min_val)
        if max_val:
            self.url += "&max" + filter_type + "=" + str(max_val)

        return self

    def add_filters(self, filters: list[FilterOptions], filter_settings: list[dict]) -> RecipeSearch:
        """
        Structures URL to have the necessary elements to perform all filters specified.
        :param filters: List of filter options
        :param filter_settings: List of filter parameters
        :return: min and max values for price filter and a flag for price filter.d
        """
        num_filters = len(filters)
        for i in range(num_filters):

            if filters[i] != FilterOptions.Price:
                min_val = filter_settings[i]["min"]
                max_val = filter_settings[i]["max"]
                self.add_filter(filters[i].value, min_val, max_val)

        return self

    def add_diets(self, diets: list[DietOptions]) -> RecipeSearch:
        """
        Specifies which diet to filter by in the API call
        :param diets: Diet types
        :return: self
        """

        diet_str = "|".join([x.value for x in diets])

        self.url += "&diet=" + diet_str
        return self

    def exclude_ingredients(self, ingredients: str) -> RecipeSearch:
        """

        :param ingredients:
        :return:
        """

        self.url += "&excludeIngredients=" + ingredients.replace(" ", "")

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


class FilterOptions(Enum):
    Calories = "Calories"
    Carbs = "Carbs"
    Fat = "Fat"
    Price = "price"


class SortOptions(Enum):
    """
    Class used to maintain consistency on the types of sorting options that Spoonacular API offers.
    """
    default = "--"
    popularity = "popularity"
    price = "price"
    time = "time"
    healthiness = "healthiness"
    carbs = "carbs"
    calories = "calories"
    cholesterol = "cholesterol"
    protein = "protein"
    sodium = "sodium"
    sugar = "sugar"
    total_fat = "total-fat"


class DietOptions(Enum):
    Vegetarian = "vegetarian"
    Vegan = "vegan"
    GlutenFree = "glutenfree"
    Ketogenic = "ketogenic"
    LactoVegetarian = "lacto-vegetarian"
    OvoVegetarian = "ovo-vegetarian"
    Pescetarian = "pescetarian"
    Paleo = "paleo"
    Primal = "primal"
    Whole30 = "whole30"


class SearchMode(Enum):
    """
    Class used to maintain consistency on the type of search we are performing on the API.
    """
    ByIngredients = 0
    ByName = 1
