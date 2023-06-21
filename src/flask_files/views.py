from flask import Blueprint, request, url_for, redirect, render_template, flash
from flask_login import current_user, login_required
from src.flask_files import forms
from src.flask_files.database import mongo

views = Blueprint('views', __name__, template_folder="../templates", static_folder="../static")

@views.route("/", methods=['GET'])
def home_page():
    return render_template("index.html")

@views.route("/about")
def about_page():
    return render_template("about.html")

@views.route("/results")
def display_results():
    return render_template("display_results.html")

@views.route("/passreset")
def password_reset():
    return render_template("password_reset.html")







