import requests
import string

APIKEY = "&apiKey=b9f570c04c8a44229ffd38618ddfabe2"

SEARCH_URL = "https://api.spoonacular.com/recipes/complexSearch?query="


def search_by_name(query: string) -> list:
    """
    Performs an API call to search for a recipe given a query from the user. Retrieves Recipe Title, Summary, and
    Image.

    Args:
        query: The search that the user wants to perform
    Returns:
        simplified_recipes: list of recipes where each recipe is a dictionary containing Title, Summary, and Image URL
    """

    full_url = SEARCH_URL + query + APIKEY + "&sort=price&addRecipeInformation=true"

    response = requests.get(full_url).json()

    recipes = response['results']

    simplified_recipes = []

    for r in recipes:
        simplified_recipes.append({'title': r['title'], 'summary': r['summary'], 'image': r['image']})

    return simplified_recipes

