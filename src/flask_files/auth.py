from flask import Blueprint, request, url_for, redirect, render_template, flash
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from src.flask_files import forms
from src.flask_files.extensions import login_manager, bcrypt
from src.flask_files.models import User
from src.flask_files.database import mongo
import src.email_util as email_util

auth = Blueprint('auth', __name__, template_folder="../templates", static_folder="../static")
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Setting up database
client = mongo.cx
db = client["recipeapp"]
accounts_db = db["accounts"]
favorites_db = db["favorites"]
preferences_db = db["preferences"]
email_confirmations = db["email_confirmations"]


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # if user is already logged in, redirect to homepage
    if current_user.is_authenticated:
        return redirect("/")

    form = forms.LoginForm()

    if form.validate_on_submit():

        # looks for entries in the database with a matching email from the form
        user = accounts_db.find_one({"email": form.email.data})

        # checks if user is not null. checks if password matches
        if user and bcrypt.check_password_hash(user["password"], form.password.data):
            user_object = User(user["username"], user["email"], user["password"], user["confirmed"])

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
                         "password": hashed_password,
                         "confirmed": False
                         }

        new_user_preferences = {
            "username": form.username.data,
            "intolerances": [],
            "macros": {"carbohydrates": None,
                       "protein": None,
                       "fats": None}
        }

        new_user_favorites = {
            "username": form.username.data,
            "favorites": {}
        }

        # inserts new entries in database
        accounts_db.insert_one(new_user_info)
        preferences_db.insert_one(new_user_preferences)
        favorites_db.insert_one(new_user_favorites)

        # confirmation email
        token = email_util.generate_token(form.email.data, 'email-confirm')
        confirmation_link = email_util.generate_confirmation_link(token, "auth.confirm_email")
        message = email_util.create_confirmation_email(form.email.data, confirmation_link)
        email_util.send_email(message)

        flash("Confirmation email has been sent.")
        return redirect("/login")

    return render_template("register.html", form=form)


@auth.route("/password-reset", methods=['GET', 'POST'])
def password_reset():
    if current_user.is_authenticated:
        return redirect("/")

    form = forms.ForgotPasswordForm()

    if form.validate_on_submit():
        email = form.email.data

        # password reset email
        token = email_util.generate_token(email, 'password-reset')
        confirmation_link = email_util.generate_confirmation_link(token, "auth.confirm_password_reset")
        message = email_util.create_password_reset_email(email, confirmation_link)
        email_util.send_email(message)

        flash("Password reset email has been sent")
        return redirect("/")

    return render_template("password_reset.html", form=form)


@auth.route("/password-reset/<token>", methods=['GET', 'POST'])
def confirm_password_reset(token):
    email = email_util.confirm_token(token, 'password-reset')

    if email:
        form = forms.NewPasswordForm()

        if form.validate_on_submit():
            # encrypts password
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            accounts_db.update_one({"email": email},
                                   {"$set": {"password": hashed_password}})

            flash("Password changed successfully")

            return redirect("/login")

        return render_template("new_password.html", form=form)

    else:
        return redirect("/")


@auth.route('/confirm/<token>')
def confirm_email(token):
    email = email_util.confirm_token(token, 'email-confirm')
    if email:

        accounts_db.update_one({"email": email},
                               {"$set": {"confirmed": True}})

        flash("Account has been verified", 'success')
        return redirect("/login")

    else:
        flash("Link has expired", 'failure')
        return redirect("/login")


@auth.route('/confirm-change/<token>')
def confirm_change_email(token):
    email = email_util.confirm_token(token, 'email-confirm')
    if email:

        record = email_confirmations.find_one({"token": token})
        account_id = record["id"]

        accounts_db.update_one({"_id": account_id},
                               {"$set":
                                    {"confirmed": True,
                                     "email": email
                                     }})

        email_confirmations.delete_one({"token": token})

        flash("Your new email has been verified.", 'success')
        return redirect("/login")

    else:
        flash("Link has expired", 'failure')
        return redirect("/login")


@auth.route('/resend-confirmation')
@login_required
def resend_confirmation():
    # confirmation email
    token = email_util.generate_token(current_user.email, 'email-confirm')
    confirmation_link = email_util.generate_confirmation_link(token, "auth.confirm_email")
    message = email_util.create_confirmation_email(current_user.email, confirmation_link)
    email_util.send_email(message)

    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    user = accounts_db.find_one({"username": user_id})

    if user:
        return User(user["username"], user["email"], user["password"], user["confirmed"])

    return None
