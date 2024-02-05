from flask import flash, render_template, request, redirect, session, url_for
from mixify import app, db
from mixify.models import User
from werkzeug.security import generate_password_hash, check_password_hash

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/favourites")
def favourites():
    return render_template("favourites.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/recipes")
def recipes():
    return render_template("recipes.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")


# Function for new users to isgn up to site
@app.route("/signup", methods=["GET", "POST"])
def register():
    """Generates a page with a sign up form. Which allows a user to signup"""
    if request.method == "POST":
        # Checks database to query if Chosen Username is already being used
        existing_user = User.query.filter(
            User.user_name == request.form.get("user_name").lower()).all()
        # If username is in use. Alerts user and requests they chose another username
        if existing_user:
            flash(
                "This username is already in use. Please try a different username")
            return redirect(url_for("register"))

        user = User(
            user_name=request.form.get("user_name").lower(),
            user_first_name=request.form.get("first_name").lower(),
            user_last_name=request.form.get("last_name").lower(),
            password=generate_password_hash(request.form.get("password"))
        )
        # Creates a user record in database
        db.session.add(user)
        db.session.commit()
        session["user"] = request.form.get("user_name").lower()
        # Informs the users that signup is successful
        flash("Signup complete - Thank you for joining Mixify!")
        return redirect(url_for("login"))

