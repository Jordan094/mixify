from flask import render_template
from mixify import app, db

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/favourites")
def favourites():
    return render_template("favourites.html")

@app.route("/log-in")
def login():
    return render_template("log-in.html")

@app.route("/recipes")
def recipes():
    return render_template("recipes.html")

@app.route("/sign-up")
def signup():
    return render_template("sign-up.html")