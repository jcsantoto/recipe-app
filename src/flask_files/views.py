from flask import Blueprint, request, url_for, redirect, render_template, flash
from flask_login import current_user, login_required
import src.flask_files.forms as forms
from src.flask_files.database import mongo
from src.search import search
from src.api_url_builder import SortOptions, FilterOptions, SearchMode

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
        sort = SortOptions(form.sort.data)

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

        results = search(query=query, mode=SearchMode.ByName, sort=sort, filters=filters,
                         filter_settings=filter_settings, diets=diets, ex_ingredients=ingredients)

        return render_template('display_results.html', query=query, results=results, form=form)

    else:
        results = search(query, mode=SearchMode.ByName)

    return render_template('display_results.html', query=query, results=results, form=form)
