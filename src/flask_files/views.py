from flask import Blueprint, request, url_for, redirect, render_template, flash, session, make_response, jsonify
from flask_login import current_user, login_required
import pdfkit, json
import pdfkit
from bson.objectid import ObjectId
import random
import time

import src.search as recipe_search
import src.trending_recipe as trending_recipe_util
from src.flask_files import forms
from src.flask_files.database import mongo
from src import api_options as Options
from src.recipe_info import Recipe, contains_intolerances
from src.recipe_info_util import clean_summary
from src.user_recipes import UserRecipe, decompress_data
from src.recipe_recommend import get_similar_recipe


views = Blueprint('views', __name__, template_folder="../templates", static_folder="../static")

client = mongo.cx
db = client["recipeapp"]
accounts_db = db["accounts"]
preferences_db = db["preferences"]
favorites_db = db["favorites"]
user_recipes = db["user_recipes"]
recommendation_db = db["recommendation"]
search_history = db["SearchHistory"]


@views.route("/clear", methods=['GET'])
def clear():
    trending_recipe_util.clear_cache()

@views.route("/", methods=['GET'])
def home_page():
    form = forms.SearchForm()

    trending_recipes = trending_recipe_util.get_trending_recipes()

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

            return render_template("index.html", form=form, original_name=basis, recommendation=recommended_recipes,
                                   trending_recipes=trending_recipes)

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

            return render_template("index.html", form=form, original_name=basis, recommendation=recommended_recipes,
                                   trending_recipes=trending_recipes)

    return render_template("index.html", form=form, trending_recipes=trending_recipes)


@views.route("/about")
def about_page():
    return render_template("about.html")


@views.route("/passreset")
def password_reset():
    return render_template("password_reset.html")


@views.route("/community", methods=['GET', 'POST'])
@login_required
def community_home():
    form = forms.SearchForm()

    return render_template("community.html", form=form)


@views.route("/community/search", methods=['GET', 'POST'])
@login_required
def search_user_recipe():
    query = request.args.get('query')
    # user_recipes.create_index([('title', 'text'), ('ingredients', 'text')])

    results = user_recipes.find({"$text": {"$search": query}})

    recipes = []
    for item in results:
        recipes.append({
            "id": str(item['_id']),
            "title": item['title'],
            'description': decompress_data(item['description'])
        })

    return render_template("user_recipe_results.html", results=recipes)


@views.route("/recipe/community/<recipe_id>", methods=['GET', 'POST'])
@login_required
def display_user_recipe(recipe_id):
    recipe_info = UserRecipe()
    recipe_info.load_from_database(ObjectId(recipe_id))

    title = recipe_info.title
    summary = recipe_info.description
    ingredients = recipe_info.ingredients
    instructions = recipe_info.instructions
    prep_time = recipe_info.time
    owner = recipe_info.owner
    intolerances = [Options.IntoleranceOptions(x) for x in recipe_info.intolerances]
    favorite = False
    matching_intolerances = None

    session["title"] = title
    session["ingredients"] = ingredients
    session["instructions"] = instructions
    session["time"] = prep_time

    if current_user.is_authenticated:
        username = current_user.username

        user_favorites_info = favorites_db.find_one({"username": username})
        user_preferences_info = preferences_db.find_one({"username": username})

        user_favorites = user_favorites_info["favorites"]
        user_intolerances = Options.idx_to_option(user_preferences_info["intolerances"], Options.IntoleranceOptions)

        matching_intolerances = set(user_intolerances).intersection(intolerances)

        community_recipe_id = 'community/' + recipe_id

        if community_recipe_id in user_favorites:
            favorite = True

        if request.method == 'POST':

            # Favorite recipe
            if community_recipe_id in user_favorites:
                del user_favorites[community_recipe_id]
            else:
                user_favorites[community_recipe_id] = title

            favorites_db.update_one({"username": username}, {"$set": {"favorites": user_favorites}})

            return 'Action Completed'

    return render_template("user_recipe_info.html", title=title, summary=summary, ingredients=ingredients,
                           instructions=instructions, time=prep_time, owner=owner, favorite=favorite,
                           contains_intolerances=matching_intolerances, recipe_id=recipe_id)


