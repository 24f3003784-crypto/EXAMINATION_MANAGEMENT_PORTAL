from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


# Keep extension objects separate from the app factory. Models can import db
# from here without importing the Flask app itself.
db = SQLAlchemy()
login_manager = LoginManager()