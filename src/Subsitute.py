import requests

def get_substitute_by_name(ingredient: str):
    url = "https://api.spoonacular.com/food/ingredients/substitutes"
    param = {"ingredientName": ingredient,
             "apiKey": "b9f570c04c8a44229ffd38618ddfabe2"
             }
    sub_request = requests.get(url, param).json()

    return sub_request


def get_substitute_by_id(idr: str):
    url = "https://api.spoonacular.com/food/ingredients/{id}/substitutes"
    url.replace("{id}", idr)

    param = {
        "apiKey": "b9f570c04c8a44229ffd38618ddfabe2"
    }
    sub_request = requests.get(url, param).json()

    return sub_request
