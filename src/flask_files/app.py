from flask import Flask, render_template, redirect, request
from src.flask_files import database, extensions


def create_app():
    app = Flask(__name__, template_folder='./templates', static_folder="../static")

    SECRET_KEY = "i6!IgiclHbbC+Out@O$@cz4^@:Bz(GSM5Ts{>1@cHI=QY0{t'>+NR27{lY^|s,C"
    URI = "mongodb+srv://recipeapp:94cQWKQqdXeLGrhV@recipeapp.wsu3zml.mongodb.net/?retryWrites=true&w=majority"

    database.init_app(app)

    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["MONGO_URI"] = URI

    extensions.bcrypt.init_app(app)
    extensions.login_manager.init_app(app)
    extensions.cache.init_app(app)

    from src.flask_files.auth import auth as auth_blueprint
    from src.flask_files.views import views as views_blueprint
    app.register_blueprint(views_blueprint)
    app.register_blueprint(auth_blueprint)

    return app






