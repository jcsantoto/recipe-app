from flask import Blueprint, request, url_for, redirect, render_template, flash
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required

views = Blueprint('views', __name__, template_folder="../templates", static_folder="../static")


@views.route("/")
def home_page():
    return render_template("index.html")


@views.route("/about")
def about_page():
    return render_template("about.html")


@views.route("/account")
@login_required
def account_page():
    username = current_user.username
    email = current_user.email

    return render_template("account.html", username=username, email=email)


@views.route("/results")
def display_results():
    return render_template("display_results.html")


