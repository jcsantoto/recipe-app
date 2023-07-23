import requests
import random
import string
from src.search_builder import RecipeSearch

APIKEY = "b9f570c04c8a44229ffd38618ddfabe2"


def get_similar_recipe(recipe_name: str):

    recipe_name = recipe_name.translate(str.maketrans('', '', string.punctuation))

    keywords = recipe_name.split(" ")
    random_keyword = random.sample(keywords, 2)
    query = " ".join(random_keyword)

    search = RecipeSearch()
    search.add_query(query)
    search.set_num_results(4)

    response = requests.get(search.url, search.querystring).json()['results']

    return response


def get_random_recipe(tags: str):
    url = "https://api.spoonacular.com/recipes/random"
    param = {"apiKey": APIKEY,
             "tags": tags,
             "number": 4}

    response = requests.get(url, param).json()['recipes']

    return response

