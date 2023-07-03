from flask import Blueprint, request, url_for, redirect, render_template, flash
from flask_login import current_user, login_required, login_user
from src.flask_files import forms
from src.flask_files.database import mongo
from src.flask_files.models import User
from src.flask_files.extensions import bcrypt
from src.api_options import IntoleranceOptions

accounts = Blueprint('accounts', __name__, template_folder="../templates", static_folder="../static")

client = mongo.cx
db = client["recipeapp"]
accounts_db = db["accounts"]
preferences_db = db["preferences"]
favorites_db = db["favorites"]


@accounts.route("/account")
@login_required
def account_page():
    username = current_user.username
    email = current_user.email
    intolerance_list = [x for x in IntoleranceOptions]

    intolerance_idx = current_user.preferences["intolerances"]
    intolerances = ",".join([intolerance_list[x].name for x in intolerance_idx])

    favorites = favorites_db.find_one({"username": username})["favorites"]

    return render_template("account.html", username=username, email=email, intolerances=intolerances,
                           favorites=favorites)


@accounts.route("/account/settings", methods=['GET', 'POST'])
@login_required
def account_settings():

    if not current_user.confirmed:
        flash("Please confirm your email before setting user preferences")
        return redirect("/account")

    form = forms.AccountSettingsForm()

    username = current_user.username

    user_info = accounts_db.find_one({"username": username})
    user_preferences = current_user.preferences

    # Displaying current username and email
    form.username.render_kw = {"placeholder": username}
    form.email.render_kw = {"placeholder": current_user.email}

    # Displaying saved intolerances
    form.intolerances.default = user_preferences["intolerances"]

    # Displaying saved macros
    macros = user_preferences["macros"]
    form.carbohydrates.default = macros["carbohydrates"]
    form.protein.default = macros["protein"]
    form.fats.default = macros["fats"]

    if form.submit.data and form.validate():

        user_info_id = user_info['_id']

        # Update username
        if form.username.data:
            accounts_db.update_one({"_id": user_info_id},
                                   {"$set": {"username": form.username.data}})
            current_user.username = form.username.data

        # Update email
        if form.email.data:
            accounts_db.update_one({"_id": user_info_id},
                                   {"$set": {"email": form.email.data}})
            current_user.email = form.email.data

        # Update password
        if form.old_password.data and form.new_password.data and form.confirm_password.data:
            hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            accounts_db.update_one({"_id": user_info_id},
                                   {"$set": {"password": hashed_password}})

        # Set Intolerances
        preferences_db.update_one({"username": username},
                                  {"$set": {"intolerances": form.intolerances.data}})

        # Set Macros
        preferences_db.update_one({"username": username},
                                  {"$set":
                                      {"macros": {
                                          "carbohydrates": form.carbohydrates.data,
                                          "protein": form.protein.data,
                                          "fats": form.fats.data
                                      }}})
        flash("Changes saved")

        updated_user = User(current_user.username, current_user.email, current_user.password_hash, current_user.confirmed)
        login_user(updated_user)

        return redirect("/account")

    elif form.errors:
        flash(form.errors)

    form.process()
    return render_template("account_settings.html", form=form)
