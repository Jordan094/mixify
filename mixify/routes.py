from flask import flash, render_template, request, redirect, session, url_for, abort
from mixify import app, db
from mixify.models import User, Recipe
from werkzeug.security import generate_password_hash, check_password_hash

# Route for the home page
@app.route("/")
def home():
    return render_template("index.html")


# Route for displaying favorite recipes
@app.route("/favourites")
def favourites():
    return render_template("favourites.html")


# Route for displaying all recipes
@app.route("/recipes")
def recipes():
    recipes = Recipe.query.all()
    return render_template("recipes.html", recipes=recipes)


# Route for adding a new recipe
@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        # Extract data from the form
        recipe_title = request.form.get("recipe_title")
        recipe_description = request.form.get("recipe_description")
        recipe_ingredients = request.form.get("recipe_ingredients")
        recipe_instructions = request.form.get("recipe_instructions")
        
        # Process file upload
        recipe_image = request.files['recipe_image']
        
        # Retrieve the currently logged-in user's username from the session
        submitter_username = session.get("user")
        
        # Create a Recipe instance and add it to the database
        recipe = Recipe(title=recipe_title, 
                        description=recipe_description, 
                        ingredients=recipe_ingredients, 
                        instructions=recipe_instructions, 
                        image_path=recipe_image.filename,
                        submitter_username=submitter_username)
        db.session.add(recipe)
        db.session.commit()
        
        # Redirect the user after adding the recipe
        return redirect(url_for("home"))

    return render_template("add_recipe.html")


# Route for displaying recipes submitted by the current user
@app.route("/my_recipes")
def my_recipes():
    # Get the username of the currently logged-in user from the session
    username = session.get("user")
    
    # Retrieve recipes belonging to the logged-in user
    user_recipes = Recipe.query.filter_by(submitter_username=username).all()
    
    return render_template("my_recipes.html", user_recipes=user_recipes)


# Route for viewing a specific recipe
@app.route("/view_recipe/<int:recipe_id>")
def view_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        abort(404)
    return render_template("view_recipe.html", recipe=recipe)


# Route for deleting a recipe
@app.route("/delete_recipe/<int:recipe_id>", methods=["POST"])
def delete_recipe(recipe_id):
    # Check if the user is logged in
    if "user" not in session:
        flash("You need to log in to delete a recipe.")
        return redirect(url_for("login"))

    # Get the current user's username
    current_user = session["user"]

    # Retrieve the recipe from the database
    recipe = Recipe.query.get(recipe_id)

    # Check if the recipe exists
    if not recipe:
        flash("Recipe not found.")
        return redirect(url_for("home"))

    # Check if the current user is the submitter of the recipe
    if current_user != recipe.submitter_username:
        flash("You can only delete recipes that you have submitted!")
        return redirect(url_for("recipes"))

    # Delete the recipe from the database
    db.session.delete(recipe)
    db.session.commit()

    flash("Recipe deleted successfully.")
    return redirect(url_for("home"))


# Route for displaying the signup page
@app.route("/signup")
def signup():
    return render_template("signup.html")


# Route and function for user registration
@app.route("/signup", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Check if the chosen username is already in use
        existing_user = User.query.filter(User.user_name == request.form.get("user_name").lower()).all()
        if existing_user:
            flash("This username is already in use. Please try a different username")
            return redirect(url_for("register"))

        # Create a new user record in the database
        user = User(
            user_name=request.form.get("user_name").lower(),
            user_first_name=request.form.get("first_name").lower(),
            user_last_name=request.form.get("last_name").lower(),
            password=generate_password_hash(request.form.get("password"))
        )
        db.session.add(user)
        db.session.commit()
        session["user"] = request.form.get("user_name").lower()
        flash("Signup complete - Thank you for joining Mixify!")
        return redirect(url_for("home"))

    return render_template("login.html")


# Route for displaying the login page
@app.route("/login")
def login():
    return render_template("login.html")


# Route and function for user login
@app.route("/login", methods=["GET", "POST"])
def sitelogin():
    if request.method == "POST":
        # Check if the username is present in the database
        existing_user = User.query.filter(User.user_name == request.form.get("user_name").lower()).all()

        if existing_user:
            # Check if the password matches
            if check_password_hash(existing_user[0].password, request.form.get("password")):
                session["user"] = request.form.get("user_name").lower()
                flash("You are logged in as, {}".format(request.form.get("user_name")))
                return redirect(url_for("recipes"))
            else:
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            flash("Incorrect Username and/or Password")
            return redirect(url_for("recipes"))


# Route for user logout
@app.route("/logout")
def logout():
    flash("You are no longer logged in")
    session.pop("user")
    return redirect(url_for("login"))