@views.route("/submit-recipe", methods=['GET', 'POST'])
@login_required
def submit_recipe():
    form = forms.UserRecipeForm()

    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        prep_time = form.time.data
        ingredients = form.ingredients.data
        instructions = form.instructions.data
        diet = form.diet.data
        intolerances = form.intolerances.data

        for item in ingredients:
            del item['csrf_token']

        for item in instructions:
            del item['csrf_token']

        recipe = UserRecipe()

        recipe.set_title(title)
        recipe.set_description(description)
        recipe.set_time(prep_time)
        recipe.set_diets(diet)
        recipe.set_intolerances(intolerances)
        recipe.set_ingredients(ingredients)
        recipe.set_instructions(instructions)

        recipe.set_owner(current_user.username)

        recipe.add_to_database()

        flash("Recipe successfully submitted")

        return redirect("/community")

    return render_template("submit_recipe.html", form=form)

  
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

        # cuisine Filter
        cuisines = form.Cuisines.data

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
                                       custom_filter=custom_filters, cuisine=cuisines)

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
                                           intolerances=form.intolerances.data, cuisine=form.Cuisines.data)

        else:
            results = recipe_search.search(query, mode=mode)

    return render_template('display_results.html', query=query, results=results, form=form)


@views.route("/favorite/recipe/<recipe_id>", methods=['GET', 'POST'])
def favorite_recipe(recipe_id):

    username = current_user.username

    user_favorites_info = favorites_db.find_one({"username": username})
    user_favorites = user_favorites_info["favorites"]

    if request.method == 'POST':

        title = request.form['title'].strip()

        # Favorite recipe
        if recipe_id in user_favorites:
            del user_favorites[recipe_id]
        else:
            pass
            user_favorites[recipe_id] = title

        favorites_db.update_one({"username": username}, {"$set": {"favorites": user_favorites}})

        return 'Action Completed'


@views.route("/recipe/<recipe_id>", methods=['GET', 'POST'])
def display_recipe(recipe_id):
    favorite = False
    title = None

    if request.method == 'POST':

        recipe_data = request.get_json()
        title = recipe_data['title']
        trending_recipe_util.increment_view_count(recipe_id, title)

        if current_user.is_authenticated:
            username = current_user.username

            user_favorites_info = favorites_db.find_one({"username": username})
            user_preferences_info = preferences_db.find_one({"username": username})

            user_favorites = user_favorites_info["favorites"]
            user_intolerances = Options.idx_to_option(user_preferences_info["intolerances"], Options.IntoleranceOptions)

            add_to_search_history(recipe_id, title)

            if recipe_id in user_favorites:
                favorite = True

            ingredients = recipe_data['ingredients']
            dairy_free = recipe_data['dairyFree']
            gluten_free = recipe_data["glutenFree"]

            intolerances = contains_intolerances(ingredients, dairy_free, gluten_free, user_intolerances)

            return jsonify(intolerances)

    return render_template('display_recipe.html', recipe_id=recipe_id, favorite=favorite)


@views.route("/retrieve-recipe/<recipe_id>", methods=['GET', 'POST'])
def retrieve_recipe(recipe_id):

    recipe = Recipe(recipe_id)

    recipe_info = {
        "title": recipe.get_title(),
        "summary": clean_summary(recipe.get_summary()),
        "ingredients": recipe.get_ingredients(),
        "instructions": recipe.get_instructions_list(),
        "time": recipe.get_prep_time(),
        "dairyFree": recipe.recipe_info["dairyFree"],
        "glutenFree": recipe.recipe_info["glutenFree"],
        "price": recipe.get_total_Cost(),
        "macros": recipe.get_Macros()
    }

    session["title"] = recipe_info['title']
    session["ingredients"] = recipe_info['ingredients']
    session["instructions"] = recipe_info['instructions']
    session["time"] = recipe_info['time']

    response_data = jsonify(recipe_info)
    response = make_response(response_data)
    response.headers['Cache-Control'] = 'public, max-age=3600'

    # Handle conditional requests
    if_none_match = request.headers.get('If-None-Match')
    if if_none_match and if_none_match == response.headers.get('ETag'):
        return '', 304  # Respond with 304 Not Modified if the data is still fresh

    return response


@views.route("/pdf")
def shopping_list():
    title = session["title"]
    ingredients = session["ingredients"]
    instructions = session["instructions"]
    prep_time = session["time"]

    rendered = render_template("shopping_list.html", title=title, time=prep_time, ingredients=ingredients,
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

