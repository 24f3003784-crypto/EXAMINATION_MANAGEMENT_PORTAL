from app import create_app
from app.extensions import db
from flask import current_app
from app.models import User

app = create_app()
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



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_admin()
    app.run(debug=True)