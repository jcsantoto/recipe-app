import requests
import string

APIKEY = "?apiKey=b9f570c04c8a44229ffd38618ddfabe2"

SEARCH_URL = "https://api.spoonacular.com/recipes/{id}/information"


class Recipe:

    def __init__(self, recipe_id: int):
        self.id = recipe_id
        url = SEARCH_URL.replace("{id}", self.id) + APIKEY
        self.recipe_info = requests.get(url).json()

    def get_title(self) -> string:
        return self.recipe_info['title']

    def get_price(self) -> string:
        return self.recipe_info['pricePerServing'] / 100

    def get_prep_time(self) -> string:
        return self.recipe_info['readyInMinutes']

    def get_summary(self) -> string:
        return self.recipe_info['summary']

    def get_ingredients(self) -> list:
        return self.recipe_info['extendedIngredients']

    def get_instructions_html(self) -> string:
        return self.recipe_info['instructions']

    def get_instructions_list(self) -> list:
        return self.recipe_info['analyzedInstructions'][0]['steps']

if __name__ == '__main__':
    r = Recipe("1095810")
    print(r.recipe_info)
