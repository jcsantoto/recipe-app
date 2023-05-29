import requests
import string


class RecipeNameSearcher:
    """Class for doing stuff"""

    APIKEY = "&apiKey=b9f570c04c8a44229ffd38618ddfabe2"

    SEARCH_URL = "https://api.spoonacular.com/recipes/complexSearch?query="

    def search_by_name(self, query: string) -> list:
        """
        Performs an API call to search for a recipe given a query from the user. Retrieves Recipe Title, Summary, and
        Image

        Args:
            self: The search that the user wants to perform
        Returns:
            recipes: list of recipes where each recipe is a dictionary
        """

        full_url = self.SEARCH_URL + query + self.APIKEY + "&sort=price&addRecipeInformation=true"

        response = requests.get(full_url).json()





