from __future__ import annotations
from src.api_options import ApiFilterOptions, DietOptions, IntoleranceOptions

APIKEY = "b9f570c04c8a44229ffd38618ddfabe2"


class RecipeSearch:
    """
    Class used to easily build API calls for recipe searching in the Spoonacular API
    """
    default_url = "https://api.spoonacular.com/recipes/complexSearch"

    def __init__(self, url=default_url):
        self.url = url
        self.querystring = {"apiKey": APIKEY}

    def add_query(self, query: str) -> RecipeSearch:
        """
        Specifies a search by name in the API call
        :param query: The name of the recipe
        :return: self
        """
        self.querystring["query"] = query
        return self

    def add_ingredient_search(self, ingredients: str) -> RecipeSearch:
        """
        Specifies ingredients to search for in API call
        :param ingredients: List of ingredients as a comma separated list
        :return: self
        """
        self.querystring["includeIngredients"] = ingredients
        return self

    def add_sort(self, sort: str) -> RecipeSearch:
        """
        Specifies the type of sort to perform in the API call
        :param sort: Type of sort
        :return: self
        """
        self.querystring["sort"] = sort
        return self

    def add_filter(self, filter_type: str, min_val: int, max_val: int):
        """
        Specifies the type of filter to apply and the range of values to filter by.
        :param filter_type: Type of filter
        :param min_val: Minimum value to filter by
        :param max_val: Maximum value to filter by
        :return: self
        """
        if min_val:
            self.querystring["min"+filter_type] = min_val
        if max_val:
            self.querystring["max"+filter_type] = max_val

        return self

    def add_filters(self, filters: dict) -> RecipeSearch:
        """
        Structures URL to have the necessary elements to perform all filters specified.
        :param filters: List of filter options
        :param filter_settings: List of filter parameters
        :return: min and max values for price filter and a flag for price filter.d
        """

        for item in filters:
            filter_range = filters[item]
            self.add_filter(item.value, filter_range["min"], filter_range["max"])

        return self

    def add_diets(self, diets: list[DietOptions]) -> RecipeSearch:
        """
        Specifies which diet to filter by in the API call
        :param diets: Diet types
        :return: self
        """

        diet_str = "|".join([x.value for x in diets])

        self.querystring["diet"] = diet_str
        return self

    def add_intolerances(self, intolerances: list[IntoleranceOptions]) -> RecipeSearch:

        intolerance_str = ",".join([x.value for x in intolerances])
        self.querystring["intolerances"] = intolerance_str
        return self

    def exclude_ingredients(self, ingredients: str) -> RecipeSearch:
        """
        Specifies ingredients to exclude from search
        :param ingredients: Ingredient to exclude
        :return: self
        """
        self.querystring["excludeIngredients"] = ingredients.replace(" ", "")

        return self

    def add_recipe_info(self) -> RecipeSearch:
        """
        Specifies that you want the API to return extended information about the recipe.
        :return: self
        """
        self.querystring["addRecipeInformation"] = "true"
        return self

    def add_recipe_nutrition(self) -> RecipeSearch:
        self.querystring["addRecipeNutrition"] = "true"
        return self

    def add_offset(self, offset: int) -> RecipeSearch:
        """
        Specifies how many results to skip ahead when returning the list of recipes.
        :param offset: Number of recipes to skip
        :return: self
        """
        self.querystring["offset"] = offset
        return self

    def set_num_results(self, num_results: int) -> RecipeSearch:
        """
        Specifies how many results to return.
        :param num_results: Number of results to return
        :return: self
        """
        self.querystring["number"] = num_results

    def get_url(self) -> str:
        """
        Retrieves the url
        :return: the url appended with the API key.
        """
        return self.url

    def get_querystring(self) -> dict:
        """
        Retrieves parameters of the query as a dict
        :return: the parameters of the query as a dict.
        """
        return self.querystring
