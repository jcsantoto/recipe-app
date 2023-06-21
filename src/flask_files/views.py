from flask import Blueprint, request, url_for, redirect, render_template, flash, session, make_response
from flask_login import current_user, login_required
import pdfkit

import src.search as recipe_search
from src.flask_files import forms
from src.flask_files.database import mongo
from src.api_options import SortOptions, FilterOptions, SearchMode
from src.recipe_info import Recipe
from src.recipe_info_util import clean_summary

views = Blueprint('views', __name__, template_folder="../templates", static_folder="../static")


@views.route("/", methods=['GET'])
def home_page():
    return render_template("index.html")


@views.route("/about")
def about_page():
    return render_template("about.html")


@views.route("/search", methods=['GET', 'POST'])
def search():
    query = request.args.get('query')

    form = forms.SortAndFilterOptionsForm()

    nutrition_labels = ["Calories", "Carbs", "Fat"]
    num_labels = len(nutrition_labels)

    for i in range(num_labels):
        form.nutrition[i].label.text = nutrition_labels[i]

    if form.validate_on_submit():
        filters = []
        filter_settings = []

        # diet filter
        diets = form.diet.data

        # sort
        if form.sort.data != SortOptions.default:
            sort = SortOptions(form.sort.data)
        else:
            sort = None

        # ingredient filter
        ingredients = form.ingredients.data

        # price filter
        min_price = form.min_price.data
        max_price = form.max_price.data
        if min_price or max_price:
            filters.append(FilterOptions.Price)
            filter_settings.append({"min": min_price,
                                    "max": max_price})

        # nutrition filter
        for field in form.nutrition:
            name = field.label.text
            min_val = field.min_value.data
            max_val = field.max_value.data

            if min_val or max_val:
                filters.append(FilterOptions(name))
                filter_settings.append({"min": min_val,
                                        "max": max_val})

        results = recipe_search.search(query=query, mode=SearchMode.ByName, sort=sort, filters=filters,
                                       filter_settings=filter_settings, diets=diets, ex_ingredients=ingredients)

        return render_template('display_results.html', query=query, results=results, form=form)

    else:
        results = recipe_search.search(query, mode=SearchMode.ByName)

    return render_template('display_results.html', query=query, results=results, form=form)


@views.route("/recipe/<recipe_id>", methods=['GET', 'POST'])
def display_recipe(recipe_id):
    recipe_info = Recipe(recipe_id)

    title = recipe_info.get_title()
    summary = clean_summary(recipe_info.get_summary())
    ingredients = recipe_info.get_ingredients()
    instructions = recipe_info.get_instructions_list()
    time = recipe_info.get_prep_time()

    session["title"] = title
    session["summary"] = summary
    session["ingredients"] = ingredients
    session["instructions"] = instructions
    session["time"] = time

    return render_template('display_recipe.html', title=title, summary=summary, ingredients=ingredients,
                           instructions=instructions)


@views.route("/pdf")
def shopping_list():
    title = session["title"]
    summary = session["summary"]
    ingredients = session["ingredients"]
    instructions = session["instructions"]
    time = session["time"]

    rendered = render_template("shopping_list.html", title=title, summary=summary, time=time, ingredients=ingredients,
                               instructions=instructions)

    pdf = pdfkit.from_string(rendered, False)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=shoppinglist.pdf'

    return response
