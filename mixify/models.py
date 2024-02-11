from mixify import db # Import the db instance from the mixify package

# Define the User model
class User(db.Model):
    # Define the columns for the User table
    id = db.Column(db.Integer, primary_key=True) # Primary key column for user ID
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    user_first_name = db.Column(db.String(50), nullable=False)
    user_last_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(260), nullable=False)
    favorites = db.relationship('Favorite', backref='user', lazy=True)

# Define the Recipe model
class Recipe(db.Model):
    # Define the columns for the Recipe table
    recepieid = db.Column(db.Integer, primary_key=True) # Primary key column for recipe ID
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(100), nullable=True)
    submitter_username = db.Column(db.String(50), nullable=False)
    favorited_by = db.relationship('Favorite', backref='recipe', lazy=True)

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.recepieid'), nullable=False)
