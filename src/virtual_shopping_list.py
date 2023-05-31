import pdfkit
import jinja2
import recipe_info


def create_virtual_shopping_list(recipe_id: int):
    recipe = recipe_info.Recipe(recipe_id)

    title = recipe.get_title()
    ingredients = recipe.get_ingredients()
    instructions = recipe.get_instructions_list()
    time = recipe.get_prep_time()
    summary = recipe.get_summary()


    template_loader = jinja2.FileSystemLoader(searchpath="./templates")
    template_env = jinja2.Environment(loader=template_loader)
    template_file = "shopping_list.html"
    template = template_env.get_template(template_file)

    output = template.render(title=title, summary=summary, time=time, ingredients=ingredients, instructions=instructions)
    html_file = open("shoppinglist.html", 'w')
    html_file.write(output)
    html_file.close()


if __name__ == '__main__':
    create_virtual_shopping_list("1095810")
