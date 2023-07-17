from flask import Blueprint, request, url_for, redirect, render_template, flash, jsonify
from flask_login import current_user, login_required, login_user, logout_user
from src.flask_files import forms
from src.flask_files.database import mongo
from src.flask_files.models import User
from src.flask_files.extensions import bcrypt
from src.api_options import IntoleranceOptions
import src.email_util as email_util

accounts = Blueprint('accounts', __name__, template_folder="../templates", static_folder="../static")

client = mongo.cx
db = client["recipeapp"]
accounts_db = db["accounts"]
preferences_db = db["preferences"]
favorites_db = db["favorites"]
email_confirmations = db["email_confirmations"]


@accounts.route("/account", methods=['GET', 'POST'])
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


@accounts.route("/account/favorites", methods=['GET', 'POST'])
@login_required
def account_favorites():
    favorites = current_user.favorites['favorites']

    return render_template('account_favorites.html', favorites=favorites)


@accounts.route("/account/settings", methods=['GET', 'POST'])
@login_required
def account_settings():

    if not current_user.confirmed:
        flash("Please confirm your email before setting user preferences")
        return redirect("/account")

    require_relogin = False

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

            require_relogin = True

        # Update email
        if form.email.data:

            # confirmation email
            token = email_util.generate_token(form.email.data, 'email-confirm')
            confirmation_link = email_util.generate_confirmation_link(token, "auth.confirm_change_email")
            message = email_util.create_confirmation_email(form.email.data, confirmation_link)
            email_util.send_email(message)

            email_confirmations.insert_one({
                "token":  token,
                "id": user_info_id,
                "email": form.email.data
            })

            # set account to unverified
            accounts_db.update_one({"_id": user_info_id},
                                   {"$set": {"confirmed": False}})

            require_relogin = True

        # Update password
        if form.old_password.data and form.new_password.data and form.confirm_password.data:
            hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            accounts_db.update_one({"_id": user_info_id},
                                   {"$set": {"password": hashed_password}})

            require_relogin = True

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

        if require_relogin:
            logout_user()
            return redirect("/login")

        return redirect("/account")

    elif form.errors:
        flash(form.errors)

    form.process()
    return render_template("account_settings.html", form=form)


