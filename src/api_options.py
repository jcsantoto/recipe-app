from enum import Enum


def to_list(option_enum: Enum) -> list:
    return [x for x in option_enum]

class IntoleranceOptions(Enum):
    Dairy = "dairy"
    Egg = "egg"
    Gluten = "gluten"
    Grain = "grain"
    Peanut = "peanut"
    Seafood = "seafood"
    Sesame = "sesame"
    Shellfish = "shellfish"
    Soy = "soy"
    Sulfite = "sulfite"
    TreeNut = "tree-nut"
    Wheat = "wheat"

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
