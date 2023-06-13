import requests
from api_url_builder import RecipeSearch, SortOptions, SearchMode, DietOptions, FilterOptions


def search_by_name(query: str, sort: SortOptions = None,
                   filters: list[FilterOptions] = None,
                   filter_settings: list[dict] = None,
                   num_results: int = 10) -> list:
    """
    Performs an API call to search for a recipe by its name. Sorting options and Filtering options can be specified.
    :param query: Name of the recipe
    :param sort: Type of sort to perform
    :param filters: List of filters to apply
    :param filter_settings: List of filter parameters represented as dicts. For diet specify the key as 'diet'.
    For all other filters, specify a min and max value using the keys 'min' and 'max' respectively.
    :param num_results: Number of results to return
    :return: list of recipes where each recipe is a dictionary containing ID, Title, Summary, Price and Image URL
    """

    if query == "":
        return []

    url = RecipeSearch()
    url.add_query(query).add_recipe_info().set_num_results(num_results)

    if sort:
        url.add_sort(sort.value)

    if filters:
        max_price, min_price, price_filter_flag = add_filters(filters=filters, filter_settings=filter_settings, url=url)

        if price_filter_flag:
            return filter_by_price_range(url.get_url(), min_price, max_price, num_results)

    results = _get_results(url.get_url())

    return results


def search_by_ingredient(query: str, sort: SortOptions = None,
                         filters: list[FilterOptions] = None,
                         filter_settings: list[dict] = None,
                         num_results: int = 10) -> list:
    """
    Performs an API call to search for a recipe by its name. Sorting options and Filtering options can be specified.
    :param query: Name of the recipe
    :param sort: Type of sort to perform
    :param filters: List of filters to apply
    :param filter_settings: List of filter parameters represented as dicts. For diet specify the key as 'diet'.
    For all other filters, specify a min and max value using the keys 'min' and 'max' respectively.
    :param num_results: Number of results to return
    :return: list of recipes where each recipe is a dictionary containing ID, Title, Summary, Price and Image URL
    """
    if query == "":
        return []

    url = RecipeSearch()
    url.add_ingredient_search(query).add_recipe_info().set_num_results(num_results)

    if sort:
        url.add_sort(sort.value)

    if filters:
        max_price, min_price, price_filter_flag = add_filters(filters=filters, filter_settings=filter_settings, url=url)

        if price_filter_flag:
            return filter_by_price_range(url.get_url(), min_price, max_price, num_results)

    # results = _get_results(url.get_url())

    return None


def add_filters(filters: list[FilterOptions], filter_settings: list[dict], url: str) -> tuple[int, int, bool]:
    """
    Structures URL to have the necessary elements to perform all filters specified.
    :param filters: List of filter options
    :param filter_settings: List of filter parameters
    :param url: RecipeSearch object to represent URL
    :return: min and max values for price filter and a flag for price filter.d
    """
    num_filters = len(filters)
    price_filter_flag = False
    min_price = -1
    max_price = -1
    for i in range(num_filters):

        if filters[i] == FilterOptions.Diet:
            diet_list = filter_settings[i]["diet"]
            diets = "|".join([x.value for x in diet_list])
            url.add_diets(diets)

        elif filters[i] == FilterOptions.Price:
            price_filter_flag = True
            min_price = filter_settings[i]["min"]
            max_price = filter_settings[i]["max"]

        else:
            min_val = filter_settings[i]["min"]
            max_val = filter_settings[i]["max"]
            url.add_filter(filters[i].value, min_val, max_val)
    return max_price, min_price, price_filter_flag


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
