tree_nuts = ["almonds", "brazil nut", "cashew", "hazelnut", "macadamia nut", "pecan", "pine nut", "pistachio", "walnut"]
# dairy and gluten covered
egg = "egg"
peanut = "peanuts"
grain = ["flour"]


def clean_summary(summary: str) -> str:
    sentence_cutoff = _find_sentence_with_keyword(summary,  "serves")
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

