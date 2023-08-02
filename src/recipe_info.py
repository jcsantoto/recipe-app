import requests
from src.api_options import IntoleranceOptions
import src.recipe_info_util as util

APIKEY = "?apiKey=b9f570c04c8a44229ffd38618ddfabe2"

SEARCH_URL = "https://api.spoonacular.com/recipes/{id}/information"
SEARCH_URL2 = "https://api.spoonacular.com/recipes/{id}/priceBreakdownWidget.json"
SEARCH_URL3 ="https://api.spoonacular.com/recipes/{id}/nutritionWidget.json"


class Recipe:
    """
    This class is used to represent a recipe specified by a recipe id.
    It contains methods to retrieve information about a recipe.
    """

    def __init__(self, recipe_id: int = None, response: dict = None):

        if recipe_id:
            self.id = recipe_id
            url = SEARCH_URL.replace("{id}", str(self.id)) + APIKEY
            self.recipe_info = requests.get(url).json()

            url2 = SEARCH_URL2.replace("{id}", str(self.id)) + APIKEY
            self.priceBreakDown = requests.get(url2).json()

            url3 = SEARCH_URL3.replace("{id}", str(self.id)) + APIKEY
            self.macros = requests.get(url3).json()

        elif response:
            self.id = response['id']
            self.recipe_info = response
            self.priceBreakDown = response
            self.macros = response

    def get_all(self):
        """
        Returns the recipe info dictionary
        :return: recipe info dictionary
        """
        return self.recipe_info

    def get_title(self) -> str:
        """
        Method to get recipe title
        :return: Returns recipe title
        """
        return self.recipe_info['title']

    def get_price(self) -> str:
        """
        Method to return price of recipe
        :return: Returns recipe price
        """
        return self.recipe_info['pricePerServing'] / 100

    def get_total_Cost(self) -> str:

        rounded = round((self.priceBreakDown['totalCost'] /100) ,2)
        return "$"+ str(rounded)

    def get_Macros(self) -> str:

        return self.macros['nutrients']

    def get_prep_time(self) -> str:
        """
        Method to return ready time of a recipe
        :return: Returns ready time
        """
        return self.recipe_info['readyInMinutes']

    def get_summary(self) -> str:
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

    def get_instructions_html(self) -> str:
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


def contains_intolerances(ingredients: list, dairy: bool, gluten: bool, user_intolerances: list[IntoleranceOptions]) -> list:
    """
    Checks if the recipe contains any of the intolerances that the user has specified.
    :param gluten: If recipe contains gluten
    :param dairy: If recipe contains dairy
    :param ingredients: ingredient list of recipe
    :param user_intolerances: The user's intolerances
    :return: list of intolerances that the recipe contains
    """
    contained_intolerances = []

    for intolerance in user_intolerances:
        # check dairy
        if intolerance == IntoleranceOptions.Dairy and not dairy:
            contained_intolerances.append(IntoleranceOptions.Dairy.value)

        # check gluten
        elif intolerance == IntoleranceOptions.Gluten and not gluten:
            contained_intolerances.append(IntoleranceOptions.Gluten.value)

        # check wheat
        elif intolerance == IntoleranceOptions.Wheat and not gluten:
            contained_intolerances.append(IntoleranceOptions.Wheat.value)

        # check grain
        elif intolerance == IntoleranceOptions.Grain:

            if not self.recipe_info["glutenFree"] or util.check_for_grain(ingredients):
                contained_intolerances.append(IntoleranceOptions.Grain.value)

        # check egg
        elif intolerance == IntoleranceOptions.Egg and util.check_for_egg(ingredients):
            contained_intolerances.append(IntoleranceOptions.Egg.value)

        # check peanut
        elif intolerance == IntoleranceOptions.Peanut and util.check_for_peanuts(ingredients):
            contained_intolerances.append(IntoleranceOptions.Peanut.value)

        # check seafood
        elif intolerance == IntoleranceOptions.Seafood and util.check_for_seafood(ingredients):
            contained_intolerances.append(IntoleranceOptions.Seafood.value)

        # check sesame
        elif intolerance == IntoleranceOptions.Sesame and util.check_for_sesame(ingredients):
            contained_intolerances.append(IntoleranceOptions.Sesame.value)

        # check soy
        elif intolerance == IntoleranceOptions.Soy and util.check_for_soy(ingredients):
            contained_intolerances.append(IntoleranceOptions.Soy.value)

        # check sulfite
        elif intolerance == IntoleranceOptions.Sulfite and util.check_for_sulfite(ingredients):
            contained_intolerances.append(IntoleranceOptions.Sulfite.value)

        # check tree nut
        elif intolerance == IntoleranceOptions.TreeNut and util.check_for_tree_nuts(ingredients):
            contained_intolerances.append(IntoleranceOptions.TreeNut.value)

    return contained_intolerances
