from flask import Blueprint, request, url_for, redirect, render_template, flash
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from src.flask_files import forms
from src.flask_files.extensions import login_manager, bcrypt
from src.flask_files.models import User
from src.flask_files.database import mongo

# Setting up database
client = mongo.cx
db = client["recipeapp"]
accounts_db = db["accounts"]
favorites_db = db["favorites"]
preferences_db = db["preferences"]

auth = Blueprint('auth', __name__, template_folder="../templates", static_folder="../static")
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # if user is already logged in, redirect to homepage
    if current_user.is_authenticated:
        return redirect("/")

    # creates login form object
    form = forms.LoginForm()

    # validates form
    if form.validate_on_submit():

        # looks for entries in the database with a matching email from the form
        user = accounts_db.find_one({"email": form.email.data})

        # checks if user is not null. checks if password matches
        if user and bcrypt.check_password_hash(user["password"], form.password.data):
            user_object = User(user["username"], user["email"], user["password"])

            # logs user in
            login_user(user_object, remember=form.remember.data)

            flash("Login Successful")
            return redirect("/")

        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template("login.html", form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Successfully logged out.")
    return redirect("/")


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect("/")

    form = forms.RegistrationForm()
    if form.validate_on_submit():
        # encrypts password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        new_user_info = {"username": form.username.data,
                         "email": form.email.data,
                         "password": hashed_password
                         }

        new_user_preferences = {
            "username": form.username.data,
            "intolerances": [],
            "macros": {"carbohydrates": None,
                       "protein": None,
                       "fats": None}
        }

        # inserts new entries in database
        accounts_db.insert_one(new_user_info)
        preferences_db.insert_one(new_user_preferences)
        favorites_db.insert_one({"username": form.username.data, "favorites": {}})

        flash('Your account has been created! You are now able to log in', 'success')

        return redirect("/login")

    return render_template("register.html", form=form)


@login_manager.user_loader
def load_user(user_id):
    user = accounts_db.find_one({"username": user_id})

    if user:
        return User(user["username"], user["email"], user["password"])

    return None
