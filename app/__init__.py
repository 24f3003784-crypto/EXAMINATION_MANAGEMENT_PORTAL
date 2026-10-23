from  flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.config import Config

def create_app():
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = Config.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
    
  
    from app.routes.auth import auth
    from app.routes.views import views
    app.register_blueprint(auth)
    app.register_blueprint(views)
    
    
    return app