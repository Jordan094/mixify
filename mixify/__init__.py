import os # Import the os module for interacting with the operating system
from flask import Flask # Import the Flask class from the flask package
from flask_sqlalchemy import SQLAlchemy # Import the SQLAlchemy class from the flask_sqlalchemy package

# Check if the file 'env.py' exists
if os.path.exists("env.py"):
    import env # If Exists Import contents of 'env.py'

# Create a Flask application instance
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") # Secret Key for Security
if os.environ.get("DEVELOPMENT") == "True":
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URL")
else:
    uri = os.environ.get("DATABASE_URL")
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = uri


# Create an instance of SQLAlchemy for database management
db = SQLAlchemy(app)

# Import routes from the 'mixify' package
from mixify import routes