from flask import flash, render_template, request, redirect, session, url_for, abort
from mixify import app, db
from mixify.models import User, Recipe, Favorite
from werkzeug.security import generate_password_hash, check_password_hash

# Route for the home page
@app.route("/")
def home():
    return render_template("index.html")





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

        # Retrieve the currently logged-in user's username from the session
        submitter_username = session.get("user")
        
        # Create a Recipe instance and add it to the database
        recipe = Recipe(title=recipe_title, 
                        description=recipe_description, 
                        ingredients=recipe_ingredients, 
                        instructions=recipe_instructions, 
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


@app.route("/edit_recipe/<int:recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    # Check if the user is logged in
    if "user" not in session:
        flash("You need to log in to edit a recipe.")
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
        flash("You can only edit recipes that you have submitted!")
        return redirect(url_for("recipes"))

    if request.method == "POST":
        # Extract data from the form
        recipe_title = request.form.get("recipe_title")
        recipe_description = request.form.get("recipe_description")
        recipe_ingredients = request.form.get("recipe_ingredients")
        recipe_instructions = request.form.get("recipe_instructions")

        # Update the recipe data
        recipe.title = recipe_title
        recipe.description = recipe_description
        recipe.ingredients = recipe_ingredients
        recipe.instructions = recipe_instructions

        # Commit changes to the database
        db.session.commit()

        flash("Recipe edited successfully.")
        return redirect(url_for("home"))

    # If it's a GET request, render the template with the existing recipe data
    return render_template("edit_recipe.html", recipe=recipe)


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

@app.route("/favourites")
def my_favourites():
    # Retrieve the username from the session
    username = session.get("user")

    if not username:
        # If the user is not logged in, you might want to redirect them to the login page
        return redirect(url_for("login"))

    # Fetch the user's favorite recipes from the database
    user = User.query.filter_by(user_name=username).first()

    if not user:
        # USer invalid
        return "User not found", 404

    # Convert user_id to integer
    user_id = user.id

    # Fetch the user's favorite recipes from the database using the user_id
    user_favorites = Favorite.query.filter_by(user_id=user_id).all()

    # Extract the recipe IDs from the favorites
    favorite_recipe_ids = [fav.recipe_id for fav in user_favorites]

    # Fetch the actual recipe objects based on the recipe IDs
    favorites = Recipe.query.filter(Recipe.recepieid.in_(favorite_recipe_ids)).all()

    return render_template("favourites.html", favorites=favorites)

# Route to add a recipe to favorites
@app.route('/favorite/add/<int:recipe_id>', methods=['POST'])
def add_to_favorites(recipe_id):
    # Retrieve the username from the session
    username = session.get("user")
    
    # Retrieve the user ID from the database using the username
    user = User.query.filter_by(user_name=username).first()
    
    if not user:
        flash('User not logged in.', 'error')
        return redirect(url_for('login'))  # Redirect to login page or wherever appropriate
    
    recipe = Recipe.query.get_or_404(recipe_id)
    
    if Favorite.query.filter_by(user_id=user.id, recipe_id=recipe_id).first():
        flash('Recipe is already in favorites.', 'error')
        return redirect(url_for('view_recipe', recipe_id=recipe_id))
    
    favorite = Favorite(user_id=user.id, recipe_id=recipe_id)
    db.session.add(favorite)
    db.session.commit()
    
    flash('Recipe added to favorites successfully.', 'success')
    return redirect(url_for('view_recipe', recipe_id=recipe_id))

# Route to remove a recipe from favorites
@app.route('/favorite/remove/<int:recipe_id>', methods=['POST'])
def remove_from_favorites(recipe_id):
    # Retrieve the username from the session
    username = session.get("user")
    
    # Retrieve the user ID from the database using the username
    user = User.query.filter_by(user_name=username).first()
    
    if not user:
        flash('User not logged in.', 'error')
        return redirect(url_for('login'))  # Redirect to login page or wherever appropriate
    
    favorite = Favorite.query.filter_by(user_id=user.id, recipe_id=recipe_id).first()
    
    if not favorite:
        flash('Recipe is not in favorites.', 'error')
        return redirect(url_for('view_recipe', recipe_id=recipe_id))
    
    db.session.delete(favorite)
    db.session.commit()
    
    flash('Recipe removed from favorites successfully.', 'success')
    return redirect(url_for('view_recipe', recipe_id=recipe_id))