from enum import Enum


class IntoleranceOptions(Enum):
    Dairy = 1
    Egg = 2
    Gluten = 3
    Grain = 4
    Peanut = 5
    Seafood = 6
    Sesame = 7
    Shellfish = 8
    Soy = 9
    Sulfite = 10
    Tree = 11
    Nut = 12
    Wheat = 13


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