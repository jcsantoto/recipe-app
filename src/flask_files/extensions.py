from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_login import LoginManager

bcrypt = Bcrypt()
login_manager = LoginManager()
cache = Cache()
