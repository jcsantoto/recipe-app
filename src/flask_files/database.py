from flask_pymongo import PyMongo

mongo = PyMongo()

client = mongo.cx
db = client["recipeapp"]
accounts = db["accounts"]


def init_app(app, uri):
    mongo.init_app(app, uri)
