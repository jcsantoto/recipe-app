from enum import Enum


def to_list(option_enum: Enum) -> list:
    """
    Function to create a list out of an enum.
    :param option_enum: Type of enum
    :return: list of values in the enum class
    """
    return [x for x in option_enum]


def idx_to_option(idx: list, option_enum: Enum) -> list:
    """
    Creates a list of enum values based on the indices provide

    Example: idx_to_option([1, 2] , IntoleranceOptions) = [egg, gluten]

    :param idx: list of indices
    :param option_enum: Type of enum
    :return: List of enum values
    """
    options = to_list(option_enum)
    return [options[x] for x in idx]


class IntoleranceOptions(Enum):
    """
    Class to represent all intolerance options supported by the API
    """
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


class ApiFilterOptions(Enum):
    """
    Class to represent nutritional filter options
    """
    Calories = "Calories"
    Carbs = "Carbs"
    Fat = "Fat"
    Protein = "Protein"


class CustomFilterOptions(Enum):
    """
    Class to represent filtering options we have implemented that are not provided by the API
    """
    Price = "Price"
    Servings = "Servings"
    Ingredients = "Ingredients"


class SortOptions(Enum):
    """
    Class used to represent the types of sorting options that Spoonacular API offers.
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
    """
    Class used to represent the types of diet that the API can filter by
    """
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
    ByName = 1
    ByIngredients = 2

class CuisineOptions(Enum):
    African = "African"
    Asian = "Asian"
    American = "American"
    British = "British"
    Cajun = "Cajun"
    Caribbean = "Caribbean"
    Chinese = "Chinese"
    Eastern = "Eastern"
    European = "European"
    French = "French"
    German = "German"
    Greek = "Greek"
    Indian = "Indian"
    Irish = "Irish"
    Italian = "Italian"
    Japanese = "Japanese"
    Jewish = "Jewish"
    Korean = "Korean"
    Latin = "Latin"
    Mediterranean = "Mediterranean"
    Mexican = "Mexican"
    Middle = "Middle"
    Nordic = "Nordic"
    Southern = "Southern"
    Spanish = "Spanish"
    Thai = "Thai"
    Vietnamese = "Vietnamese"

