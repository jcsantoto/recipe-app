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

    sentences = summary.split('.')
    summary = sentences[0] + sentences[1] + sentences[2] + sentences[3]

    template_loader = jinja2.FileSystemLoader(searchpath="./templates")
    template_env = jinja2.Environment(loader=template_loader)
    template_file = "shopping_list.html"
    template = template_env.get_template(template_file)

    output = template.render(title=title, summary=summary, time=time, ingredients=ingredients,
                             instructions=instructions)
    html_file = open("shoppinglist.html", 'w')
    html_file.write(output)
    html_file.close()

    # Must install wkhtmltopdf and point path to exe.
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    pdfkit.from_file("shoppinglist.html", "shoppinglist.pdf", configuration=config)

