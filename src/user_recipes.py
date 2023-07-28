from src.flask_files.database import mongo
import gzip
import json


client = mongo.cx
db = client["recipeapp"]
user_recipes = db["user_recipes"]


class UserRecipe:

    def __init__(self):
        self.title = None
        self.description = None
        self.time = None
        self.ingredients = None
        self.instructions = None
        self.diets = None
        self.intolerances = None
        self.id = None
        self.owner = None

    def set_title(self, title: str):
        self.title = title

    def set_description(self, description: str):
        self.description = description

    def set_time(self, time: str):
        self.time = time

    def set_ingredients(self, ingredients: dict):
        self.ingredients = ingredients

    def set_instructions(self, instructions: list):
        self.instructions = instructions

    def set_owner(self, username: str):
        self.owner = username

    def set_diets(self, diets: list):
        self.diets = diets

    def set_intolerances(self, intolerances: list):
        self.intolerances = intolerances

    def add_to_database(self):

        if self.id is None:
            user_recipes.insert_one({
                "title": self.title,
                "description": compress_data(self.description),
                "time": self.time,
                "ingredients": self.ingredients,
                "instructions": compress_object(self.instructions),
                "intolerances": self.intolerances,
                "diets": self.diets,
                "owner": self.owner
            })
        else:
            raise Exception("Cannot add this recipe to the database")

    def remove_from_database(self):
        recipe = user_recipes.delete_one({"_id": self.id})

    def load_from_database(self, recipe_id):
        recipe = user_recipes.find_one({"_id": recipe_id})

        self.id = recipe_id
        self.title = recipe['title']
        self.description = decompress_data(recipe['description'])
        self.time = recipe['time']
        self.ingredients = recipe['ingredients']
        self.instructions = decompress_object(recipe['instructions'])
        self.intolerances = recipe['intolerances']
        self.diets = recipe['diets']
        self.owner = recipe['owner']


def compress_data(data):
    compressed_data = gzip.compress(data.encode('utf-8'))
    return compressed_data


def decompress_data(compressed_data):
    decompressed_data = gzip.decompress(compressed_data).decode('utf-8')
    return decompressed_data


def compress_object(data):
    serialized_data = json.dumps(data).encode('utf-8')
    compressed_data = gzip.compress(serialized_data)
    return compressed_data


def decompress_object(compressed_data):
    decompressed_data = gzip.decompress(compressed_data)
    data = json.loads(decompressed_data.decode('utf-8'))
    return data

