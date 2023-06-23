# Allergens
# dairy and gluten covered
tree_nuts = ["almond", "brazil nut", "cashew", "hazelnut", "macadamia nut", "pecan", "pine nut", "pistachio", "walnut"]

grain = ["corn", "flax", "millet", "rice", "quinoa", "sorghum", "buckwheat"]

shellfish = ["shrimp", "crayfish", "crab", "lobster", "clams", "scallop", "oyster", "mussel"]

soy = ["soy", "miso", "edamame", "natto", "tamari", "tofu", "tempeh"]

sulfite_aisles = ["Ethnic Foods", "Condiments", "Canned and Jarred", "Baking", "Vinegar", "Alcohol"]

sulfite = ["lemon juice", "lime juice"]


def check_for_peanuts(ingredients: list) -> bool:
    for ingr in ingredients:
        if "peanut" in ingr["name"]:
            return True

    return False


def check_for_egg(ingredients: list) -> bool:
    for ingr in ingredients:
        if "egg" in ingr["name"] and "Egg" in ingr["aisle"]:
            return True

    return False


def check_for_sesame(ingredients: list) -> bool:
    for ingr in ingredients:
        if "sesame" in ingr["name"]:
            return True

    return False


def check_for_seafood(ingredients: list) -> bool:
    for ingr in ingredients:
        if ingr["aisle"] == "Seafood":
            return True

        return False


def check_for_sulfite(ingredients: list) -> bool:
    for ingr in ingredients:
        if any(item in ingr["aisle"] for item in sulfite_aisles):
            return True

        if any(item in ingr["name"] for item in sulfite):
            return True

        return False


def check_for_shellfish(ingredients: list) -> bool:
    for ingr in ingredients:
        if any(item in ingr["name"] for item in shellfish):
            return True

    return False


def check_for_soy(ingredients: list) -> bool:
    for ingr in ingredients:
        if any(item in ingr["name"] for item in soy):
            return True

    return False


def check_for_grain(ingredients: list) -> bool:
    for ingr in ingredients:
        if any(item in ingr["name"] for item in grain):
            return True

    return False


def check_for_tree_nuts(ingredients: list) -> bool:
    for ingr in ingredients:
        if any(item in ingr["name"] for item in tree_nuts):
            return True

    return False


def clean_summary(summary: str) -> str:
    sentence_cutoff = _find_sentence_with_keyword(summary, "serves")
    summary = _first_n_sentences(summary, sentence_cutoff + 1)
    summary = _remove_html_bold(summary)

    return summary


def _remove_html_bold(text: str) -> str:
    unbolded_text = text.replace("<b>", "")
    unbolded_text = unbolded_text.replace("</b>", "")

    return unbolded_text


def _first_n_sentences(text: str, n: int) -> str:
    if n < 1:
        return text

    sentences = text.split('. ')
    first_n = ""
    for i in range(n):
        first_n = first_n + sentences[i] + ". "

    return first_n


def _find_sentence_with_keyword(text: str, keyword: str) -> int:
    sentences = text.split('. ')
    for index, sentence, in enumerate(sentences):
        if keyword in sentence:
            return index

    return -1
