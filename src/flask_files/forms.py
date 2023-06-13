from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, BooleanField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms import validators
from flask_login import current_user
from .extensions import bcrypt


class SearchForm(FlaskForm):
    """
    Class to help validate and retrieve data from fields in the search bar.
    """
    query = StringField('query')


class RegistrationForm(FlaskForm):
    """
    Class to help validate and retrieve data from fields in the registration form
    """
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    """
    Class to help validate and retrieve data from fields in the login form
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class AccountSettingsForm(FlaskForm):
    """
    Class to help validate and retrieve data from fields in the Account Settings Form
    """

    intolerance_choices = [(1, "Dairy"), (2, "Egg"), (3, "Gluten"), (4, "Grain"), (5, "Peanut"),
                           (6, "Seafood"), (7, "Sesame"), (8, "Shellfish"), (9, "Soy"),
                           (10, "Sulfite"), (11, "Tree"), (12, "Nut"), (13, "Wheat")]

    username = StringField('Username', validators=[Length(min=2, max=20), Optional()])
    email = StringField('Email', validators=[Email(), Optional()])
    intolerances = SelectMultipleField('Intolerances', validators=[Optional()], choices=intolerance_choices,
                                       widget=ListWidget(prefix_label=False), option_widget=CheckboxInput(),
                                       coerce=int)
    old_password = PasswordField('Old Password', validators=[])
    new_password = PasswordField('New Password', validators=[])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('new_password')])
    submit = SubmitField('Save Changes')

    def validate_username(self, username):
        if current_user.username == username.data:
            raise validators.ValidationError("New username cannot be the same as the current username.")

    def validate_email(self, email):
        if current_user.email == email.data:
            raise validators.ValidationError("New email cannot be the same as the current email.")

    def validate_old_password(self, old_password):
        if (self.new_password.data or self.confirm_password.data) and not old_password.data:
            raise validators.ValidationError("Old Password is Required.")

        if old_password.data and not bcrypt.check_password_hash(current_user.password_hash, old_password.data):
            raise validators.ValidationError("Incorrect password")

    def validate_new_password(self, new_password):
        if (self.old_password.data or self.confirm_password.data) and not new_password.data:
            raise validators.ValidationError("New Password is Required.")

    def validate_confirm_password(self, confirm_password):
        if (self.new_password.data or self.old_password.data) and not confirm_password.data:
            raise validators.ValidationError("Confirm Password is required.")
