from flask_pymongo import PyMongo

URI = "mongodb+srv://recipeapp:94cQWKQqdXeLGrhV@recipeapp.wsu3zml.mongodb.net/?retryWrites=true&w=majority"
mongo = PyMongo()


def init_app(app):
    mongo.init_app(app, URI)




