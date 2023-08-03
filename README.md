# Recipe Web Application

This is a web application that allows users to search for recipes by name and by ingredients. It includes various sorting/filtering features as well as account specific features like favoriting recipes. This application is developed in Python, using Flask as the framework and MongoDB as the database. It retrieves recipes from the Spoonacular API.

# Usage (Running locally)

To run the application locally, run main.py located in the src folder. Then open http://127.0.0.1:5000/ in the browser of your choice.

# Navigating the Website
When visiting the website, you will be greeted by the home page.
From there, there is a navigation bar that will allow you to visit various other pages.

 * Home: The landing page of the website. Currently displays a greeting and a navigation bar.
 * About Us: Displays information about the website as well as the development team.
 * Register: Allows the user to register for an account to access various features.
 * Login: Allows the user to login to their account and access various features.
 * Search: A search bar that allows a user to enter a query to search for a recipe.

<b> After searching: </b>
Results: Displays results of the search. Shows various sorting and filtering options on the side.
Recipe: Displays information about the recipe such as 
 
 <b> When logged in: </b>
 * Account: Displays information about the user such as their username and email.
 * Account Settings: Allows user to change their username, email, and other preferences.
 * Logout: Logs the user out of their account.

# Developer Documentation

### src
- `api_options.py`: Contains enum classes to help maintain consistency when specifying an option for a parameter in an API call.
- `email_util.py`: Contains functions to help create and send emails using SendGrid.
- `main.py`: Creates and runs the flask web application.
- `recipe_info.py`: Obtains information of a recipe using an ID and stores in a Recipe object. Contains several methods to retrieve different aspects of a recipe.
- `recipe_info_util.py`: Contains various helper functions to aid in working with recipe info. This includes functions to check for certain allergens in an ingredients list and a function to clean up the summary of a recipe.
- `search.py`: Contains a function for searching that takes in various parameters to customize the search. Also contains various helper functions to aid in retrieval and filtering of data.
- `search_builder.py`: Helps build the API call for searching for recipes.
- `trending_recipe.py`: Increments view counts of recipes and retrieves top 3 most viewed as trending.
- `user_recipes.py`: Obtains information of a user created recipe using an ID and stores in a UserRecipe object. Contains several methods to retrieve different aspects of a recipe.


### src/flask_files
- `app.py`: Contains a single function which intializes the flask app, the database, and any flask extensions.
- `accounts.py`: Contains code for flask routes related to the user's account such as the Account and Account Settings page.
- `auth.py`: Contains code for flask routes related to authentication such as Login, Registration, and Logout.
- `config.py`: Contains code to load secrets from the environment file.
- `database.py`: Contains a single function to initialize the database.
- `extensions.py`: Contains flask extensions and their instances.
- `forms.py`: Contains classes for each type of form needed for the website such as the Login form and Registration form.
- `models.py`: Contains a class that models a User by their username, email, and password.
- `redis_util.py`: Contains code to instantiate Redis client object.
- `views.py`: Contains code for flask routes that are not related authentication.

### src/static/js

- `account.js`: Contains code to load account page info dynamically.
- `additional_field.js`: Contains code to add additional ingredient and instruction fields for user created recipes.
- `cache_recipe.js`: Contains code to store recipe date in JavaScript localStorage.
- `favorite.js`: Contains code for an AJAX request to add a recipe to the favorites collection.
- `tags.js`: Contains code to apply selectize from the Selectize library to input boxes.
- `toggle.js`: Contains code to selectize and deselectize a search bar when clicking a toggle.



## Credits

#### Abdulai [GitHub](https://github.com/Abdulai00)
Backend Developer

#### Elvis [GitHub](https://github.com/Elvis-pixel)
Backend Developer

#### Gerald [GitHub](https://github.com/GeraldReyes00)
Frontend Developer

#### John [GitHub](https://github.com/jcsantoto)
Backend Developer

#### Kenny [GitHub](https://github.com/kennyt1232)
UI/UX consultant, SM, PM


