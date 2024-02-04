from flask import render_template
from mixify import app, db

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/favourites")
def favourites():
    return render_template("favourites.html")