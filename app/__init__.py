from  flask import Flask
from app.config import Config
from app.extensions import db, login_manager
from flask import current_app
from app.models import User

def seed_admin():
    admin_email = current_app.config.get('ADMIN_EMAIL')
    admin_password = current_app.config.get('ADMIN_PASSWORD')

    admin_user = User.query.filter_by(email=admin_email).first()
    
    if admin_user:
        return  # Admin user already exists

    admin_user = User(email=admin_email, role='admin',name='Admin')
    admin_user.set_password(admin_password)

    db.session.add(admin_user)
    db.session.commit()
    
def create_app(class_name=Config):
    
    app = Flask(__name__)
    
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)
    
    from app.routes.auth import auth
    from app.routes.admin import admin_bp
    from app.routes.main import main_bp
    
    app.register_blueprint(auth)
    app.register_blueprint(admin_bp)
    app.register_blueprint(main_bp)

    return app

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

    