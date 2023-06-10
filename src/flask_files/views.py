from flask import Blueprint, request, url_for, redirect, render_template, flash

views = Blueprint('views', __name__, template_folder="./templates")


@views.route("/")
def home_page():
    return render_template("index.html")


@views.route("/about")
def about_page():
    return render_template("about.html")


@views.route("/results")
def display_results():
    return render_template("display_results.html")