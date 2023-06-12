import requests
from api_url_builder import RecipeSearch, SortOptions, SearchMode


def search_by_name(query: str, num_results: int = 10) -> list:
    """
    Performs an API call to search for a recipe by name given a query from the user. Retrieves Recipe Title, Summary, and
    Image.

    :param query: The search that the user wants to perform
    :param num_results: Number of results to return, defaulted to 10
    :return: list of recipes where each recipe is a dictionary containing ID, Title, Summary, Price and Image URL
    """

    if query == "":
        return []

    url = RecipeSearch()
    url.add_query(query).add_recipe_info().set_num_results(num_results)

    results = _get_results(url)

    return results


def search_by_ingredient(query: str, num_results: int = 10) -> list:
    """
    Performs an API call to search for a recipe by ingredients given a query from the user formatted as a comma
    separated list. Retrieves Recipe Title, Summary, and Image.

    :param query: The search that the user wants to perform
    :param num_results: Number of results to return, defaulted to 10
    :return: list of recipes where each recipe is a dictionary containing ID, Title, Summary, Price, and Image URL
    """

    if query == "":
        return []

    url = RecipeSearch()
    url.add_ingredient_search(query).add_recipe_info().set_num_results(num_results)

    results = _get_results(url.get_url())

    return results


def sort_by_total_fat(query: str, mode: SearchMode, num_results: int = 10) -> list:
    """
    Performs an API call to search for a recipe in one of the two modes specified by mode and return results sorted by
    total fat. Retrieves Recipe Title, Summary, and Image.
    :param query: Name of recipe or List of ingredients
    :param mode: The type of search to perform (name / ingredients)
    :param num_results: Number of results to return, defaulted to 10
    :return: list of recipes where each recipe is a dictionary containing ID, Title, Summary, Price, and Image URL
    """
    if query == "":
        return []

    url = _build_sort_url(query, mode, SortOptions.total_fat, num_results)

    results = _get_results(url)

    return results


def sort_by_carbs(query: str, mode: SearchMode, num_results: int = 10) -> list:
    """
    Performs an API call to search for a recipe in one of the two modes specified by mode and return results sorted by
    carbs. Retrieves Recipe Title, Summary, and Image.
    :param query: Name of recipe or List of ingredients
    :param mode: The type of search to perform (name / ingredients)
    :param num_results: Number of results to return, defaulted to 10
    :return: list of recipes where each recipe is a dictionary containing ID, Title, Summary, Price, and Image URL
    """
    if query == "":
        return []

    url = _build_sort_url(query, mode, SortOptions.carbs, num_results)

    results = _get_results(url)

    return results


def sort_by_protein(query: str, mode: SearchMode, num_results: int = 10) -> list:
    """
    Performs an API call to search for a recipe in one of the two modes specified by mode and return results sorted by
    protein. Retrieves Recipe Title, Summary, and Image.
    :param query: Name of recipe or List of ingredients
    :param mode: The type of search to perform (name / ingredients)
    :param num_results: Number of results to return, defaulted to 10
    :return: list of recipes where each recipe is a dictionary containing ID, Title, Summary, Price, and Image URL
    """
    if query == "":
        return []

    url = RecipeSearch()
    url = _build_sort_url(query, mode, SortOptions.protein, num_results)

    results = _get_results(url)

    return results


def filter_by_price_range(url: str, min_price: float, max_price: float, num_results: int = 10) -> list:
    """
    Performs an API call using the URL of a previous API call that returned a dataset that is required to be filtered
    by a price range defined by min_price and max_price. Retrieves Recipe ID, Title, Summary, Price and Image.

    :param url: API call url
    :param min_price: Minimum price to filter by
    :param max_price: Maximum price to filter by
    :param num_results: Number of results to return, defaulted to 10
    :return: list of recipes filtered by price where each recipe is a dictionary containing
    Title, Summary, Price, and Image URL
    """

    if min_price < 0 or max_price < min_price:
        return []

    if url == "":
        return []

    results = _get_results(url)

    filtered_results = [x for x in results if min_price <= x["price"] <= max_price]

    # Retrieves more recipes if there are not enough to match the num_results parameter.
    num_additional_calls = 0
    while len(filtered_results) < num_results:
        num_additional_calls += 1
        offset = num_additional_calls * num_results

        additional_results = _get_results(url + "&offset=" + str(offset))
        filtered_additional_results = [x for x in additional_results if min_price <= x["price"] <= max_price]
        filtered_results += filtered_additional_results

    return filtered_results[:num_results]


def _build_sort_url(query: str, mode: SearchMode, sort_type: SortOptions, num_results: int) -> str:
    """
    Helps build the url for the sort functions
    :param query: Name of recipe or List of ingredients
    :param mode: The type of search to perform (name / ingredients)
    :param sort_type: Element to sort by
    :param num_results: Number of results to return
    :return: The url for the API call
    """
    url = RecipeSearch()

    if mode == SearchMode.search_by_name:
        url.add_query(query).add_sort(sort_type.value).add_recipe_info().set_num_results(num_results)
    elif mode == SearchMode.search_by_ingredients:
        url.add_ingredient_search(query).add_sort(sort_type.value).add_recipe_info().set_num_results(num_results)

    return url.get_url()


def _get_results(url: str):
    """
    Retrieves the title, summary, image, and price attributes for each recipe obtained from the API call 
    made using the specified URL.

    :param url: URL for API call
    :return: list of recipes with the ID, title, summary, image, and price attributes
    """

    response = requests.get(url).json()
    recipes = response['results']
    simplified_recipes = []
    for r in recipes:
        info = {
            'title': r['title'],
            'summary': r['summary'],
            'image': r['image'],
            'price': r['pricePerServing'] / 100,
            'id': r['id']
        }
        simplified_recipes.append(info)

    return simplified_recipes

