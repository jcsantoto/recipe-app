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
 <b> When logged in: </b>
 * Account: Displays information about the user such as their username and email.
 * Logout: Logs the user out of their account.

# Developer Documentation

### src
- `main.py`: Creates and runs the flask web application.
- `recipe_info.py`: Obtains information of a recipe using an ID and stores in a Recipe object. Contains several methods to retrieve different aspects of the recipe.
- `search.py`: Contains functions related to retrieving recipes by name and by ingredients as well as various sorting and filtering functions.
- `virtual_shopping_list.py`: Contains code to create a virtual shopping list of a recipe and serving it as a pdf.

### src/flask_files
- `app.py`: Contains a single function which intializes the flask app, the database, and any flask extensions.
- `auth.py`: Contains code for flask routes related to authentication such as Login, Registration, and Logout.
- `database.py`: Contains a single function to initialize the database.
- `extension.py`: Contains flask extensions and their instances.
- `forms.py`: Contains classes for each type of form needed for the website such as the Login form and Registration form.
- `models.py`: Contains a class that models a User by their username, email, and password.
- `views.py`: Contains code for flask routes that are not related authentication.

### templates
- `about.html`: Contains template for the About Us page.
- `account.html`: Contains a template for the Account page.
- `display_results.html`: Contains a template for the results page after searching for a recipe.
- `index.html`: Contains a template for the home page.
- `login.html`: Contains a template for the login page.
- `register.html`: Contains a template for the register page.
- `shopping_list.html`: Contains a template for the virtual shopping list.
- `template.html`: Contains code for the navigation bar.

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
UI/UX designer, Scrum Master


