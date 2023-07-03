# Allergens
# dairy and gluten covered
tree_nuts = ["almond", "brazil nut", "cashew", "hazelnut", "macadamia nut", "pecan", "pine nut", "pistachio", "walnut"]

grain = ["corn", "flax", "millet", "rice", "quinoa", "sorghum", "buckwheat"]

shellfish = ["shrimp", "crayfish", "crab", "lobster", "clams", "scallop", "oyster", "mussel"]

soy = ["soy", "miso", "edamame", "natto", "tamari", "tofu", "tempeh"]

sulfite_aisles = ["Ethnic Foods", "Condiments", "Canned and Jarred", "Baking", "Vinegar", "Alcohol"]

sulfite = ["lemon juice", "lime juice"]


def check_for_peanuts(ingredients: list) -> bool:
    """
    Checks if an ingredients list contains peanut by checking if an ingredient has the word peanut in it
    :param ingredients: List of ingredients
    :return: If the list contains peanut
    """
    for ingr in ingredients:
        if "peanut" in ingr["name"]:
            return True

    return False


def check_for_egg(ingredients: list) -> bool:
    """
    Checks if an ingredients list contains egg by checking if the ingredient belongs to the egg aisle.
    :param ingredients: List of ingredients
    :return: If the list contains egg
    """
    for ingr in ingredients:
        if "egg" in ingr["name"] and "Egg" in ingr["aisle"]:
            return True

    return False


def check_for_sesame(ingredients: list) -> bool:
    """
    Checks if an ingredients list contains seafood by checking if an ingredient has the word sesame in it.
    :param ingredients: List of ingredients
    :return: If the list contains sesame
    """
    for ingr in ingredients:
        if "sesame" in ingr["name"]:
            return True

    return False


def check_for_seafood(ingredients: list) -> bool:
    """
    Checks if an ingredients list contains seafood by checking if an ingredient belongs to the seafood aisle.
    :param ingredients: List of ingredients
    :return: If the list contains seafood
    """
    for ingr in ingredients:
        if ingr["aisle"] == "Seafood":
            return True

        return False


def check_for_sulfite(ingredients: list) -> bool:
    """
    Checks if an ingredient list contains a sulfite by checking if the ingredient comes from a store aisle that contains
    ingredients that likely have sulfite. Also checks against a list of ingredients that contain sulfite
    :param ingredients: List of ingredients
    :return: If the list contains sulfite or likely to contain sulfite
    """
    for ingr in ingredients:
        if any(item in ingr["aisle"] for item in sulfite_aisles):
            return True

        if any(item in ingr["name"] for item in sulfite):
            return True

        return False


def check_for_shellfish(ingredients: list) -> bool:
    """
    Checks if an ingredient list contains a shellfish by checking it against the shellfish list.
    :param ingredients: List of ingredients
    :return: If the list contains shellfish
    """
    for ingr in ingredients:
        if any(item in ingr["name"] for item in shellfish):
            return True

    return False


def check_for_soy(ingredients: list) -> bool:
    """
    Checks if an ingredient list contains a soy by checking it against the soy list.
    :param ingredients: List of ingredients
    :return: If the list contains soy
    """
    for ingr in ingredients:
        if any(item in ingr["name"] for item in soy):
            return True

    return False


def check_for_grain(ingredients: list) -> bool:
    """
    Checks if an ingredient list contains a grain by checking it against the grain list.
    :param ingredients: List of ingredients
    :return: If the list contains grain
    """
    for ingr in ingredients:
        if any(item in ingr["name"] for item in grain):
            return True

    return False


def check_for_tree_nuts(ingredients: list) -> bool:
    """
    Checks if an ingredient list contains a tree nut by checking it against the tree nut list.
    :param ingredients: List of ingredients
    :return: If the list contains tree nut
    """
    for ingr in ingredients:
        if any(item in ingr["name"] for item in tree_nuts):
            return True

    return False


def clean_summary(summary: str) -> str:
    """
    Trims and cleans a recipe's summary by removing certain sentences and removing certain html tags.
    :param summary: summary of a recipe
    :return: modified summary
    """
    sentence_cutoff = _find_sentence_with_keyword(summary, "serves")
    summary = _first_n_sentences(summary, sentence_cutoff + 1)
    summary = _remove_html_bold(summary)

    return summary


def _remove_html_bold(text: str) -> str:
    """
    Removes the html tags for bolding a sentence"
    :param text: text
    :return: modified text
    """
    unbolded_text = text.replace("<b>", "")
    unbolded_text = unbolded_text.replace("</b>", "")

    return unbolded_text


def _first_n_sentences(text: str, n: int) -> str:
    """
    Retrieves the first n sentences from a paragraph.
    :param text: Paragraph
    :param n: number of sentences to retrieve
    :return: Modified sentence
    """
    if n < 1:
        return text

    sentences = text.split('. ')
    first_n = ""
    for i in range(n):
        first_n = first_n + sentences[i] + ". "

    return first_n


def _find_sentence_with_keyword(text: str, keyword: str) -> int:
    """
    Returns the sentence in a paragraph that contains a keyword.
    :param text: Paragraph
    :param keyword: The keyword
    :return: The number of the sentence
    """
    sentences = text.split('. ')
    for index, sentence, in enumerate(sentences):
        if keyword in sentence:
            return index

    return -1
