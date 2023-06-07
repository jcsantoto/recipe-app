import requests

APIKEY = "&apiKey=b9f570c04c8a44229ffd38618ddfabe2"

SEARCH_URL = "https://api.spoonacular.com/recipes/complexSearch"

BY_NAME = "?query="

BY_INGREDIENTS = "?includeIngredients="


def search_by_name(query: str) -> list:
    """
    Performs an API call to search for a recipe by name given a query from the user. Retrieves Recipe Title, Summary, and
    Image.

    :param
        query: The search that the user wants to perform
    :return:
        simplified_recipes: list of recipes where each recipe is a dictionary containing Title, Summary, and Image URL
    """

    full_url = SEARCH_URL + BY_NAME + query + APIKEY + "&addRecipeInformation=true"

    response = requests.get(full_url).json()

    recipes = response['results']

    simplified_recipes = []

    for r in recipes:
        simplified_recipes.append({'title': r['title'], 'summary': r['summary'], 'image': r['image']})

    return simplified_recipes

def search_by_ingredient(query: str) -> list:
    """
    Performs an API callto search for a recipe by ingredients given a query from the user formatted as a comma separated list. Retrieves Recipe Title, Summary, and
    Image.

    :param
        query: The search that the user wants to perform
    :return:
        simplified_recipes: list of recipes where each recipe is a dictionary containing Title, Summary, and Image URL
    """

    full_url = SEARCH_URL + BY_INGREDIENTS + query + APIKEY + "&addRecipeInformation=true"

    response = requests.get(full_url).json()

    recipes = response['results']

    simplified_recipes = []

    for r in recipes:
        simplified_recipes.append({'title': r['title'], 'summary': r['summary'], 'image': r['image']})

    return simplified_recipes

def search_by_cook_time():
    """
    Will sort out cook
    :return:
    return cook
    """
