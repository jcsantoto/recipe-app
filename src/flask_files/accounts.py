from flask import Blueprint, request, url_for, redirect, render_template, flash
from flask_login import current_user, login_required, login_user
from src.flask_files import forms
from src.flask_files.database import mongo
from src.flask_files.models import User
from src.flask_files.extensions import bcrypt
from src.api_options import IntoleranceOptions

from enum import Enum

accounts = Blueprint('accounts', __name__, template_folder="../templates", static_folder="../static")

client = mongo.cx
db = client["recipeapp"]
accounts_db = db["accounts"]
favorites_db = db["favorites"]


@accounts.route("/account")
@login_required
def account_page():
    username = current_user.username
    email = current_user.email
    intolerance_list = [x for x in IntoleranceOptions]

    intolerance_idx = current_user.intolerances
    intolerances = ",".join([intolerance_list[x].name for x in intolerance_idx])

    favorites = favorites_db.find_one({"username": username})["favorites"]

    return render_template("account.html", username=username, email=email, intolerances=intolerances,
                           favorites=favorites)


@accounts.route("/account/settings", methods=['GET', 'POST'])
@login_required
def account_settings():
    form = forms.AccountSettingsForm()

    username = current_user.username

    user_info = accounts_db.find_one({"username": username})

    form.intolerances.default = user_info["intolerances"]

    if form.validate_on_submit():

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
        accounts_db.update_one({"_id": user_info_id},
                               {"$set": {"intolerances": form.intolerances.data}})

        updated_user = User(current_user.username, current_user.email, current_user.password_hash, current_user.intolerances)
        login_user(updated_user)

        flash("Changes saved")

        return redirect("/account")

    else:
        flash(form.errors)

    form.process()
    return render_template("account_settings.html", form=form)
