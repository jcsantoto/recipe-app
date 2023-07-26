import requests
from src.api_options import SortOptions, SearchMode, DietOptions, ApiFilterOptions, IntoleranceOptions, \
    CustomFilterOptions, CuisineOptions
from src.search_builder import RecipeSearch




def search(query: str, mode: SearchMode = None, sort: SortOptions = None,
           filters: dict = None,
           custom_filter: dict = None,
           diets: list[DietOptions] = None,
           intolerances: list[IntoleranceOptions] = None,
           ex_ingredients: str = None,
           cuisine: dict = None,
           num_results: int = 10) -> list:
    """
    Performs an API call with the options specified in the parameters

    :param intolerances: Specify intolerances
    :param query: The name or ingredients to search for
    :param mode: Specify search mode: By Name or By Ingredients
    :param sort: Specify a type of sort
    :param filters: Specify multiple filters using a list
    :param custom_filter: Specify filters that are not supported by the API
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
        recipe_search.add_query(query).add_recipe_info().add_recipe_nutrition().set_num_results(num_results)
    elif mode == SearchMode.ByIngredients:
        recipe_search.add_ingredient_search(query).add_recipe_info().add_recipe_nutrition().set_num_results(num_results)

    # Sort
    if sort:
        recipe_search.add_sort(sort.value)

    # Diet Filter
    if diets:
        recipe_search.add_diets([DietOptions(x) for x in diets])


    # Cuisine filter
    if cuisine:
        recipe_search.add_cuisine([CuisineOptions(x) for x in cuisine])

    # Intolerances
    if intolerances:
        recipe_search.add_intolerances([IntoleranceOptions(x) for x in intolerances])

    # Ingredient Filter
    if ex_ingredients:
        recipe_search.exclude_ingredients(ex_ingredients)

    # API filters
    if filters:
        recipe_search.add_filters(filters=filters)

    # Custom Filters
    if custom_filter:
        return apply_custom_filter(recipe_search, custom_filter)

    # Retrieve results
    results = _get_results(recipe_search)

    return results


def apply_custom_filter(query: RecipeSearch, filters: dict, num_results: int = 10) -> list:
    """
    Function to apply filters that are not supported by the API
    :param query: query
    :param filters: dictionary where the key is the filter being applied and
    the value is a dict of the min and max parameters for the filter
    :param num_results: number of results to return
    :return: the filtered list
    """

    results = _get_results(query)

    if CustomFilterOptions.Price in filters.keys():
        min_price = filters[CustomFilterOptions.Price]["min"]
        max_price = filters[CustomFilterOptions.Price]["max"]

        results = filter_by_price_range(results, min_price, max_price, num_results)

    if CustomFilterOptions.Servings in filters.keys():
        min_serv = filters[CustomFilterOptions.Servings]["min"]
        max_serv = filters[CustomFilterOptions.Servings]["max"]

        results = filter_by_num_servings(results, min_serv, max_serv, num_results)

    if CustomFilterOptions.Ingredients in filters.keys():
        min_ingr = filters[CustomFilterOptions.Ingredients]["min"]
        max_ingr = filters[CustomFilterOptions.Ingredients]["max"]

        results = filter_by_num_ingredients(results, min_ingr, max_ingr, num_results)

        # Retrieves more recipes if there are not enough to match the num_results parameter.
        num_calls = 0
        call_cap = 2
        while len(results) < num_results and num_calls < call_cap:
            num_calls += 1
            offset = num_calls * num_results

            additional_results = _get_results(query.add_offset(offset))

            if CustomFilterOptions.Price in filters.keys():
                min_price = filters[CustomFilterOptions.Price]["min"]
                max_price = filters[CustomFilterOptions.Price]["max"]

                additional_results = filter_by_price_range(results, min_price, max_price, num_results)

            if CustomFilterOptions.Servings in filters.keys():
                min_serv = filters[CustomFilterOptions.Servings]["min"]
                max_serv = filters[CustomFilterOptions.Servings]["max"]

                additional_results = filter_by_num_servings(results, min_serv, max_serv, num_results)

            if CustomFilterOptions.Ingredients in filters.keys():
                min_ingr = filters[CustomFilterOptions.Ingredients]["min"]
                max_ingr = filters[CustomFilterOptions.Ingredients]["max"]

                additional_results = filter_by_num_ingredients(results, min_ingr, max_ingr, num_results)

                results += additional_results

    return results


def filter_by_price_range(results: list, min_price: float, max_price: float, num_results: int = 10) -> list:
    """
    Filters a list of recipes by price
    :param results: the list of recipes
    :param min_price: minimum price
    :param max_price: maximum price
    :param num_results: number of results to return
    :return: filtered list
    """
    # If min price is not set
    if not min_price:
        min_price = 0

    # If max price is not set
    if not max_price:
        filtered_results = [x for x in results if min_price <= x["price"]]
    else:
        filtered_results = [x for x in results if min_price <= x["price"] <= max_price]

    return filtered_results


def filter_by_num_servings(results: list, min_serv: float, max_serv: float, num_results: int = 10) -> list:
    """
    Filters a  list of recipes by number of servings
    :param results: the list of recipes
    :param min_serv: minimum number of servings
    :param max_serv: maximum number of servings
    :param num_results: number of results to return
    :return: filtered list
    """
    # If min is not set
    if not min_serv:
        min_serv = 0

    # If max  is not set
    if not max_serv:
        filtered_results = [x for x in results if min_serv <= x["servings"]]
    else:
        filtered_results = [x for x in results if min_serv <= x["servings"] <= max_serv]

    return filtered_results


def filter_by_num_ingredients(results: list, min_ingr: float, max_ingr: float, num_results: int = 10) -> list:
    """
    Filters a list of recipes by number of ingredients
    :param results: the list of recipes
    :param min_ingr: minimum number of ingredients
    :param max_ingr: maximum number of ingredients
    :param num_results: number of results to return
    :return: filtered list
    """
    # If min is not set
    if not min_ingr:
        min_ingr = 0

    # If max  is not set
    if not max_ingr:
        filtered_results = [x for x in results if min_ingr <= len(x["ingredients"])]
    else:
        filtered_results = [x for x in results if min_ingr <= len(x["ingredients"]) <= max_ingr]

    return filtered_results


def _get_results(query: RecipeSearch) -> list:
    """
    Retrieves the title, summary, image, and price attributes for each recipe obtained from the API call 
    made using the specified URL.

    :param query: RecipeSearch object that represents the API call.
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
            'priceserving': r['pricePerServing'] / 100,
            'price': (r['pricePerServing'] * r['servings']) / 100,
            'id': r['id'],
            'servings': r['servings'],
            'ingredients': r['nutrition']['ingredients']

        }
        simplified_recipes.append(info)

    return simplified_recipes
