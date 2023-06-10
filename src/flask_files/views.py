from flask import Blueprint, request, url_for, redirect, render_template, flash
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required

views = Blueprint('views', __name__, template_folder="../templates")


@views.route("/")
def home_page():
    return render_template("index.html")


@views.route("/about")
def about_page():
    return render_template("about.html")


@views.route("/results")
def display_results():
    return render_template("display_results.html")


@views.route("/test")
@login_required
def test_login():
    return "<p> Logged In </p>"