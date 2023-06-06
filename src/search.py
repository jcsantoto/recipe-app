import requests

APIKEY = "&apiKey=b9f570c04c8a44229ffd38618ddfabe2"

SEARCH_URL = "https://api.spoonacular.com/recipes/complexSearch"

BY_NAME = "?query="

BY_INGREDIENTS = "?includeIngredients="


def search_by_name(query: str, num_results: int = 10) -> list:
    """
    Performs an API call to search for a recipe by name given a query from the user. Retrieves Recipe Title, Summary, and
    Image.

    :param query: The search that the user wants to perform
    :param num_results: Number of results to return, defaulted to 10
    :return: list of recipes where each recipe is a dictionary containing Title, Summary, and Image URL
    """

    full_url = SEARCH_URL + BY_NAME + query + APIKEY + "&addRecipeInformation=true"

    results = _get_results(full_url)

    return results

def search_by_ingredient(query: str, num_results: int = 10) -> list:
    """
    Performs an API call to search for a recipe by ingredients given a query from the user formatted as a comma separated list. Retrieves Recipe Title, Summary, and
    Image.

    :param query: The search that the user wants to perform, defaulted to 10
    :return: list of recipes where each recipe is a dictionary containing Title, Summary, and Image URL
    """

    full_url = SEARCH_URL + BY_INGREDIENTS + query + APIKEY + "&addRecipeInformation=true"

    results = _get_results(full_url)

    return results

def filter_by_price_range(query: str, min_price: float, max_price: float, num_results: int = 10) -> list:
    """_summary_

    :param query: _description_
    :param min_price: _description_
    :param max_price: _description_
    :return: _description_
    """

    full_url = SEARCH_URL + BY_NAME + query + APIKEY + "&sort=price&addRecipeInformation=true"

    results = _get_results(full_url)

    filtered_results = [x for x in results if x["price"] >= min_price and x["price"] <= max_price]

    # Retrieves more recipes if there are not enough to match the num_results parameter.
    num_additional_calls = 0
    while len(filtered_results) < num_results:
        num_additional_calls += 1
        offset = num_additional_calls * num_results

        additional_results =  _get_results(full_url + "&offset=" + str(offset))
        filtered_additional_results = [x for x in additional_results if x["price"] >= min_price and x["price"] <= max_price]
        filtered_results += filtered_additional_results
        
    return filtered_results[:num_results]


def _get_results(url: str):
    """
    Retrieves the title, summary, image, and price attributes for each recipe obtained from the API call 
    made using the specified URL.

    :param url: URL for API call
    :return: list of recipes with the title, summary, image, and price attributes
    """

    response = requests.get(url).json()
    recipes = response['results']
    simplified_recipes = []
    for r in recipes:
        info = {
            'title': r['title'], 
            'summary': r['summary'], 
            'image': r['image'],
            'price': r['pricePerServing']/100,
        }
        simplified_recipes.append(info)
    
    return simplified_recipes


if __name__ == '__main__':
    print(filter_by_price_range("cake",0,5))