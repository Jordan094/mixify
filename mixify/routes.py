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
        # checks if username already exists
        existing_user = User.query.filter(
            User.user_name == request.form.get("user_name").lower()).all()

        if existing_user:
            flash(
                "Username already exists. Please try a different username")
            return redirect(url_for("register"))

        user = User(
            user_name=request.form.get("user_name").lower(),
            user_first_name=request.form.get("first_name").lower(),
            user_last_name=request.form.get("last_name").lower(),
            password=generate_password_hash(request.form.get("password"))
        )

        # Add user to databsase
        db.session.add(user)
        db.session.commit()

        # put the new user into 'session' cookie
        session["user"] = request.form.get("user_name").lower()
        flash("Registration Successful!")
        return redirect(url_for("favourites"))

    return render_template("login.html")

@app.route("/login", methods=["GET", "POST"])
def sitelogin():
    """Renders log in page and allows user to login"""
    if request.method == "POST":
        # check if username exists in db
        existing_user = User.query.filter(
            User.user_name == request.form.get("user_name").lower()).all()

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user[0].password, request.form.get("password")):
                session["user"] = request.form.get("user_name").lower()
                flash("Welcome, {}".format(
                    request.form.get("user_name")))
                return redirect(url_for(
                    "recipes"))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")
