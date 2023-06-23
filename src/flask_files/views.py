from flask import Blueprint, request, url_for, redirect, render_template, flash, session, make_response
from flask_login import current_user, login_required
import pdfkit

import src.search as recipe_search
from src.flask_files import forms
from src.flask_files.database import mongo
from src import api_options as Options
from src.recipe_info import Recipe
from src.recipe_info_util import clean_summary

views = Blueprint('views', __name__, template_folder="../templates", static_folder="../static")

client = mongo.cx
db = client["recipeapp"]
accounts_db = db["accounts"]


@views.route("/", methods=['GET'])
def home_page():
    return render_template("index.html")


@views.route("/about")
def about_page():
    return render_template("about.html")

@views.route("/passreset")
def password_reset():
    return render_template("password_reset.html")

@views.route("/search", methods=['GET', 'POST'])
def search():
    query = request.args.get('query')

    form = forms.SortAndFilterOptionsForm()
    notices = None

    # Set labels on the nutrition filter
    nutrition_labels = ["Calories", "Carbs", "Fat"]
    num_labels = len(nutrition_labels)
    for i in range(num_labels):
        form.nutrition[i].label.text = nutrition_labels[i]

    if form.validate_on_submit():
        filters = []
        filter_settings = []

        # diet filter
        diets = form.diet.data

        # intolerance filter
        intolerances = form.intolerances.data

        # sort
        if form.sort.data != Options.SortOptions.default:
            sort = Options.SortOptions(form.sort.data)
        else:
            sort = None

        # ingredient filter
        ingredients = form.ingredients.data

        # price filter
        min_price = form.min_price.data
        max_price = form.max_price.data
        if min_price or max_price:
            filters.append(Options.FilterOptions.Price)
            filter_settings.append({"min": min_price,
                                    "max": max_price})

        # nutrition filter
        for field in form.nutrition:
            name = field.label.text
            min_val = field.min_value.data
            max_val = field.max_value.data

            if min_val or max_val:
                filters.append(Options.FilterOptions(name))
                filter_settings.append({"min": min_val,
                                        "max": max_val})

        # If user is logged in, check intolerances
        if current_user.is_authenticated:
            username = current_user.username

            user_info = accounts_db.find_one({"username": username})

            intolerance_list = Options.to_list(Options.IntoleranceOptions)
            user_intolerances_idx = user_info["intolerances"]
            user_intolerances = [intolerance_list[x].value for x in user_intolerances_idx]

            selected_intolerances = form.intolerances.data

            diff = list(set(user_intolerances).difference(selected_intolerances))

            notices = ["Warning: Your user preferences indicate you are intolerant to " + x +
                       ". The recipes shown may contain this ingredient. Select " + x +
                       " under the Intolerances section to filter out recipes containing that ingredient"
                       for x in diff]

        results = recipe_search.search(query=query, mode=Options.SearchMode.ByName, sort=sort, filters=filters,
                                       filter_settings=filter_settings, diets=diets, ex_ingredients=ingredients,
                                       intolerances=intolerances)

        return render_template('display_results.html', query=query, results=results, form=form, notices=notices)

    else:

        # If user is logged in, preselect intolerances
        if current_user.is_authenticated:
            username = current_user.username

            user_info = accounts_db.find_one({"username": username})

            intolerance_list = Options.to_list(Options.IntoleranceOptions)
            user_intolerances = user_info["intolerances"]

            form.intolerances.data = [intolerance_list[x].value for x in user_intolerances]

            results = recipe_search.search(query, mode=Options.SearchMode.ByName, intolerances=form.intolerances.data)

        else:
            results = recipe_search.search(query, mode=Options.SearchMode.ByName)

    return render_template('display_results.html', query=query, results=results, form=form, notices=notices)


@views.route("/recipe/<recipe_id>", methods=['GET', 'POST'])
def display_recipe(recipe_id):
    recipe_info = Recipe(recipe_id)

    title = recipe_info.get_title()
    summary = clean_summary(recipe_info.get_summary())
    ingredients = recipe_info.get_ingredients()
    instructions = recipe_info.get_instructions_list()
    time = recipe_info.get_prep_time()
    contains_intolerances = None

    if current_user.is_authenticated:
        username = current_user.username

        user_info = accounts_db.find_one({"username": username})

        user_intolerances = Options.idx_to_option(user_info["intolerances"], Options.IntoleranceOptions)

        contains_intolerances = recipe_info.contains_intolerances(user_intolerances)

    session["title"] = title
    session["summary"] = summary
    session["ingredients"] = ingredients
    session["instructions"] = instructions
    session["time"] = time

    return render_template('display_recipe.html', title=title, summary=summary, ingredients=ingredients,
                           instructions=instructions, contains_intolerances=contains_intolerances)


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
