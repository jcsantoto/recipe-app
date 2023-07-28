from flask import Flask
from src.flask_files import database, extensions
from src.flask_files.config import Config
from src.flask_files.redis_util import redis_client


def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")

    SECRET_KEY = Config.SECRET_KEY
    URI = Config.URI

    database.init_app(app)

    redis_client.init_redis_client()

    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["MONGO_URI"] = URI

    extensions.bcrypt.init_app(app)
    extensions.login_manager.init_app(app)

    from src.flask_files.auth import auth as auth_blueprint
    from src.flask_files.views import views as views_blueprint
    from src.flask_files.accounts import accounts as accounts_blueprint
    app.register_blueprint(views_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(accounts_blueprint)

    return app






