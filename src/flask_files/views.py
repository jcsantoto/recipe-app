from flask import Blueprint, request, url_for, redirect, render_template, flash, session, make_response
from flask_login import current_user, login_required
import pdfkit
import random
import time

import src.search as recipe_search
from src.flask_files import forms
from src.flask_files.database import mongo
from src import api_options as Options
from src.recipe_info import Recipe
from src.recipe_info_util import clean_summary
from src.recipe_recommend import get_similar_recipe

views = Blueprint('views', __name__, template_folder="../templates", static_folder="../static")

client = mongo.cx
db = client["recipeapp"]
accounts_db = db["accounts"]
preferences_db = db["preferences"]
favorites_db = db["favorites"]
recommendation_db = db["recommendation"]
search_history = db["SearchHistory"]



@views.route("/", methods=['GET'])
def home_page():
    form = forms.SearchForm()

    if current_user.is_authenticated:

        favorites = current_user.favorites['favorites']

        recommendations = current_user.load_recommendations()

        # If recommendation already exists
        if recommendations:

            # Check timestamp of when recommendation was given
            last_recommended_timestamp = recommendations["timestamp"]

            current_timestamp = time.time()

            elapsed_time = current_timestamp - last_recommended_timestamp

            # If recommendation is more than 2 hours old, generate new recommendation
            if elapsed_time >= 7200:

                basis, recommended_recipes = generate_recommendations()

                # update recommendation in database
                recommendation_db.update_one({"username": current_user.username},
                                             {"$set":{
                                                 "username": current_user.username,
                                                 "timestamp": time.time(),
                                                 "recipes": recommended_recipes,
                                                 "basis": basis
                                             }})

            # If not, display stored recommendation
            else:
                basis = recommendations['basis']
                recommended_recipes = recommendations['recipes']

            return render_template("index.html", form=form, original_name=basis, recommendation=recommended_recipes)

        # If recommendation doesn't exist, and if user has favorites,
        elif favorites:

            # generate new recommendation
            basis, recommended_recipes = generate_recommendations()

            # put recommendation in database with timestamp
            recommendation_db.insert_one({
                "username": current_user.username,
                "timestamp": time.time(),
                "recipes": recommended_recipes,
                "basis": basis
            })

            return render_template("index.html", form=form, original_name=basis, recommendation=recommended_recipes)

    return render_template("index.html", form=form)


@views.route("/about")
def about_page():
    return render_template("about.html")


@views.route("/search", methods=['GET', 'POST'])
def search():
    query = request.args.get('query')

    mode = Options.SearchMode(int(request.args.get('mode')))

    form = forms.SortAndFilterOptionsForm()
    unselected_intolerances = None

    # Set labels on the nutrition filter
    nutrition_labels = ["Calories", "Carbs", "Protein", "Fat"]
    num_labels = len(nutrition_labels)
    for i in range(num_labels):
        form.nutrition[i].label.text = nutrition_labels[i]

    # Set labels on custom filters
    custom_labels = ["Price", "Servings", "Ingredients"]
    num_custom_labels = len(custom_labels)
    for i in range(num_custom_labels):
        form.custom_filters[i].label.text = custom_labels[i]

    if form.validate_on_submit():
        filters = {}
        custom_filters = {}

        # sort
        if form.sort.data != Options.SortOptions.default:
            sort = Options.SortOptions(form.sort.data)
        else:
            sort = None

        # diet filter
        diets = form.diet.data

        # intolerance filter
        intolerances = form.intolerances.data

        # ingredient filter
        ingredients = form.ingredients.data

        # custom filter
        for field in form.custom_filters:
            name = field.label.text
            min_val = field.min_value.data
            max_val = field.max_value.data

            if min_val or max_val:
                custom_filters[Options.CustomFilterOptions(name)] = {"min": min_val, "max": max_val}

        # nutrition filter
        _parse_nutrition_filter(filters, form.nutrition)

        # If user is logged in, check intolerances
        if current_user.is_authenticated:
            user_preferences = current_user.preferences

            intolerance_list = Options.to_list(Options.IntoleranceOptions)
            user_intolerances_idx = user_preferences["intolerances"]
            user_intolerances = [intolerance_list[x].value for x in user_intolerances_idx]

            selected_intolerances = form.intolerances.data

            unselected_intolerances = list(set(user_intolerances).difference(selected_intolerances))

        results = recipe_search.search(query=query, mode=mode, sort=sort, filters=filters,
                                       diets=diets, ex_ingredients=ingredients, intolerances=intolerances,
                                       custom_filter=custom_filters)

        return render_template('display_results.html', query=query, results=results, form=form,
                               unselected_intolerances=unselected_intolerances)

    else:

        # If user is logged in, preselect preferences
        if current_user.is_authenticated:
            user_preferences = current_user.preferences

            intolerance_list = Options.to_list(Options.IntoleranceOptions)
            user_intolerances = user_preferences["intolerances"]
            form.intolerances.data = [intolerance_list[x].value for x in user_intolerances]

            user_macros = user_preferences["macros"]
            carbs = user_macros["carbohydrates"]
            protein = user_macros["protein"]
            fats = user_macros["fats"]

            if carbs:
                form.nutrition[1].min_value.data = carbs - 5
                form.nutrition[1].max_value.data = carbs + 5

            if protein:
                form.nutrition[2].min_value.data = protein - 5
                form.nutrition[2].max_value.data = protein + 5

            if fats:
                form.nutrition[3].min_value.data = fats - 5
                form.nutrition[3].max_value.data = fats + 5

            filters = {}
            _parse_nutrition_filter(filters, form.nutrition)

            results = recipe_search.search(query=query, mode=mode, filters=filters,
                                           intolerances=form.intolerances.data)

        else:
            results = recipe_search.search(query, mode=mode)

    return render_template('display_results.html', query=query, results=results, form=form)


