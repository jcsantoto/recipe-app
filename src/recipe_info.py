import requests
import string

APIKEY = "?apiKey=b9f570c04c8a44229ffd38618ddfabe2"

SEARCH_URL = "https://api.spoonacular.com/recipes/{id}/information"


class Recipe:
    """
    This class is used to represent a recipe specified by a recipe id.
    It contains methods to retrieve information about a recipe.
    """
    def __init__(self, recipe_id: int):
        self.id = recipe_id
        url = SEARCH_URL.replace("{id}", self.id) + APIKEY
        self.recipe_info = requests.get(url).json()

    def get_title(self) -> string:
        """
        Method to get recipe title
        :return: Returns recipe title
        """
        return self.recipe_info['title']

    def get_price(self) -> string:
        """
        Method to return price of recipe
        :return: Returns recipe price
        """
        return self.recipe_info['pricePerServing'] / 100

    def get_prep_time(self) -> string:
        """
        Method to return ready time of a recipe
        :return: Returns ready time
        """
        return self.recipe_info['readyInMinutes']

    def get_summary(self) -> string:
        """
        Method to return recipe summary
        :return: Returns recipe summary
        """
        return self.recipe_info['summary']

    def get_ingredients(self) -> list:
        """
        Method to return a list of ingredients
        :return: Returns ingredients as a list
        """
        return self.recipe_info['extendedIngredients']

    def get_instructions_html(self) -> string:
        """
        Method to return instructions as a string with html formatting
        :return: Returns instructions as a string
        """
        return self.recipe_info['instructions']

    def get_instructions_list(self) -> list:
        """
        Method to return instructions as a list
        :return: Returns instructions as a list.
        """
        return self.recipe_info['analyzedInstructions'][0]['steps']

