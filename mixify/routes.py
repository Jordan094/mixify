from flask import render_template
from mixify import app, db

@app.route("/")
def home():
    return render_template("index.html")