@views.route("/recipe/<recipe_id>", methods=['GET', 'POST'])
def display_recipe(recipe_id):
    recipe_info = Recipe(recipe_id)
    title = recipe_info.get_title()
    summary = clean_summary(recipe_info.get_summary())
    ingredients = recipe_info.get_ingredients()
    instructions = recipe_info.get_instructions_list()
    prep_time = recipe_info.get_prep_time()
    price = recipe_info.get_total_Cost()
    macros = recipe_info.get_Macros()
    contains_intolerances = None
    favorite = False

    if current_user.is_authenticated:
        username = current_user.username

        user_favorites_info = favorites_db.find_one({"username": username})
        user_preferences_info = preferences_db.find_one({"username": username})

        user_favorites = user_favorites_info["favorites"]
        user_intolerances = Options.idx_to_option(user_preferences_info["intolerances"], Options.IntoleranceOptions)

        contains_intolerances = recipe_info.contains_intolerances(user_intolerances)

        add_to_search_history(recipe_id, title)

        if recipe_id in user_favorites:
            favorite = True

        if request.method == 'POST':

            # Favorite recipe
            if recipe_id in user_favorites:
                del user_favorites[recipe_id]
            else:
                user_favorites[recipe_id] = title

            favorites_db.update_one({"username": username}, {"$set": {"favorites": user_favorites}})

            return 'Action Completed'

    session["title"] = title
    session["ingredients"] = ingredients
    session["instructions"] = instructions
    session["time"] = prep_time

    return render_template('display_recipe.html', title=title, summary=summary, ingredients=ingredients,
                           instructions=instructions, contains_intolerances=contains_intolerances, favorite=favorite,
                           current_user=current_user, recipe_id=recipe_id,price = price, macros = macros)


@views.route("/pdf")
def shopping_list():
    title = session["title"]
    ingredients = session["ingredients"]
    instructions = session["instructions"]
    time = session["time"]

    rendered = render_template("shopping_list.html", title=title, time=time, ingredients=ingredients,
                               instructions=instructions)

    pdf = pdfkit.from_string(rendered, False)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=shoppinglist.pdf'

    return response


def _parse_nutrition_filter(filters, nutrition_form):
    for field in nutrition_form:
        name = field.label.text
        min_val = field.min_value.data
        max_val = field.max_value.data

        if min_val or max_val:
            filters[Options.ApiFilterOptions(name)] = {"min": min_val, "max": max_val}

            
def generate_recommendations():
    favorites = current_user.favorites['favorites']

    if favorites:
        recipe_name = random.choice(list(favorites.values()))

        extracted_recipes = []

        similar_recipes = get_similar_recipe(recipe_name)

        for item in similar_recipes:

            if item['title'] == recipe_name:
                continue

            extracted_recipes.append({
                "title": item['title'],
                "id": item['id'],
                "image": item['image']

            })

    return recipe_name, extracted_recipes

def add_to_search_history(recipe_id, recipe_name):
    user_history = search_history.find_one({"username": current_user.username})

    if user_history is None:
        search_history.insert_one({"username": current_user.username,
                                   "recipes": [{"recipe_id": recipe_id,
                                                "recipe_name": recipe_name
                                                }]
                                   })

        return

    recipe_list = user_history["recipes"]
    existing_id = next((d for d in recipe_list if d["recipe_id"] == recipe_id), None)

    if existing_id:
        recipe_list.remove(existing_id)
        recipe_list.insert(0, existing_id)

        search_history.update_one({"username": current_user.username},{"$set":{"recipes": recipe_list}})

    elif len(user_history["recipes"]) == 15:
        recipe_list.remove(14)
        recipe_list.insert(0,
                           {"recipe_id": recipe_id,
                            "recipe_name": recipe_name})

        search_history.update_one({"username": current_user.username}, {"$set": {"recipes": recipe_list}})

    else:
        recipe_list.insert(0,
                           {"recipe_id": recipe_id,
                            "recipe_name": recipe_name})

        search_history.update_one({"username": current_user.username}, {"$set": {"recipes": recipe_list}})

