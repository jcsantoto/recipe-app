import requests
from src.api_options import SortOptions, SearchMode, DietOptions, FilterOptions
from src.search_builder import RecipeSearch


def search(query: str, mode: SearchMode = None, sort: SortOptions = None,
           filters: list[FilterOptions] = None,
           filter_settings: list[dict] = None,
           diets: list[DietOptions] = None,
           ex_ingredients: str = None,
           num_results: int = 10) -> list:
    """
    Performs an API call with the options specified in the parameters

    :param query: The name or ingredients to search for
    :param mode: Specify search mode: By Name or By Ingredients
    :param sort: Specify a type of sort
    :param filters: Specify multiple filters using a list
    :param filter_settings: Specify the range of each filter
    :param diets: Specify the type of diet
    :param ex_ingredients: Specify which ingredients to exclude
    :param num_results: Specify how many results to return.
    :return: A list of recipes where each recipe is a dict containing 'title', 'summary', 'image', 'price' and 'id'
    """

    # Return nothing if empty
    if query == "":
        return []

    recipe_search = RecipeSearch()

    # Search Mode
    if mode == SearchMode.ByName:
        recipe_search.add_query(query).add_recipe_info().set_num_results(num_results)
    elif mode == SearchMode.ByIngredients:
        recipe_search.add_ingredient_search(query).add_recipe_info().set_num_results(num_results)

    # Sort
    if sort:
        recipe_search.add_sort(sort.value)

    # Diet Filter
    if diets:
        recipe_search.add_diets([DietOptions(x) for x in diets])

    # Ingredient Filter
    if ex_ingredients:
        recipe_search.exclude_ingredients(ex_ingredients)

    # All other filters
    if filters:
        recipe_search.add_filters(filters=filters, filter_settings=filter_settings)

        if FilterOptions.Price in filters:
            idx = filters.index(FilterOptions.Price)
            return filter_by_price_range(recipe_search.get_url(), filter_settings[idx]["min"], filter_settings[idx]["max"],
                                         num_results)

    # Retrieve results
    results = _get_results(recipe_search)

    print(recipe_search.get_url())
    print(recipe_search.get_querystring())

    return results


def filter_by_price_range(query: RecipeSearch, min_price: float, max_price: float, num_results: int = 10) -> list:
    """
    Performs an API call using the URL of a previous API call that returned a dataset that is required to be filtered
    by a price range defined by min_price and max_price. Retrieves Recipe ID, Title, Summary, Price and Image.

    :param query: API call url
    :param min_price: Minimum price to filter by
    :param max_price: Maximum price to filter by
    :param num_results: Number of results to return, defaulted to 10
    :return: list of recipes filtered by price where each recipe is a dictionary containing
    Title, Summary, Price, and Image URL
    """

    if not min_price:
        min_price = 0

    if min_price < 0 or max_price < min_price:
        return []

    results = _get_results(query)

    # It's possible that the while loop may attempt to retrieve recipes infinitely,
    # so we will limit how many extra calls it can perform.
    num_calls = 0
    call_cap = 3

    if not max_price:
        filtered_results = [x for x in results if min_price <= x["price"]]
    else:
        filtered_results = [x for x in results if min_price <= x["price"] <= max_price]

    # Retrieves more recipes if there are not enough to match the num_results parameter.
    num_additional_calls = 0
    while len(filtered_results) < num_results and num_calls < call_cap:
        num_additional_calls += 1
        offset = num_additional_calls * num_results

        additional_results = _get_results(query.add_offset(offset))
        num_calls += 1

        if not max_price:
            filtered_additional_results = [x for x in additional_results if min_price <= x["price"]]
        else:
            filtered_additional_results = [x for x in additional_results if min_price <= x["price"] <= max_price]

        filtered_results += filtered_additional_results

    return filtered_results[:num_results]


def _get_results(query: RecipeSearch) -> list:
    """
    Retrieves the title, summary, image, and price attributes for each recipe obtained from the API call 
    made using the specified URL.

    :param url: URL for API call
    :return: list of recipes with the ID, title, summary, image, and price attributes
    """

    response = requests.get(query.get_url(), params=query.get_querystring()).json()

    if 'status' in response and response['status'] == 'failure':
        return [{"title": "Failure", "summary": response['message']}]

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

