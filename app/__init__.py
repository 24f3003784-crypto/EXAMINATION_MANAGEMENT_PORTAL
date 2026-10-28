from  flask import Flask
from app.config import Config
from app.extensions import db, login_manager
from flask import current_app
from app.models import User,Department

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
    
def seed_departments():
    departments = [
        {"id": 1, "name": "AERONAUTICAL", "department_code": "AERO-001" },
        {"id": 2, "name": "ELECTRICAL", "department_code": "ELC-001"},
        {"id": 3, "name": "COMPUTER SCIENCE", "department_code": "CS-001" },
        {"id": 4, "name": "MECHANICAL", "department_code": "MECH-001"},
        {"id": 5, "name": "CIVIL", "department_code": "CVL-001"},
    ]

    for department_data in departments:
        existing_department = Department.query.filter_by(name=department_data["name"]).first()
        if not existing_department:
            new_department = Department(id=department_data["id"],name=department_data["name"],department_code=department_data["department_code"])
            db.session.add(new_department)
    
    db.session.commit()
def create_app(class_name=Config):
    
    app = Flask(__name__)
    
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)
    
    from app.routes.auth import auth
    from app.routes.admin import admin_bp
    from app.routes.main import main_bp
    from app.routes.student import student_bp
    
    app.register_blueprint(auth)
    app.register_blueprint(admin_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(student_bp)

    return app

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

    