import pdfkit
import jinja2
import recipe_info


def create_virtual_shopping_list(recipe_id: int):
    """
    Creates a shopping list  pdf by inserting title, cook time, summary, ingredients, and instructions of a recipe into
    an HTML template and converting the resulting webpage into a pdf.

    :param
        recipe_id: ID of the recipe
    :return:
        None
    """
    recipe = recipe_info.Recipe(recipe_id)

    title = recipe.get_title()
    ingredients = recipe.get_ingredients()
    instructions = recipe.get_instructions_list()
    time = recipe.get_prep_time()
    summary = recipe.get_summary()

    sentence_cutoff = _find_sentence_with_keyword(summary,  "serves")
    summary = _first_n_sentences(summary, sentence_cutoff + 1)
    summary = _remove_html_bold(summary)

    # Loading html template
    template_loader = jinja2.FileSystemLoader(searchpath="./templates")
    template_env = jinja2.Environment(loader=template_loader)
    template_file = "shopping_list.html"
    template = template_env.get_template(template_file)

    # Jinja variable substitution
    output = template.render(title=title, summary=summary, time=time, ingredients=ingredients,
                             instructions=instructions)

    # Write to HTML file
    html_file = open("shoppinglist.html", 'w')
    html_file.write(output)
    html_file.close()

    # Converting html to pdf. Must install wkhtmltopdf and point path to exe.
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    pdfkit.from_file("shoppinglist.html", "shoppinglist.pdf", configuration=config)


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


if __name__ == '__main__':
    create_virtual_shopping_list("662264")
