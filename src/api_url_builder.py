from __future__ import annotations
from enum import Enum


APIKEY = "&apiKey=b9f570c04c8a44229ffd38618ddfabe2"


class RecipeSearch:

    def __init__(self):
        self.url = "https://api.spoonacular.com/recipes/complexSearch"

    def add_query(self, query: str) -> RecipeSearch:
        self.url += "?query=" + query
        return self

    def add_ingredient_search(self, ingredient: str) -> RecipeSearch:
        self.url += "?includeIngredients=" + ingredient
        return self

    def add_sort(self, sort: str) -> RecipeSearch:
        self.url += "&sort=" + sort
        return self

    def add_recipe_info(self) -> RecipeSearch:
        self.url += "&addRecipeInformation=true"
        return self

    def add_offset(self, offset: int) -> RecipeSearch:
        self.url += "&offset=" + str(offset)
        return self

    def set_offset(self, offset: int) -> RecipeSearch:
        None

    def set_num_results(self, num_results: int) -> RecipeSearch:
        self.url += "&=" + str(num_results)

    def get_url(self) -> RecipeSearch:
        return self.url + APIKEY


class InfoSearch:
    
    def __init__(self, id: int) -> None:
        self.url = "https://api.spoonacular.com/recipes/{id}/information"
        self.url.replace("{id}", str(id))

    def set_id(self, id: int):
        self.url.replace("{id}", str(id))


class SortOptions(Enum):
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


class SearchMode(Enum):
    search_by_ingredients = 0
    search_by_name = 1
    



