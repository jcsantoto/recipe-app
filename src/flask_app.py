from flask import Flask, render_template, redirect, request
from flask_pymongo import PyMongo

URI = "mongodb+srv://recipeapp:5YHQYhTvGOTnWKoB@recipeapp.wsu3zml.mongodb.net/?retryWrites=true&w=majority"

app = Flask(__name__, template_folder='./templates')
app.config["MONGO_URI"] = URI
app.config["SECRET_KEY"] = "i6!IgiclHbbC+Out@O$@cz4^@:Bz(GSM5Ts{>1@cHI=QY0{t'>+NR27{lY^|s,C"

mongo = PyMongo(app, URI)
client = mongo.cx
db = client["recipeapp"]
accounts = db["accounts"]


@app.route("/")
def home_page():
    return render_template("index.html")


@app.route("/login")
def login_page():
    return render_template("login.html")


@app.route("/register")
def register_page():
    return render_template("register.html")


if __name__ == '__main__':
    app.run(debug=True)
