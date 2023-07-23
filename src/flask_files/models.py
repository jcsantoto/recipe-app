from flask_login import UserMixin
from src.flask_files.database import mongo

client = mongo.cx
db = client["recipeapp"]
favorites_db = db["favorites"]
preferences_db = db["preferences"]
recommendation_db = db["recommendation"]
search_history = db["SearchHistory"]



class User(UserMixin):

    def __init__(self, username, email, password_hash, confirmed):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.confirmed = confirmed
        self.preferences = self.load_preferences(username)
        self.favorites = self.load_favorites(username)


    def load_recommendations(self):
        recommendations = recommendation_db.find_one({"username": self.username})
        return recommendations

    def load_history(self):
        history = search_history.find_one({"username": self.username})
        return history

    def load_preferences(self, username):
        preferences = preferences_db.find_one({"username": username})
        return preferences

    def load_favorites(self, username):
        favorites = favorites_db.find_one({"username": username})
        return favorites

    def get_id(self):
        return self.username

    def __repr__(self):
        return f"User('{self.username}', '{self.email}'')"
