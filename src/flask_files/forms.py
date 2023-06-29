from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms.fields import StringField, PasswordField, SubmitField, BooleanField, SelectMultipleField, SelectField, \
    IntegerField, FieldList, FormField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms import validators
from src.flask_files.extensions import bcrypt
from src.api_options import SortOptions, DietOptions, IntoleranceOptions


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

    intolerance_choices = [(0, "Dairy"), (1, "Egg"), (2, "Gluten"), (3, "Grain"), (4, "Peanut"),
                           (5, "Seafood"), (6, "Sesame"), (7, "Shellfish"), (8, "Soy"),
                           (9, "Sulfite"), (10, "Tree Nut"), (11, "Wheat")]

    intolerances = SelectMultipleField('Intolerances', validators=[Optional()], choices=intolerance_choices,
                                       widget=ListWidget(prefix_label=False), option_widget=CheckboxInput(),
                                       coerce=int)

    protein = IntegerField('Protein', validators=[Optional()], render_kw={"placeholder": "-"})
    carbohydrates = IntegerField('Carbohydrates', validators=[Optional()], render_kw={"placeholder": "-"})
    fats = IntegerField('Fats', validators=[Optional()], render_kw={"placeholder": "-"})

    username = StringField('Username', validators=[Length(min=2, max=20), Optional()])
    email = StringField('Email', validators=[Email(), Optional()])
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


class Range(FlaskForm):
    min_value = IntegerField('Min', validators=[Optional()], render_kw={"placeholder": "Min"})
    max_value = IntegerField('Max', validators=[Optional()], render_kw={"placeholder": "Max"})

    def validate_min_value(self, min_value):
        if not min_value.data:
            return

        if min_value.data < 0:
            raise validators.ValidationError("Input a positive number")

        if self.max_value.data and min_value.data > self.max_value.data:
            raise validators.ValidationError("Minimum cannot be greater than maximum")

    def validate_max_value(self, max_value):
        if not max_value.data:
            return

        if max_value.data < 0:
            raise validators.ValidationError("Input a positive number")

        if self.min_value.data and max_value.data < self.min_value.data:
            raise validators.ValidationError("Maximum cannot be less than minimum")


class SortAndFilterOptionsForm(FlaskForm):
    """
    Class to help validate and retrieve data from the sorting and filtering fields
    """

    sort_options = [e.value for e in SortOptions]
    diet_option = [e.value for e in DietOptions]
    intolerance_option = [e.value for e in IntoleranceOptions]

    sort = SelectField('Sort', validators=[Optional()], choices=sort_options)
    ingredients = StringField("Ingredients Filter", validators=[Optional()],
                              render_kw={"placeholder": "milk, apple, ..."})
    diet = SelectMultipleField('Diet', validators=[Optional()], choices=diet_option)
    intolerances = SelectMultipleField('Intolerance', validators=[Optional()], choices=intolerance_option)

    custom_filters = FieldList(FormField(Range), min_entries=3, max_entries=3)

    nutrition = FieldList(FormField(Range), min_entries=4, max_entries=4)

    apply = SubmitField('Apply')
